# Phase 01 — Foundations (weeks 1–2)

Nothing public ships until this phase closes. Most of it is Nick's, not Claude's — Claude's job
here is to prepare, draft, compare and remind, never to file or sign.

---

## F1 · Form NikTech AI LLC — **Nick**

Blocked on: nothing. Blocks: F2, F5, everything public.

- California LLC, **through a registered agent service — not the home address.** The registered
  agent's address goes on the public Secretary of State filing, and that filing is a source
  people-search brokers scrape and you cannot opt out of.
- Get the EIN immediately after.
- Update the niktechai.com WHOIS registrant org from blank to "NikTech AI LLC".
- Change the LinkedIn company page from **Self Employed** to **Privately Held**.
- Unblocks SAM.gov registration (see memory `federal-contracting-path` — it's blocked on LLC+EIN).

⚠️ Budget the California LLC franchise tax and the Statement of Information filing. Confirm
current amounts and first-year rules with a CPA — it's the recurring cost that surprises people.

**Claude can:** compare registered-agent services on price/privacy and draft the comparison.
**Claude must not:** file, sign, or submit anything.

**Done when:** LLC number issued, EIN in hand, business bank account open (never commingle).

---

## F2 · Business address — **Nick**, Claude researches

Blocked on: F1 (or parallel). Blocks: F5, business cards, invoices.

Registered agent for the state filing + a **virtual office with mail** for anything public. Pick
the city you want to rank in (Corona/Riverside, or an OC city).

| Option | ~Cost | Google Business Profile? |
|---|---|---|
| Registered agent only | $50–150/yr | No — filing only |
| **Virtual office w/ mail** | $50–100/mo | Usually — **pick this** |
| UPS Store / CMRA box | $25–40/mo | Often rejected by Google |
| Coworking | $100–300/mo | Usually; overkill unless the desk gets used |

**Done when:** one canonical address string exists and is written into `NAP.md` (see F6).

---

## F3 · Twilio upgrade + demo number — **Nick** upgrades, **Claude** provisions

Blocked on: nothing. Blocks: site deploy, every sales conversation, the whole product.

1. Nick: upgrade the Twilio account out of trial (~$20). Trial makes callers hear a notice and
   only verified numbers get through — unusable for a demo line *and* for a client.
2. Claude: provision **two** numbers — a business line and a demo line. Point the demo line at the
   AI Front Desk so every prospect who calls hears the product before Nick says a word.
3. **Do not reuse `+1 (833) 566-1733`.** Recruiter-screening persona, wrong greeting, trial-gated.

**Done when:** a stranger can dial the demo number from an unverified phone and reach a working
greeting with no trial message.

---

## F4 · Legal pack — **Nick** (one paid hour with a small-business attorney)

Blocked on: F1. Blocks: first paying client.

Take these to the attorney, don't write them alone:

- **MSA / Services Agreement** — one page, plain English. Scope, fees, term, 30-day cancellation,
  **liability cap at fees paid in the last 12 months** (the single most important sentence),
  IP assignment on delivery, no warranty of business results.
- **Order Form / SOW** — per engagement. What's built and, more importantly, what's excluded.
- **Care Plan terms** — SLA, inclusions, what's billable.
- **Voice-AI questions:** California all-party recording consent (Pen. Code § 632) and bot
  disclosure (B&P § 17941) as they apply to an AI answering a business's phone in a cloned voice
  and quoting prices. Also: transcript retention, and whether med-spa/dental calls pull you into
  HIPAA.
- Quote **general liability + tech E&O** (~$500–1,500/yr solo). Some clients require a COI.

**Claude can:** draft first-pass versions for the attorney to mark up, and write the disclosure
line into the greeting config.

**Done when:** three signed-off templates exist and E&O is bound.

---

## F5 · Local listings — **Claude drafts, Nick submits.** BLOCKED until F1+F2+F3

Do not start any of this early. A listing published with the home address or personal phone
re-seeds exactly what `wiki/privacy-exposure-cleanup.md` is removing, from an authoritative
source, permanently.

Order of value:
1. **Google Business Profile** — service-area business, **address hidden**, service areas matching
   the site's existing `areaServed` JSON-LD (Orange County, Greater LA, San Diego, Inland Empire).
2. Bing Places · 3. Apple Business Connect · 4. Yelp · 5. Nextdoor Business ·
6. Corona/Riverside Chamber · 7. Alignable / BNI (test one at a time) ·
8. yellowpages.com last, for completeness, expecting nothing.

**Done when:** GBP verified and published with 10+ photos, services with prices, and weekly posts
scheduled for the first month.

---

## F6 · NAP canonical file — **Claude**

Blocked on: F1, F2, F3.

Create `NAP.md` holding the exact name, address and phone strings, byte-identical. Copy-paste
from it for every listing, forever. Inconsistent NAP is the most common reason local rankings
stall, and fixing it later resets trust signals.

---

## F7 · Publish the four queued blog drafts — **Nick reviews, Claude deploys**

Blocked on: Nick's review only. Unrelated to the SMB line but it's free authority and the writing
already exists.

Queued in `content/blog/` with `status: draft`:
`five-rungs-of-agent-engineering` · `capability-urls-vs-oauth-mcp` · `fail-closed-agent-tools` ·
`zero-credential-workers`

Flip `status: published`, rebuild, deploy, then:

```sh
curl -o /dev/null -w '%{http_code}\n' https://niktechai.com/nonexistent   # MUST be 404, not 200
```

**Done when:** four posts live, sitemap and `llms.txt` regenerated, IndexNow POSTed, 404 verified.
