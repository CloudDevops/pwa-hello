"""Panel schema: normalization + ANSI terminal rendering.

One schema, two renderers. This module owns the canonical shape of a panel and
the terminal renderer; web/app.js owns the glass renderer. Keep them in sync --
SCHEMA.md is the contract.

Stdlib only, so it runs on a stock macOS python3 with no install step.
"""

import json
import os
import shutil
import time

ZONES = ("status", "main", "side", "rail")

PANEL_TYPES = ("agenda", "list", "mail", "metrics", "table", "log", "text")

# Accent colors, as (r, g, b). Mirrored in web/style.css.
ACCENTS = {
    "cyan": (34, 211, 238),
    "amber": (251, 191, 36),
    "green": (52, 211, 153),
    "red": (248, 113, 113),
    "violet": (167, 139, 250),
}

# Per-row status tints.
STATUS_RGB = {
    "ok": (226, 232, 240),
    "now": (34, 211, 238),
    "warn": (251, 191, 36),
    "crit": (248, 113, 113),
    "muted": (100, 116, 139),
}

DIM = (71, 85, 105)
LABEL = (148, 163, 184)


def _fg(rgb):
    return "\x1b[38;2;%d;%d;%dm" % rgb


RESET = "\x1b[0m"
BOLD = "\x1b[1m"


def now():
    return time.time()


def normalize_panel(panel):
    """Coerce a loosely-specified panel into the canonical shape.

    Everything except `type` is optional -- that is the point. The cheaper a
    panel is to write, the faster it lands on screen.
    """
    if panel is None:
        return None
    if isinstance(panel, str):
        panel = {"type": "text", "items": [panel]}
    if not isinstance(panel, dict):
        raise ValueError("panel must be an object or a string")

    ptype = panel.get("type", "list")
    if ptype not in PANEL_TYPES:
        raise ValueError(
            "unknown panel type %r (want one of: %s)" % (ptype, ", ".join(PANEL_TYPES))
        )

    items = panel.get("items", [])
    # A bare string body for text panels.
    if isinstance(items, str):
        items = [items]
    if not isinstance(items, list):
        raise ValueError("items must be a list")

    rows = []
    for item in items:
        if isinstance(item, (str, int, float)):
            rows.append([str(item)])
        elif isinstance(item, list):
            rows.append([("" if c is None else str(c)) for c in item])
        elif isinstance(item, dict):
            # Object form, for when readability beats brevity.
            keys = {
                "agenda": ("time", "title", "meta", "status"),
                "list": ("text", "meta", "status"),
                "mail": ("from", "subject", "time", "status"),
                "metrics": ("label", "value", "delta", "status"),
                "log": ("time", "text", "status"),
                "table": ("a", "b", "c", "d"),
                "text": ("text",),
            }[ptype]
            rows.append([str(item.get(k, "")) for k in keys])
        else:
            raise ValueError("bad row: %r" % (item,))

    accent = panel.get("accent", "cyan")
    if accent not in ACCENTS:
        accent = "cyan"

    state = panel.get("state", "ok")
    if state not in ("ok", "working", "stale", "error"):
        state = "ok"

    return {
        "type": ptype,
        "title": panel.get("title", ""),
        "sub": panel.get("sub", ""),
        "note": panel.get("note", ""),
        "state": state,
        "accent": accent,
        "items": rows,
        "ts": panel.get("ts") or now(),
    }


def empty_state():
    return {"v": 1, "ts": now(), "zones": {z: None for z in ZONES}}


def normalize_state(state):
    out = empty_state()
    if not isinstance(state, dict):
        return out
    zones = state.get("zones") or {}
    for z in ZONES:
        if zones.get(z):
            try:
                out["zones"][z] = normalize_panel(zones[z])
            except ValueError:
                out["zones"][z] = None
    out["ts"] = state.get("ts") or now()
    return out


# ---------------------------------------------------------------- terminal --

def _clip(s, width):
    """Truncate to width, with an ellipsis when it actually overflows."""
    s = s.replace("\t", " ")
    if width <= 0:
        return ""
    if len(s) <= width:
        return s
    if width == 1:
        return "…"
    return s[: width - 1] + "…"


def _pad(s, width):
    return _clip(s, width).ljust(width)


