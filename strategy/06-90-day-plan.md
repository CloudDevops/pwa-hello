# 90-day plan

Assumes ~10 hours a week: weekday evenings plus one weekend morning. Everything is sized to that.

**One success metric at day 90: $1,000+ MRR from 3+ paying clients.** Not leads, not revenue, not
followers. MRR.

---

## Weeks 1–2 — foundations (nothing public yet)

The whole point of these two weeks is that you can list, sell and invoice without exposing your home
address or your personal phone.

- [ ] **Form NikTech AI LLC** (California) via a registered agent — *not* your home address. Get the EIN.
- [ ] **Business address** — registered agent for the filing + a virtual office in Corona/Riverside or OC
      for anything public. Pick the city you want to rank in.
- [ ] **Business bank account.** Never commingle.
- [ ] **Upgrade Twilio out of trial** (~$20). Prerequisite for both the demo line and any client.
- [ ] **Provision the business/demo number.** Point your own AI Front Desk at it — every prospect who
      calls you gets the demo before you speak.
- [ ] **Write the canonical NAP string** (name / address / phone) into one file. Copy-paste it everywhere, forever.
- [ ] One paid hour with a small-business attorney: MSA, SOW, Care Plan terms, and the voice-AI
      disclosure/recording questions in `04-ops-legal-delivery.md`.
- [ ] Quote general liability + tech E&O.
- [ ] **Publish the four queued blog drafts.** They're written. Flip `status: published`, rebuild, deploy.
      Then re-verify the 404: `curl -o /dev/null -w '%{http_code}' https://niktechai.com/nonexistent` → must be 404.

## Weeks 3–4 — the product becomes shippable

- [ ] **Move the phone stack off your Mac.** Cloudflare Worker/Pages Function + Twilio + hosted LLM +
      ElevenLabs + R2. No client path may touch hardware in your house. (`04-ops-legal-delivery.md`)
- [ ] Per-client YAML config; one deployment, many configs.
- [ ] Hard spend caps on every API key. Uptime monitoring with SMS alerts to you.
- [ ] Fail-open: agent error → forward to owner's cell.
- [ ] Build the **10-call test script**. Run it. Keep the results — it's your QA and your proof.
- [ ] Deploy **`/smb/` and `/ai-front-desk/`** to niktechai.com (`site/` in this repo — files are ready).
- [ ] **Google Business Profile** — service-area business, address hidden, service areas matching the
      site's `areaServed`. Then Bing Places, Apple Business Connect, Yelp, Nextdoor.
- [ ] Order business cards with the demo number + QR code.
- [ ] **Lunch with your dealership-IT friend.** Referral arrangement both ways, and ask for his playbook.

## Weeks 5–8 — first clients

- [ ] **Four consecutive Saturdays of walk-ins.** 15 doors each. Don't judge the channel before week 4.
- [ ] Friday evenings: ring-out test on next week's list. Log who doesn't answer — that's your lead score.
- [ ] Weekday evenings: 20 cold emails + follow-up calls per session (`outreach/email-templates.md`).
- [ ] **Founding-client offer: free setup for the first three**, in exchange for a testimonial and two
      referral intros. Say out loud that it ends — so it doesn't become your price.
- [ ] Install client #1. **Time the install.** Cut it every time after.
- [ ] Day 3 and day 14 check-ins. Ask for the Google review and the referrals at day 14.
- [ ] Film the first install (anonymized) — SMB proof and enterprise proof from the same footage.

**Gate at week 8:** if you haven't had 3+ real conversations, the *message* is wrong, not the volume.
Rewrite it before sending more.

## Weeks 9–12 — repeat and tighten

- [ ] Clients #2 and #3. Same install, faster.
- [ ] **First case study with a number in it.** Calls answered, appointments booked, in a month.
- [ ] 60-second phone-video testimonial from the happiest client.
- [ ] Raise the price: founding rate ends, setup fee goes live at $995.
- [ ] Publish one post every two weeks from the vault backlog; one LinkedIn post a week.
- [ ] Automate: intake form → draft config; weekly per-client health report to yourself.
- [ ] First **AI Audit** sold at $750 to a prospect who isn't ready for the Front Desk.
- [ ] Quarterly data-broker opt-out sweep (it's recurring, not one-shot).

---

## Decision points

| When | Question | If yes | If no |
|---|---|---|---|
| Week 8 | 3+ real conversations from walk-ins? | Keep walking | Rewrite the pitch, not the volume |
| Week 12 | 3 paying clients? | Scale the same motion | Change the *vertical*, keep the product |
| Week 12 | Install under 4 hours? | Take more clients | Fix the SOP before selling more |
| Month 6 | 5+ SMB clients? | Consider a separate SMB brand | Keep it all on niktechai.com |
| Month 6 | Custom builds outselling the Front Desk? | Re-read `01-offers-and-pricing.md` — that's the trap | — |

## Sequencing rules

1. **LLC + address + phone before any public listing.** Non-negotiable, given the broker cleanup.
2. **Cloud architecture before the first paying client.** Never sell a phone line that runs on your Mac.
3. **Outbound before SEO.** SEO is the credibility backstop, not the pipeline.
4. **One vertical until it's boring.** Boring means repeatable, and repeatable is the whole business.
5. **Recurring before one-off.** Custom builds are the upsell, never the wedge.
6. **No video content until three clients are paying.**
