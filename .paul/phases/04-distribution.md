# Phase 04 — Distribution: X, LinkedIn and the channel mix

Added 2026-08-25 at Nick's request: he's seen people — including teenagers — post services on X
and get inquiries, wants to use it for reach and posting, and has never posted there before.

---

## ⚠️ Set the expectation first, or this phase wastes a month

**X will not get you salon clients.** Your beachhead is appointment businesses within a 2-mile
radius of Corona. Those owners are not on X, and a viral post in Bangalore is worth zero bookings
in the Inland Empire. Local SMB clients come from doors, Google Business Profile and referrals —
that ordering does not change.

**What X is genuinely good for, for you:**
- **Enterprise and contract leads.** Founders, CTOs and AI-team leads do live there, and they hire
  forward-deployed engineers.
- **Credibility that arrives before you do.** Same job as the blog — it exists when someone
  searches your name after an outbound message or an interview.
- **The creator track.** The AI-engineering audience is real, active and reachable there in a way
  it isn't on LinkedIn.
- **Recruiter reach**, which matters given the job pipeline.

**And the honest read on the posts you've seen:** the kid who posted a service and got inquiries
is the one you saw. Thousands posted the same thing into silence. The difference is almost never
the offer — it's that the ones that travel **show a working thing**, not a service. "I build AI
agents for small businesses, DM me" gets nothing. **A 30-second screen recording of an AI
answering a salon's phone in a cloned voice, booking an appointment** gets replies, because it's
a thing that happened rather than a claim.

You have that video. Nobody else posting "AI consultant" does. That's the whole strategy.

---

## X1 · Account setup — **Nick**, Claude drafts

Blocked on: nothing. This is doable tonight.

- **Post from a personal account with your real name**, not a company handle. Company accounts
  with zero followers get zero reach; people follow people. Same reasoning as the LinkedIn launch
  post going out from your profile rather than the company page — that worked, and it worked for
  this reason.
- **The profile is a landing page**, not a bio. Three lines: what you do, who for, and the proof.
  Pin a post, not a link.
  - Name: `Nick Harinath`
  - Bio: what you actually ship — production AI agents against real enterprise data — plus the
    fifteen years of infrastructure under it, and Corona/SoCal.
  - Link: `niktechai.com`
  - Header: reuse `labs/niktechai-site/brand/banner.png` (1128×191 crops fine).
- ⚠️ **Privacy:** no street address, no personal phone, and location no finer than "SoCal". Same
  rule as everywhere else — see `PROJECT.md` guardrails.

**Claude can:** draft three bio variants and the pinned post.
**Done when:** profile complete, header up, one pinned post live.

---

## X2 · The first 30 days: reply-first, not post-first — **Nick**

The mistake every new account makes is posting into a void. A zero-follower account's posts are
seen by nobody; **replies are seen by everyone reading the original post.** So invert it.

**Daily, ~20 minutes, weekday evenings:**
- **5 replies** to people with real audiences in your lane — AI engineering, agents, MCP, Azure
  AI, devops. Reply with something only you could say: a gotcha you hit, a measurement you took,
  a correction. Never "great post."
- **1 post** of your own, from the queue (X3).

**Do not:** buy followers, use engagement pods, post threads of generic advice, or open with
"Most people don't realize…". That register is instantly recognizable and it costs credibility
with exactly the audience you want.

**Measure replies and profile visits, not follows.** Follows are a lagging vanity number; a DM
from someone with a budget is the actual outcome.

---

## X3 · The post queue — **Claude builds it**

Blocked on: nothing. **Fully executable in a local session right now.**

Create `strategy/outreach/x-queue.md` — 20 posts drawn from material that already exists, so the
queue never depends on Nick finding time to think of something.

**Four post types that work for you, in order of strength:**

1. **The demo.** Screen recording or call audio of the AI Front Desk handling a real scenario.
   Book, reschedule, angry caller, Spanish. One clip, one sentence of context, no thread.
   *This is the strongest thing you can post and you already have the system to make it.*