def _rel(ts):
    d = max(0, int(now() - (ts or 0)))
    if d < 5:
        return "just now"
    if d < 60:
        return "%ds ago" % d
    if d < 3600:
        return "%dm ago" % (d // 60)
    if d < 86400:
        return "%dh ago" % (d // 3600)
    return "%dd ago" % (d // 86400)


def _rows_for(panel, width):
    """Lay a panel's items out into (plain_text, rgb) line tuples."""
    ptype = panel["type"]
    items = panel["items"]
    lines = []

    if not items:
        return [] if panel["state"] == "working" else [("(empty)", DIM)]

    if ptype == "text":
        for row in items:
            text = row[0] if row else ""
            if not text:
                lines.append(("", DIM))
                continue
            # Soft-wrap on words.
            words, cur = text.split(), ""
            for w in words:
                if cur and len(cur) + 1 + len(w) > width:
                    lines.append((cur, STATUS_RGB["ok"]))
                    cur = w
                else:
                    cur = (cur + " " + w).strip()
            if cur:
                lines.append((cur, STATUS_RGB["ok"]))
        return lines

    if ptype == "metrics":
        # Two columns of label/value tiles.
        cols = 2 if width >= 44 else 1
        cw = (width - (cols - 1) * 2) // cols
        buf = []
        for row in items:
            label = row[0] if len(row) > 0 else ""
            value = row[1] if len(row) > 1 else ""
            delta = row[2] if len(row) > 2 else ""
            right = value + ((" " + delta) if delta else "")
            tile = _pad(label, max(0, cw - len(right) - 1)) + " " + right
            buf.append(_pad(tile, cw))
            if len(buf) == cols:
                lines.append(("  ".join(buf), STATUS_RGB["ok"]))
                buf = []
        if buf:
            lines.append(("  ".join(buf), STATUS_RGB["ok"]))
        return lines

    if ptype == "table":
        header, body = items[0], items[1:]
        ncol = max(len(r) for r in items)
        cw = max(6, (width - (ncol - 1) * 2) // ncol)
        lines.append(("  ".join(_pad(c, cw) for c in header), LABEL))
        lines.append(("─" * width, DIM))
        for row in body:
            cells = list(row) + [""] * (ncol - len(row))
            lines.append(("  ".join(_pad(c, cw) for c in cells), STATUS_RGB["ok"]))
        return lines

    # agenda / list / mail / log all share a left / center / right layout.
    layout = {
        "agenda": (0, 1, 2, 3),
        "log": (0, 1, None, 2),
        "mail": (0, 1, 2, 3),
        "list": (None, 0, 1, 2),
    }[ptype]
    li, ci, ri, si = layout

    lead_w = 0
    if li is not None:
        lead_w = min(16, max((len(r[li]) for r in items if len(r) > li), default=0))
    tail_w = 0
    if ri is not None:
        tail_w = min(18, max((len(r[ri]) for r in items if len(r) > ri), default=0))

    mid_w = width - lead_w - tail_w - (2 if lead_w else 0) - (2 if tail_w else 0)
    mid_w = max(4, mid_w)

    for row in items:
        def cell(i):
            return row[i] if (i is not None and len(row) > i) else ""

        status = cell(si) or "ok"
        rgb = STATUS_RGB.get(status, STATUS_RGB["ok"])
        parts = []
        if lead_w:
            parts.append(_pad(cell(li), lead_w))
        parts.append(_pad(cell(ci), mid_w))
        if tail_w:
            parts.append(_clip(cell(ri), tail_w).rjust(tail_w))
        lines.append(("  ".join(parts), rgb))
    return lines


def render_panel(panel, width=None, color=True):
    """Render one panel as a rounded ANSI box."""
    panel = normalize_panel(panel)
    if width is None:
        width = min(shutil.get_terminal_size((80, 24)).columns, 100)
    width = max(24, width)
    inner = width - 4  # border + one space of padding each side

    arg = ACCENTS[panel["accent"]]
    if panel["state"] == "error":
        arg = ACCENTS["red"]
    elif panel["state"] == "working":
        arg = ACCENTS["amber"]

    def c(rgb, s, bold=False):
        if not color:
            return s
        return (BOLD if bold else "") + _fg(rgb) + s + RESET

    title = panel["title"].upper()
    sub = panel["sub"] or _rel(panel["ts"])
    if panel["state"] == "working":
        sub = sub or "working"

    # Top rule:  /-- TITLE ------------------- sub --\
    left = "╭─"
    tpart = (" " + title + " ") if title else "─"
    spart = (" " + sub + " ") if sub else ""
    fill = width - len(left) - len(tpart) - len(spart) - 1
    fill = max(1, fill)
    top = (
        c(arg, left)
        + (c(arg, tpart, bold=True) if title else c(DIM, tpart))
        + c(DIM, "─" * fill)
        + (c(DIM, spart) if spart else "")
        + c(arg, "╮")
    )

    out = [top]
    for text, rgb in _rows_for(panel, inner):
        out.append(c(DIM, "│") + " " + c(rgb, _pad(text, inner)) + " " + c(DIM, "│"))

    if panel["note"]:
        out.append(c(DIM, "│") + " " + c(DIM, _pad(panel["note"], inner)) + " " + c(DIM, "│"))

    out.append(c(arg, "╰" + "─" * (width - 2) + "╯"))
    return "\n".join(out)


def render_state(state, width=None, color=True):
    """Render every populated zone, top to bottom."""
    state = normalize_state(state)
    if width is None:
        width = min(shutil.get_terminal_size((80, 24)).columns, 100)
    chunks = []
    for z in ZONES:
        panel = state["zones"].get(z)
        if panel:
            chunks.append(render_panel(panel, width=width, color=color))
    if not chunks:
        return _fg(DIM) + "no panels" + RESET if color else "no panels"
    return "\n".join(chunks)


def load(path):
    try:
        with open(path, "r") as fh:
            return normalize_state(json.load(fh))
    except (IOError, OSError, ValueError):
        return empty_state()


def save(path, state):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(state, fh, separators=(",", ":"))
    os.replace(tmp, path)
