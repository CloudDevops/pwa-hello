# Operations, legal, and delivery

## ⚠️ The architecture change that has to happen first

Your AI phone stack currently runs on the M5 Max in your house: local Ollama, OpenClaw voice-call
plugin on `127.0.0.1:3334`, exposed through a Tailscale funnel, with ElevenLabs for voice.

**This is correct for you and unshippable for clients.** Single points of failure, all in your home:

- macOS updates and reboots.
- Model eviction and OOM — you have direct evidence, the 2026-08-20 incident where an hourly
  heartbeat loading an 81 GB model drove free RAM to 20 GiB and killed a running app.
- Tailscale funnel availability, ISP outage, power outage.
- One machine serving every client — one bad afternoon takes down ten businesses' phone lines
  simultaneously, and you find out from voicemails.

You cannot sell a business's *phone line* on that. The phone is the most availability-sensitive thing
a salon owns.

### Target architecture for client deployments

```
Customer dials the business's published number
        │
        ▼
  Twilio (per-client number, or forward from their existing line)
        │  webhook
        ▼
  Cloudflare Worker / Pages Function          ← you already run this stack for niktechai.com
        │
        ├── LLM: hosted API (frontier model), per-client key, hard spend cap
        ├── TTS/STT: ElevenLabs + hosted STT
        ├── Calendar: client's Google/Square/booking API
        └── State + transcripts: R2 (you already run R2 with per-prefix layout)
        │
        ▼
  SMS summary to owner + transcript in R2
```

Rules:
- **Nothing in the client path touches hardware you own.** Your Mac is a dev box, not infrastructure.
- **One config file per client**, not one deployment per client. Same code, different config —
  otherwise client #7 is a bespoke system and you have seven things to maintain.
- **Hard per-client spend caps** on every AI API key. An agent in a retry loop can burn a month's
  margin in an afternoon.
- **Forwarding, not porting.** Never port a client's main number to you. Have them forward
  (busy/no-answer/after-hours) to a Twilio number you control. Reversible in one setting change by
  them, which lowers the perceived risk of buying and removes your worst support scenario.
- **Fail open to a human.** If the agent errors, forward to the owner's cell. Silence on a business
  phone line is the one unrecoverable failure.
- **Uptime monitoring with SMS alerts to you.** You will not be watching. Something has to be.

---

## Legal and compliance

Not legal advice — this is the list to take to a small-business attorney for one paid hour. Worth it.

### Entity and money
- **NikTech AI LLC** (California) + EIN. See `03-identity-and-privacy.md`.
- Business bank account. Never commingle — it's the fastest way to lose the liability protection you
  just paid for.
- **General liability + E&O (professional liability / tech E&O).** ~$500–1,500/yr for a solo. Some
  larger clients will require a certificate before they sign anything.
- Stripe or similar for recurring billing. Recurring revenue you have to invoice manually is
  recurring revenue you will eventually stop collecting.

### Voice-AI specific — read this before the first client call is answered
- **California is an all-party consent state for call recording** (Penal Code § 632). If you store
  recordings or transcripts, the caller has to be told at the start of the call. Put a disclosure
  line in the greeting.
- **Bot disclosure.** California's bot statute (B&P § 17941) requires disclosure when a bot
  communicates with a person to incentivize a sale. An AI receptionist quoting prices and booking
  services is squarely in scope. Disclose in the greeting regardless — you already flagged this
  instinct in your voice config, now make it a product requirement rather than a note.
- **Say "assistant," not a fake human name.** Your cloned voice makes this more important, not less.
  A caller who realizes they were deceived about talking to a person is a complaint, a review, and
  possibly a legal problem.
- **Data handling.** Transcripts contain customer names, phone numbers, and sometimes health-adjacent
  detail (med spas). Encrypt at rest, set a retention window (30–90 days, then delete), say so in the
  contract. Do not train anything on client data.
- **Med spas, dental, anything clinical: HIPAA may apply.** If a caller says why they're booking, you
  may be touching PHI. Either scope those clients out at first, or get a BAA and treat it properly.
  You've handled PHI rules before under BD — apply the same caution.

### Contracts (three documents, that's all)
1. **MSA / Services Agreement** — one page, plain English. Scope, fees, term, 30-day cancellation,
   liability cap at fees paid, IP assignment on delivery, no warranty of specific business results.
2. **Order Form / SOW** — per engagement. What's built, what's excluded, price, dates. *Excluded* is
   the important half.
3. **Care Plan terms** — SLA, what's included, what's billable.

Write them once, reuse forever. A liability cap at "fees paid in the last 12 months" is the single
most important sentence in the whole set.

---

## Delivery SOP — AI Front Desk (target: ≤4 hours per client)

Time it on client #1 and cut it every time after. If it stays a weekend, the business doesn't scale.

1. **Intake form** (before install): hours, services, prices, FAQs, booking tool, owner's cell,
   greeting preference, escalation rules. *Never* gather this on a call — the form is what makes the
   install repeatable.
2. **Provision:** Twilio number, config file from template, calendar credentials.
3. **Voice:** pick a stock voice (Standard) or record 2 minutes for a clone (Pro).
4. **Test script:** 10 fixed calls — book, reschedule, price question, hours question, wrong-number,
   angry caller, Spanish, after-hours, escalation, silence. Same 10 every time. Keep the results.
5. **Forwarding setup with the owner** on the phone — 5 minutes, their carrier settings.
6. **Handoff:** one-page "how it works," the summary-SMS format, how to reach you, how to turn it off.
7. **Day 3 and Day 14 check-in emails.** Templated. Day 14 is where you ask for the review and the
   referral, while it's still novel and they're still delighted.

---

## What to automate for yourself, early

You have the skills to over-build this. Don't — but these four pay for themselves fast:

- **Client config as code.** One repo, one YAML per client, deploy from CI. This is the difference
  between 5 clients and 30.
- **Intake → config generator.** Form submission produces a draft config. Cuts the install in half.
- **Weekly automated health report** per client, emailed to you: call volume, error rate, spend.
  Catches problems before the client does, and it's a Pro-tier feature you can sell.
- **Prospect research agent.** Given a ZIP and a category, produce name / phone / website / booking
  tool / whether calls go to voicemail during business hours. That last field is your lead score, and
  it's testable from a phone. This is the one piece of custom software worth building for yourself
  before you build any for a client.
