# Jarvis dashboard

A persistent HUD for the Mac that the model updates by writing **data**, never
markup. One schema, two renderers: a translucent glass surface in the browser
and an ANSI version for the terminal.

## Why it is built this way

Latency in a dashboard like this is dominated by how many tokens the model has
to emit. Hand-writing a styled HTML view costs thousands of tokens per refresh;
emitting a row array costs a few dozen. So the design work is paid once, at
build time, and every update after that is just data:

```sh
jarvis push main agenda '[["09:00","Standup","30m"],["11:30","Design review","45m","now"]]' -t agenda
```

The corollary is that the pretty renderer costs the same as an ugly one. There
is no speed argument for settling for ASCII.

## Layout

Four fixed zones — `status`, `main`, `side`, `rail` — described in
[SCHEMA.md](SCHEMA.md), which is also the reference for row shapes.

## Running it

Requires nothing but the system `python3`.

```sh
./jarvis serve            # daemon on http://127.0.0.1:8787
./jarvis demo             # fill every zone with sample panels
open http://127.0.0.1:8787
```

For it to survive logout and reboot, install the launchd agent in
[`launchd/`](launchd/com.jarvis.dashboard.plist).

## Commands

```sh
jarvis push <zone> <type> '<rows json>' [-t title] [-s sub] [-a accent] [--state ok|working|stale|error]
jarvis work <zone> "querying calendar…"   # busy state, so latency reads as activity
jarvis show <type> '<rows json>' -t title # terminal only, never touches the daemon
jarvis render                             # draw the whole dashboard in the terminal
jarvis clear [zone]
jarvis status                             # is the daemon up, and what is on screen
```

Rows can also arrive on stdin, which is usually how a fetch script feeds it:

```sh
./fetch_agenda.py | jarvis push main agenda - -t agenda
```

If the daemon is down, `push` still writes the state file and says so; the next
`serve` picks up where it left off.

## Getting it on other devices

The daemon binds loopback by default. Two ways out:

- **LAN** — `jarvis serve --host 0.0.0.0`, then browse to the Mac's IP from the
  iPad. Quickest, but plain HTTP means no service worker (secure-context only)
  and no offline install.
- **Tailscale** — `tailscale serve https / http://127.0.0.1:8787` gives a real
  certificate and a stable hostname, so the dashboard works off the LAN and the
  PWA install behaves properly. This is the better path once you leave the desk.

Note that serving the page from GitHub Pages will *not* work: an HTTPS origin
cannot fetch a plain-HTTP daemon on your Mac. The page has to be served by the
daemon, same-origin with its own data.

## Layout of the code

```
panels.py     schema + normalization + ANSI renderer   (shared)
jarvisd.py    daemon: state, static files, SSE push
jarvis        CLI — the surface the model types against
web/          glass renderer (index.html, app.js, style.css)
launchd/      keep the daemon alive across reboots
```

`panels.py` and `web/app.js` implement the same schema twice. When you add a
panel type, change both — SCHEMA.md lists the three places to touch.

## Not built yet

Warm-cache fetchers on a launchd timer, and the Mac MCP bridge
(`dashboard_push` / `notify`) that lets voice on the phone drive this surface.
The fetchers should be plain scripts hitting the APIs directly — keeping the
model out of the polling loop is what makes a cached answer feel instant.
