# Recipes

How a spoken request becomes a panel. The pattern is always the same:

```
you ask → Claude calls the connector it already has → curates → jarvis focus
```

There is no fetcher daemon and no OAuth setup in this repo, because Claude
already holds the Google/Gmail/Superhuman connectors. The model *is* the data
feed. That is what makes this reactive rather than ambient.

## Curation is the point

Raw connector output is mostly noise. A real calendar pull returns recurring
habit blocks (`Sleep`, `Magnesium`) alongside actual appointments; a raw dump
of it is exactly the clutter a dashboard should not have. So every recipe ends
with judgement, not just a transform:

- drop recurring habit/health blocks unless they are what was asked for
- `muted` anything already past, so the eye lands on what is next
- `now` for the one thing happening right now — it draws the cyan tick
- put the count of what you hid in `note`, so nothing vanishes silently
- keep it under ~12 rows; the panel trims the rest to `+N more`

## Calendar

> "pull up my calendar"

`Google_Calendar.list_events` with `orderBy: startTime`, then:

```sh
jarvis focus agenda '[["09:30","Toddler drop-off","1h","muted"],
                      ["15:00","Toddler pickup","15m"]]' \
  -t "today · fri aug 28" -s "next in 2h 31m" \
  -n "2 recurring habit blocks hidden"
```

Times in the calendar's own timezone, not UTC — `list_events` returns both.

## Sent mail

> "what did I send today"

`Gmail.search_threads` with `in:sent newer_than:1d`, then:

```sh
jarvis focus mail '[["dana@acme.co","Re: rollout plan","2m"],
                    ["ops@acme.co","Postmortem draft","1h","muted"]]' \
  -t "sent today" -a violet
```

Recipient in the lead column for sent mail, sender for received.

## Slow calls

Anything with a round trip should claim the screen first, so the wait reads as
work rather than nothing happening:

```sh
jarvis work main "querying calendar…"   # then the focus push replaces it
```

## Speak the headline, render the body

Voice that reads a list aloud is painful. Say one sentence and let the panel
carry the detail:

> spoken: "Nothing until the 3pm pickup."
> on screen: the full agenda, past items dimmed

## Adding a recipe

Recipes are prompt-level, not code — there is nothing to register. If you find
yourself formatting the same shape twice, that is the signal to add a panel
type in `SCHEMA.md` instead.
