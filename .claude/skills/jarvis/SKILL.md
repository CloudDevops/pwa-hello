---
name: jarvis
description: Render an answer to the Jarvis dashboard instead of dumping it into chat. Use whenever Nick asks to see, pull up, show, or put something on the dashboard or screen — his calendar, agenda, schedule, what's next, recent or sent email, PRs, tasks, machine or home state. Triggers on "pull up my calendar", "what's on my schedule", "show me the emails I sent", "put that on the dashboard", "what's next", and the same phrasings prefixed with "Jarvis" or "hey Jarvis". Built for voice: the spoken reply stays to one sentence and the detail goes on the glass.
---

# Jarvis dashboard

Nick drives this by voice through local Claude Code. Voice reads your chat
reply aloud, so **the reply is the headline and the dashboard is the body**.

## The loop

```
he asks → you call the connector → you curate → jarvis focus → one spoken sentence
```

The CLI is `jarvis/jarvis` from the repo root. If the daemon might be down,
`./jarvis/jarvis up --no-open` first — it is idempotent and cheap.

Anything with a round trip should claim the screen before you wait on it, so
the pause reads as work:

```sh
./jarvis/jarvis work main "querying calendar…"
```

Then replace it:

```sh
./jarvis/jarvis focus agenda '[["15:00","Toddler pickup","15m"]]' \
  -t "today · fri aug 28" -s "next in 2h 31m" -n "2 habit blocks hidden"
```

`focus` clears every other zone. That is the default — he does not want a board
full of widgets. Use `push <zone>` only when he asks for something *alongside*
what is already up.

## Curating is the job

Raw connector output is mostly noise and dumping it is the failure mode. His
calendar returns recurring habit blocks (`Sleep`, `Magnesium`, twice daily)
mixed with real appointments.

- drop recurring habit/health blocks unless he asked for them
- `muted` for anything already past — the eye should land on what is next
- `now` for what is happening right now; it draws the cyan tick
- put what you hid in `-n`, so nothing disappears silently
- keep it under ~12 rows; overflow trims to `+N more` anyway
- times in the calendar's own timezone, never UTC

## Picking a panel type

| he asks about | type | rows |
|---|---|---|
| calendar, schedule, what's next | `agenda` | `[time, title, meta?, status?]` |
| email, what I sent, inbox | `mail` | `[who, subject, time?, status?]` |
| tasks, todos, queue | `list` | `[text, meta?, status?]` |
| counts, system, at-a-glance | `metrics` | `[label, value, delta?, status?]` |
| PRs, anything columnar | `table` | header row first |
| a written answer or briefing | `text` | one string per paragraph |

Full contract in `jarvis/SCHEMA.md`; worked examples in `jarvis/RECIPES.md`.

## Speaking

One sentence, the thing he actually needs to know. Never read the list aloud —
it is already on screen.

> "Nothing until the 3pm pickup."
> "Four sent today; the one to Dana is still unanswered."

If nothing is worth saying, say almost nothing. "On screen." is a fine reply.
