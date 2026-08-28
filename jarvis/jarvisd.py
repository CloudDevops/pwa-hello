"""jarvisd -- the local dashboard daemon.

Owns the state, serves the glass renderer, and pushes updates over SSE. The
whole point is that pushing a panel costs one HTTP POST, so the model never
writes markup: it writes data and this process does the rest.

Stdlib only. Run with:  ./jarvis serve
"""

import json
import os
import queue
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import panels  # noqa: E402

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
STATE_PATH = os.environ.get(
    "JARVIS_STATE", os.path.expanduser("~/.jarvis/state.json")
)

HEARTBEAT_SECS = 20
MAX_BODY = 1 << 20  # 1 MiB is far more than any panel needs

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
}


class Hub:
    """Holds the state and fans changes out to connected dashboards."""

    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.state = panels.load(path)
        self.clients = set()

    def snapshot(self):
        with self.lock:
            return json.loads(json.dumps(self.state))

    def _commit(self, state):
        state["ts"] = panels.now()
        self.state = state
        try:
            panels.save(self.path, state)
        except OSError as exc:
            sys.stderr.write("jarvisd: could not persist state: %s\n" % exc)
        payload = json.dumps(state, separators=(",", ":"))
        dead = []
        for q in self.clients:
            try:
                q.put_nowait(payload)
            except queue.Full:
                dead.append(q)
        for q in dead:
            self.clients.discard(q)

    def push(self, zone, panel):
        if zone not in panels.ZONES:
            raise ValueError(
                "unknown zone %r (want one of: %s)" % (zone, ", ".join(panels.ZONES))
            )
        panel = panels.normalize_panel(panel)
        with self.lock:
            state = json.loads(json.dumps(self.state))
            state["zones"][zone] = panel
            self._commit(state)

    def replace(self, state):
        state = panels.normalize_state(state)
        with self.lock:
            self._commit(state)

    def clear(self, zone=None):
        with self.lock:
            state = json.loads(json.dumps(self.state))
            if zone:
                if zone not in panels.ZONES:
                    raise ValueError("unknown zone %r" % zone)
                state["zones"][zone] = None
            else:
                state = panels.empty_state()
            self._commit(state)

    def subscribe(self):
        q = queue.Queue(maxsize=32)
        with self.lock:
            self.clients.add(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            self.clients.discard(q)


HUB = None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "jarvisd"

    def log_message(self, fmt, *args):  # quieter than the default
        if os.environ.get("JARVIS_VERBOSE"):
            sys.stderr.write("jarvisd %s\n" % (fmt % args))

    # -- helpers --------------------------------------------------------

    def _send(self, code, body=b"", ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, separators=(",", ":")))

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        if length > MAX_BODY:
            raise ValueError("body too large")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    # -- routes ---------------------------------------------------------

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path == "/events":
            return self._events()
        if path == "/api/state":
            return self._json(200, HUB.snapshot())
        if path == "/api/health":
            return self._json(200, {"ok": True, "pid": os.getpid()})

        rel = "index.html" if path == "/" else path.lstrip("/")
        # Keep the static handler inside WEB_DIR.
        full = os.path.normpath(os.path.join(WEB_DIR, rel))
        if not full.startswith(WEB_DIR) or not os.path.isfile(full):
            return self._send(404, "not found", "text/plain; charset=utf-8")

        ext = os.path.splitext(full)[1]
        with open(full, "rb") as fh:
            body = fh.read()
        return self._send(200, body, CONTENT_TYPES.get(ext, "application/octet-stream"))

    do_HEAD = do_GET

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            body = self._body()
        except ValueError as exc:
            return self._json(400, {"error": "bad json: %s" % exc})

        try:
            if path == "/api/push":
                HUB.push(body.get("zone", "main"), body.get("panel"))
            elif path == "/api/state":
                HUB.replace(body)
            elif path == "/api/clear":
                HUB.clear(body.get("zone"))
            else:
                return self._send(404, "not found", "text/plain; charset=utf-8")
        except ValueError as exc:
            return self._json(400, {"error": str(exc)})
        return self._json(200, {"ok": True})

    def _events(self):
        q = HUB.subscribe()
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()

            # Send current state immediately so a fresh tab paints at once.
            self._emit(json.dumps(HUB.snapshot(), separators=(",", ":")))
            while True:
                try:
                    payload = q.get(timeout=HEARTBEAT_SECS)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    continue
                self._emit(payload)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            HUB.unsubscribe(q)

    def _emit(self, payload):
        self.wfile.write(b"data: " + payload.encode("utf-8") + b"\n\n")
        self.wfile.flush()


def serve(host="127.0.0.1", port=8787):
    global HUB
    HUB = Hub(STATE_PATH)
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.daemon_threads = True
    sys.stderr.write("jarvisd listening on http://%s:%d  (state: %s)\n" % (host, port, STATE_PATH))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\njarvisd stopped\n")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Jarvis dashboard daemon")
    ap.add_argument("--host", default=os.environ.get("JARVIS_HOST", "127.0.0.1"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("JARVIS_PORT", 8787)))
    args = ap.parse_args()
    serve(args.host, args.port)
