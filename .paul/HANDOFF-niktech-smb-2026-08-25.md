# HANDOFF — niktech-smb — 2026-08-25

**Topic slug:** `niktech-smb` · **From:** cloud session on `CloudDevops/pwa-hello`,
branch `claude/creator-ai-services-strategy-su5htj` · **To:** a local Claude Code session on the
hub Mac.

---

## Read this first

Nick asked for thoughts on entering the creator economy and selling AI services to small
businesses, then asked for a handoff because he wants the work **done in a real session with
tools**, not read as a document.

**Planning is complete. Execution has not started.** Everything below is written down; nothing
below has been done.

Read in this order and you'll have the whole picture in about five minutes:
`PROJECT.md` (decisions + guardrails) → `STATE.md` (where we are, what's blocked) →
`ROADMAP.md` → the phase file you're working.

Full reasoning, if you need the *why* behind a decision, is in `strategy/` — start at
`strategy/00-assessment.md`. **Don't re-derive it.** If something looks wrong, say so in one line
and carry on.

---

## The three calls that shape everything

1. **The product already exists.** The Twilio → agent → ElevenLabs-cloned-voice phone stack
   running on the hub Mac is the business. Productize it as a monthly subscription for
   appointment-based local businesses. Custom builds are the upsell, never the wedge.
2. **Business identity before any public listing.** Directory listings republish name + address +
   phone and the aggregators scrape each other. Listing now re-seeds the exact records
   `wiki/privacy-exposure-cleanup.md` is removing. LLC → registered agent → business address →
   business phone, *then* Google Business Profile with the address hidden.
3. **The toddler-video channel is dead as a business line.** COPPA "Made for Kids" disables
   personalized ads, comments and notifications; no contactable audience, no funnel, compounds
   with nothing. The creator play is the engineering notes plus filming the installs — and now X.

---

## What already exists

| Artifact | Where |
|---|---|
| Full strategy, 8 docs | `strategy/` |
| Outreach templates, call script, prospect tracker | `strategy/outreach/` |
| Drop-in `/smb/` + `/ai-front-desk/` pages | `site/` — validated, rendered, **placeholders unresolved** |
| Draft PR | https://github.com/CloudDevops/pwa-hello/pull/1 |
| Read-only summary for Nick | https://claude.ai/code/artifact/2767930f-d6d9-4b0f-8581-b5e0a9104bcc |
| This state layer | `.paul/` |

---

## Start here — pick one, all unblocked tonight

None of these need the LLC, a business phone, or a client.

**A · Prospect research tool** — `phases/02-productize.md` P6
Given a ZIP and a category, emit name · phone · website · booking tool · **whether calls ring out
during business hours**. That last column is both the lead score and the opening line of the pitch
("I called Thursday at 2pm and it rang out"). Writes into `strategy/outreach/prospects.csv`, whose
schema is already defined. Done when it produces 15 scored salons in a 2-mile radius of a ZIP.

**B · X profile + 20-post queue** — `phases/04-distribution.md` X1 and X3
Nick has never posted on X and wants to. Draft three bio variants and the pinned post, crop the
existing banner, then build `strategy/outreach/x-queue.md` from the vault's `⚠️` gotcha blocks —
they are pre-written posts and they're his unfair advantage. Read the expectation-setting at the
top of that phase file before starting: **X serves the enterprise and creator lines, not the SMB
beachhead.** Don't let it eat Saturdays that belong to doors.

**C · Record the first demo clip**
30 seconds of the AI Front Desk handling a real scenario — book, reschedule, Spanish, angry
caller. It's the single strongest thing he can post and the single strongest thing he can hand a
salon owner. As a *post* it doesn't need the cloud migration first, so it's available tonight.

**D · The cloud migration** — `phases/02-productize.md` P1
The biggest engineering item and the one that gates every paying client. Needs hosted-model and
voice API keys, so confirm with Nick before starting.

---

## Hard rules — read `PROJECT.md` guardrails in full before touching anything public

- Never publish the home address or personal phone. City-level "Corona, California" only.
- Never use `+1 (833) 566-1733` — recruiter-screening persona, still trial-gated.
- Never publish a draft, page or listing without Nick's review.
- Never name a client. Never claim a clearance.
- No AI attribution on anything client-facing (`niktechai-site`, PRs, docs, artifacts).
- Never sell a phone line that depends on hardware in Nick's house.
- Legal, tax and entity work is a recommendation, never an action.

---

## Path resolution — do this before assuming anything

`labs/` moved out of the vault on 2026-07-28 and the memories disagree on where it landed:

```sh
~/.claude/hook-state/resolve-handoff.sh --list
ls -d ~/projects/labs/niktechai-site ~/Info_vault/labs/niktechai-site 2>/dev/null
```

Site deploys use bare `npx wrangler pages deploy` — no args, or the Functions bundle and the R2
binding are skipped.

---

## Register the topic slug (one-time, ~10 seconds)

Not done from the cloud session — there's no shell on the public MCP tier.

```sh
echo "$HOME/projects/pwa-hello" > ~/.claude/hook-state/topics/niktech-smb.txt   # adjust to the real clone path
~/.claude/hook-state/resolve-handoff.sh niktech-smb                             # verify it resolves
```

Then `.paul/` is picked up automatically by the `~/bin/claude-paul-context` SessionStart hook —
`STATE.md` and this handoff are injected on every new session, clear and compact. **Don't ask Nick
to run `/paul:resume`; just follow the injected state.**

---

## Open questions for Nick

1. **Which city for the business address?** It's a local-SEO ranking input, not just a mailing
   detail. Corona/Riverside is closest; an Orange County address ranks against a wealthier market.
2. **Demo number area code** — 951 (Inland Empire, matches the beachhead) or 949/714 (OC)?
3. **Hosted model for the client voice path** — needed before the cloud migration can start.
4. **Does the founding-client free-setup offer stand at three**, or fewer if the first one closes
   easily?
