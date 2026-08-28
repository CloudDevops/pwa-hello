# Handoff — resuming Jarvis from a local session

Written for a Claude Code session running locally on the Mac. The work so far
was done in a cloud session that had no route to this machine, so everything
below is built and tested but has never actually run here.

## Start here

```sh
cd jarvis
./jarvis up          # starts the daemon if needed, opens the dashboard
./jarvis demo        # optional: fill every zone so you can see it working
```

`up` is idempotent and detaches the daemon from your shell. Needs nothing but
the system `python3` — no venv, no pip install.

Then confirm the reactive path end to end: pull the user's calendar through the
Google Calendar connector, curate it (rules below), and push it:

```sh
./jarvis focus agenda '[["15:00","Toddler pickup","15m"]]' -t "today · fri aug 28"
```

If that lands on screen, the loop works and everything else is extension.

## What this is

A HUD the model updates by writing **data, never markup**. Latency here is
dominated by tokens emitted, so a styled view written from scratch costs
thousands of tokens per refresh while a row array costs a few dozen. The
renderers are prebuilt; the model only ever emits rows.

```
panels.py     schema + normalization + ANSI terminal renderer
jarvisd.py    daemon: holds state, serves the page, pushes over SSE
jarvis        the CLI the model types against
web/          glass renderer (index.html, app.js, style.css)
launchd/      keeps the daemon alive across reboots
```

`SCHEMA.md` is the panel contract. `RECIPES.md` maps spoken requests to panels.

## Decisions that should not be silently reverted

Each of these came from a specific correction by Nick or from real data. They
look like omissions if you only read the code.

1. **Reactive, not ambient.** He explicitly does not want a board full of
   widgets. `jarvis focus` clears every zone and shows one panel. Do not
   default to filling all four zones.
2. **No warm-cache fetchers, no launchd polling timers.** These were planned
   and then deliberately cut. Claude already holds the calendar and mail
   connectors, so the model *is* the data feed. A polling daemon would add
   staleness and a second copy of the credentials for no gain.
3. **Panels never scroll.** Overflow is trimmed to a `+N more` line. A
   dashboard you scroll is a page.
4. **The daemon serves the page.** Not GitHub Pages: an HTTPS origin cannot
   fetch a plain-HTTP daemon on localhost, and the browser blocks it silently.
5. **Two renderers, one schema.** `panels.py` and `web/app.js` implement the
   same shapes independently. Change both or they drift — `SCHEMA.md` lists
   the three places to touch.

## Curation is the feature

A live pull of his calendar returned mostly recurring habit blocks — `Sleep`
and `Magnesium`, twice a day — mixed in with real appointments. Dumping that
raw is exactly the clutter he objected to. So when turning connector output
into rows:

- drop recurring habit/health blocks unless they were what was asked for
- `muted` for anything already past, so the eye lands on what is next
- `now` for the thing happening right now — it draws the cyan tick
- say what you hid in `note`, so nothing disappears silently
- keep it under ~12 rows

This is why the model belongs in the loop instead of a cron script.

## Voice: decided

**Local Claude Code voice, to start.** He dictates into a local session; the
session shells out to `jarvis focus`. No transport to build — the shell is the
bridge.

What makes it work is the project skill at `.claude/skills/jarvis/SKILL.md`,
which fires on "pull up my calendar" and similar (with or without a leading
"Jarvis") and encodes the connector → curate → focus pipeline. Two things
about it matter more than they look:

- **The chat reply is spoken aloud.** So it is the headline, one sentence, and
  the detail goes on the glass. Never read a list out loud — it is already on
  screen. Long chat replies are the main way this gets annoying to use.
- **`focus` is the default, not `push`.** He does not want an ambient board.

Deferred, not cancelled: the `mac-mcp` bridge (`dashboard_push` / `notify`)
for driving this from Claude voice on the phone. That is a different surface —
the Claude app is not Claude Code and reaches this Mac only through mac-mcp,
whose source is **not in this repo**. Ask him for the path when he wants it.
A composite `brief()` fanning out to calendar/mail/home in one call is the
other thing worth adding there, since round trips dominate latency.

## Facts you will want

- state: `~/.jarvis/state.json` (`JARVIS_STATE` overrides)
- port 8787 (`JARVIS_PORT`), loopback only by default
- daemon log from `jarvis up`: `~/.jarvis/jarvisd.log`
- persistence across reboot: `launchd/com.jarvis.dashboard.plist`, path
  placeholder needs substituting before it is loaded
- with the daemon down, `push` still writes the state file and warns; the next
  `serve` picks it up

## Gotchas already hit

- Do not kill the daemon with `pkill -f jarvis`, or with any `ps | grep` whose
  pattern appears in your own command line — the shell running the command
  matches too, and kills itself (exit 144). Match on the interpreter instead:

  ```sh
  ps -eo pid,comm,args | awk '$2 ~ /^python3/ && $0 ~ /jarvisd\.py/ {print $1}' | xargs -r kill
  ```
- Plain-HTTP LAN access works, but service workers need a secure context, so
  there is no offline install that way. `tailscale serve` gives a real
  certificate and a stable hostname — the better path for the iPad later.
- Panels stretch to fill their zone, so a short list in a tall zone leaves
  space. That is intentional framing, not a layout bug.

## Suggested first moves

1. `./jarvis up`, confirm the glass renders.
2. Do one real calendar pull → `jarvis focus`. That is the whole product.
3. Have him say a few requests out loud and watch whether the `jarvis` skill
   fires. Dictation is messy — if it misses, widen the trigger phrasings in the
   skill description rather than making him phrase things carefully.
4. Only then: ports to the iPad, or the `mac-mcp` bridge when he wants phone
   voice.

Ports to other devices come after the Mac loop feels right — that was his
stated order.
