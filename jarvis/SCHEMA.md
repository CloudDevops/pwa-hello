# Panel schema

The contract between the model and the two renderers (`panels.py` for the
terminal, `web/app.js` for the glass). The design goal is that a fully styled
panel costs a few dozen tokens to write, so presentation never sits in the
generation path.

## State

```json
{ "v": 1, "ts": 1756400000.0,
  "zones": { "status": <panel|null>, "main": <panel|null>,
             "side": <panel|null>, "rail": <panel|null> } }
```

Four zones, fixed. On screen they lay out as:

```
┌───────────────────────────────┐
│ status  (full-width strip)    │
├──────────────────┬────────────┤
│ main             │ side       │
├──────────────────┴────────────┤
│ rail                          │
└───────────────────────────────┘
```

Below 900px wide they stack in the same order.

## Panel

Only `type` is required.

| field    | default    | notes                                              |
|----------|------------|----------------------------------------------------|
| `type`   | —          | `agenda` `list` `mail` `metrics` `table` `log` `text` |
| `title`  | `""`       | rendered uppercase                                  |
| `sub`    | rel. time  | right side of the header — good for freshness       |
| `note`   | `""`       | small footer line                                   |
| `state`  | `ok`       | `ok` `working` `stale` `error`                      |
| `accent` | `cyan`     | `cyan` `amber` `green` `red` `violet`               |
| `items`  | `[]`       | rows, shape depends on `type`                       |
| `ts`     | now        | set by the daemon when absent                       |

## Rows

Rows are positional arrays — that is what keeps them cheap to emit. Trailing
fields are optional, so `["09:00","Standup"]` is valid.

| type      | row                                    |
|-----------|----------------------------------------|
| `agenda`  | `[time, title, meta?, status?]`        |
| `mail`    | `[from, subject, time?, status?]`      |
| `log`     | `[time, text, status?]`                |
| `list`    | `[text, meta?, status?]`               |
| `metrics` | `[label, value, delta?, status?]`      |
| `table`   | first row is the header, rest are body |
| `text`    | `[paragraph]`, or a bare string        |

`status` tints the row: `ok` `now` `warn` `crit` `muted`. `now` also draws the
cyan tick in the left gutter — use it for the thing happening right now.

Objects work too, when writing by hand beats writing tersely:
`{"time":"09:00","title":"Standup","status":"muted"}`.

## Overflow

Panels never scroll. Rows that do not fit are hidden and replaced by a
`+N more` line. Send what matters first; the renderer handles the cut.

## Adding a panel type

Touch three places, or the two renderers drift:

1. `panels.py` — add to `PANEL_TYPES`, then handle it in `_rows_for`
2. `web/app.js` — handle it in `bodyNodes` (and `LAYOUT` if it is row-shaped)
3. this table