2. **The gotcha.** Straight from the vault's `⚠️` blocks — the failure, the evidence, the root
   cause, the fix. These are already written. Examples sitting unused right now:
   - An hourly agent heartbeat silently loading an 81 GB model and OOM-ing a 128 GB Mac, with the
     log trail that proved it
   - Cloudflare Pages returning HTTP 200 for every nonexistent URL because the project had no
     `404.html` — a soft-404 that would have let Google index unlimited duplicates
   - Pages `_redirects` matching paths, not hostnames, so the Netlify-style www→apex line silently
     does nothing
   - A voice agent whose TwiML pointed at a `wss://` route never exposed through the funnel, so
     every answered call would have died silently
   - ElevenLabs output sounding "robotic" tracing to the *model choice*, not the voice clone
3. **Build in public.** "Day 12 of turning my AI phone agent into a product for local salons.
   Here's what broke today." Numbers, screenshots, failures included. Failures outperform wins.
4. **The counter-take**, sparingly. You have earned exactly one category of these: what actually
   kills AI pilots in enterprises, from having been in the room. Don't spend it on generic
   contrarianism.

**Rules for the queue:**
- One idea per post. No threads until something of yours has actually travelled.
- Lead with the specific: the error string, the number, the clip. Never the lesson.
- No hashtags. No "🧵". No engagement bait.
- **Never name a client** — "a global beverage manufacturer", "a materials manufacturer".
- Never post client call audio, even anonymized, without written consent.

**Done when:** 20 drafted posts exist in the queue with types tagged, ready to pull one a day.

---

## X4 · Write once, adapt everywhere — **Claude**

Blocked on: X3.

Every gotcha is already a blog post. Make it a post everywhere without writing it four times:

| Channel | Adaptation | Why |
|---|---|---|
| **Blog** (`content/blog/*.md`) | The full piece | The canonical, indexable version — and the GEO play |
| **LinkedIn** | Opening paragraph + "full write-up on the site" | Where his network actually is; proven |
| **X** | The single sharpest sentence + the screenshot | Different register, different audience |
| **YouTube / Shorts** | The install footage, 2–5 min | Doubles as SMB sales collateral |

The blog is the source of truth; the others are cuts of it. `~/.claude/skills/niktechai-content/`
already encodes the publish pipeline, GEO invariants and voice — extend it with the X register
rather than writing a second set of rules.

---

## X5 · The other channels, ranked honestly — **Nick**

He asked to use all channels. They are not equal, so here's the ordering rather than a list:

| Channel | Serves | Effort | Verdict |
|---|---|---|---|
| **Doors + Google Business Profile** | SMB clients | Saturdays | **The business.** Everything else is secondary |
| **LinkedIn (personal profile)** | Enterprise, recruiters | Low — already working | Keep. Highest ROI of the social channels |
| **X (personal account)** | Enterprise, creator, recruiters | 20 min/evening | **New. Worth it — with the demo video, not without** |
| **Nextdoor Business** | SMB clients, local | Very low | Do it. The actual "neighborhood" channel |
| **YouTube (install series)** | Both lines + credibility | High | Only after 3 paying clients |
| **Reddit** (r/smallbusiness, local subs) | SMB clients | Medium | ⚠️ Self-promo gets you banned. Answer questions for a month before mentioning anything you sell |
| **Instagram / TikTok** | SMB clients, local | High | Salon owners *are* here — but it's a full content job. Not before the business works |
| **Facebook local groups** | SMB clients, local | Low | Worth one test. Corona/Riverside business groups |

**Sequencing rule:** X and Nextdoor now (both cheap). Reddit only with the month of goodwill
first. YouTube and Instagram after revenue exists. Do not add a channel while an earlier one is
un-worked.

---

## What a local session can execute right now, unblocked

1. Draft the X profile: three bio variants, the pinned post, and crop the banner. **(X1)**
2. Build `strategy/outreach/x-queue.md` — 20 posts from the vault's existing `⚠️` blocks and the
   build-in-public angle, types tagged, ready to pull one a day. **(X3)**
3. Extend `~/.claude/skills/niktechai-content/` with the X register and the write-once/adapt-
   everywhere matrix. **(X4)**
4. Record the first demo clip against the current voice stack — even on the Mac, even before the
   cloud migration. It's a post, not a product, so the availability constraint doesn't apply yet.

None of these need the LLC, the business phone or a client. All four are doable in one evening.
