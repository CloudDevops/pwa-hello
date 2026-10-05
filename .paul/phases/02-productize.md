# Phase 02 — Productize (weeks 3–4)

This is the phase with the most real engineering, and the most for a Claude Code session to do.

---

## P1 · Move the client path off the Mac — **Claude**, needs keys ⚠️ THE BIG ONE

Blocked on: hosted-model + voice API keys. Blocks: every paying client.

**Why:** today the stack is local Ollama on the M5 Max, OpenClaw voice-call plugin on
`127.0.0.1:3334`, exposed through a Tailscale funnel. Correct for Nick, unshippable for clients.
Single points of failure all inside one house: macOS updates, reboots, ISP, power, and model
eviction. There is direct evidence — the 2026-08-20 incident where an hourly OpenClaw heartbeat
loaded an 81 GB model and drove a 128 GB machine to 20.1 GiB free, killing a running app. Ten
salons cannot share that blast radius, and the phone is the most availability-sensitive thing a
salon owns.

**Target:**

```
caller → Twilio (per-client number)
       → Cloudflare Pages Function / Worker      ← same stack as niktechai.com already
       → hosted LLM (per-client key, hard spend cap)
       → ElevenLabs TTS + hosted STT
       → client calendar API (Google / Square / Booksy / Vagaro)
       → R2 for transcripts + state (reuse infovault-blobs prefix pattern)
       → SMS summary to owner
```

**Non-negotiables:**
- Nothing in the client path touches hardware Nick owns.
- **One codebase, one YAML config per client** — not one deployment per client, or client #7 is a
  bespoke system.
- Hard per-client spend caps on every API key. An agent in a retry loop burns a month's margin in
  an afternoon.
- **Forwarding, never porting.** Clients forward busy/no-answer/after-hours to a Twilio number.
  Reversible by them in one setting — lowers the perceived risk of buying and removes the worst
  support scenario.
- **Fail open to a human.** Agent error → forward to the owner's cell. Silence on a business line
  is the one unrecoverable failure.
- Uptime monitoring with SMS alerts to Nick. Nobody will be watching.

**Reference:** `strategy/04-ops-legal-delivery.md`. Deploy with bare `npx wrangler pages deploy`
(no args — `wrangler.toml` supplies name and `pages_build_output_dir`; args skip the Functions
bundle and the R2 binding).

**Done when:** the demo number runs entirely in the cloud, the Mac is powered off, and a call
still books an appointment.

---

## P2 · The ten-call test script — **Claude**

Blocked on: P1. Blocks: selling to anyone.

Ten fixed calls, same ten every time, results kept. This is both QA and sales proof.

1. Book an appointment · 2. Reschedule · 3. Price question · 4. Hours question ·
5. Wrong number · 6. Angry caller · 7. Spanish · 8. After-hours · 9. Escalation to cell ·
10. Silence / no speech

**Done when:** all ten pass on the cloud deployment and the transcript set is saved.

---

## P3 · Deploy `/smb/` and `/ai-front-desk/` — **Claude**

Blocked on: F3 (a real demo number). Blocks: GBP, business cards, every outbound message.

```sh
grep -rn 'DEMO_NUMBER' site/     # 6 placeholders across the two pages — must be 0 before deploy
cd site && sed -i '' 's/{{DEMO_NUMBER_E164}}/+1XXXXXXXXXX/g; s/{{DEMO_NUMBER}}/(XXX) XXX-XXXX/g' \
  smb/index.html ai-front-desk/index.html
```

Then copy into the site repo's `public/` (**alongside `capability/`, wherever `build.py` treats
static pages** — if `build.py` regenerates `public/`, anything dropped in the wrong place is wiped
on the next build) and `npx wrangler pages deploy`.

Post-deploy checklist is in `site/README.md`. The one that bites:

```sh
curl -o /dev/null -w '%{http_code}\n' https://niktechai.com/nonexistent   # MUST be 404
```

Also: add both URLs to `sitemap.xml` and `llms.txt`, POST IndexNow (Bing/Yandex — Google doesn't
participate), submit in Search Console, run Rich Results Test on both, send one test contact-form
submission per page and confirm the R2 object lands under `claude/contact/<date>/`.

**Also:** the one-line nav and footer edits to the homepage, in `site/README.md`. Do **not** put
`/smb/` in the homepage hero or body copy — the homepage stays enterprise-facing.

---

## P4 · Separate Calendly event type — **Claude**

The existing `intro-call-niktech-ai` is worded for enterprise. Create an SMB one.
⚠️ **Calendly embeds are paid** — Nick's account is free and the inline/popup embed renders
"This calendar is currently unavailable." **Link out, never embed.** Both new pages already do.

---

## P5 · Business cards — **Nick orders**, Claude designs

Demo number + QR code to `/ai-front-desk/`. Blocked on F3 and F2. Needed for phase 03 walk-ins.

---

## P6 · Prospect research tool — **Claude** ✅ UNBLOCKED, START HERE

Blocked on: nothing. This is the highest-value thing a session can do before the entity exists.

Given a ZIP and a category, produce: business name · phone · website · booking tool (Square /
Booksy / Vagaro / none) · **whether calls ring out during business hours**.

That last field is the lead score and the opening line of the pitch — "I called Thursday at 2pm
and it rang out." Everything else is public data.

Output straight into `strategy/outreach/prospects.csv` (schema already defined there).

**Done when:** it produces 15 scored salons in a 2-mile radius of a given ZIP, ready to walk.
