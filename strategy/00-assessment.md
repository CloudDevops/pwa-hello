# Assessment — creator economy + AI services for small business

Written 2026-08-25. Opinionated on purpose. Read `06-90-day-plan.md` if you only want the actions.

---

## The short version

1. **You already built the best SMB product you could sell, and you built it for yourself.** The
   Twilio → agent → ElevenLabs cloned-voice phone line is a recurring-revenue product that
   appointment-based local businesses will pay for every month. Everything else on your list is
   worse than this one. Lead with it.
2. **Don't sell "vibe coding."** Nobody buys a methodology. Custom software as the *lead* offer is
   the trap in this plan — it is one-off revenue with unbounded support liability, and you have a
   full-time Microsoft contract. Sell one repeatable thing, then sell custom work to people who
   already pay you.
3. **The toddler-video channel is the weakest item on the list.** Not because it can't work, but
   because it compounds with nothing else you're doing. Kill it as a business. `05-creator-track.md`
   has the version that does compound.
4. **"Register in the Yellow Book" collides head-on with the data-broker scrub you started today.**
   Directory listings republish name + address + phone — the exact records you are paying to remove.
   This is solvable, but it has to be solved *before* the first listing, not after.
   See `03-identity-and-privacy.md`.
5. **One brand, one domain, two front doors.** Keep niktechai.com. Add `/smb/`. Do not build a
   second site until the SMB line has five paying clients.

---

## The constraint everything else has to bend around

You have a full-time contract (Microsoft/Milliken, weekdays, work hours). A salon owner calls at
11:20am on a Tuesday. You cannot answer. You cannot do a 2pm site visit. You cannot run a discovery
call series.

This is not a small problem — it is *the* problem, and it disqualifies most of the obvious
small-business service models:

| Model | Needs daytime you? | Verdict |
|---|---|---|
| Break/fix IT, on-site support | Constantly | ❌ Can't do it |
| Ongoing "AI consulting" retainers | Meetings in business hours | ❌ Can't do it |
| Custom software projects | Discovery + revisions + support | ⚠️ Only for existing clients, fixed scope |
| **Install-once product with a monthly fee** | Evenings/weekends to install, then it runs itself | ✅ **This one** |

So the filter for every offer is: **can it be sold in one evening call, installed on a weekend, and
then run without you?** If not, it doesn't go on the menu yet.

The good news: your day job is the asset, not just the constraint. "The engineer who ships AI agents
for Microsoft's enterprise clients" is an absurdly strong credential in front of a salon owner. It
is worth more there than it is in the enterprise market, where everyone has it.

---

## Positioning: keep the credential, lose the "neighborhood AI guy" framing

I like the instinct — local, approachable, one-stop. I don't like it as a *brand*, because
"neighborhood AI guy" gets priced like a handyman. You'd be competing on being nearby, which is the
one thing that can't be defended and doesn't pay.

Put the warmth in the copy, not the brand:

> **Brand:** NikTech AI. Same as enterprise.
> **Line:** "I build AI systems for Microsoft's enterprise clients. I also build them for the
> businesses on Main Street — same engineering, smaller bill."

That sentence does three jobs at once: credibility, locality, and price framing. "Neighborhood AI
guy" does one, badly.

**Where the local-ness lives:** in the *offer* and the *SEO*, not the identity. "AI phone answering
for salons in the Inland Empire" is a winnable search and a specific pitch. "Neighborhood AI guy" is
neither.

---

## The three things you listed, ranked

### 1. AI Front Desk — the phone agent (BUILD AND SELL THIS)

You already have every piece running: Twilio number, webhook, agent brain, ElevenLabs voice clone,
calendar awareness, a working call in production on 2026-08-24.

Why it beats everything else:
- **Recurring.** $299–$499/mo, not a one-time $4k that you have to re-earn next month.
- **Identical every time.** Client #7 is the same install as client #2. That is the only way a
  solo operator with a day job scales.
- **Demonstrable in 30 seconds.** You don't pitch it — you give them a number and tell them to call
  it from the parking lot. No deck, no proposal, no second meeting. That is a one-evening sale.
- **The pain is measurable by the prospect, not by you.** Ask any salon owner "how many calls do you
  miss while you're with a client?" They know the number. They've been annoyed by it for years.
  You never have to create the urgency.
- **It fails safe.** Worst case, a call is handled awkwardly. Compare to custom software, where worst
  case is their booking system is down on a Saturday and it's your fault.

⚠️ **The one architectural thing you must change before selling it:** it currently runs on your Mac,
through a Tailscale funnel, on local Ollama. That is fine for you and catastrophic for clients — an
OOM, a reboot, or a macOS update takes ten businesses' phone lines down at once, and you'd find out
from an angry voicemail. You already have direct evidence of this failure mode (the 2026-08-20
heartbeat OOM). **Client deployments must be cloud-hosted with no dependency on hardware in your
house.** Architecture in `04-ops-legal-delivery.md`.

### 2. Agent setup + custom builds (SELL SECOND, TO EXISTING CLIENTS)

OpenClaw/Hermes installs, automation, small custom tools. Real demand, real money, but:
- Every one is different → no leverage.
- The buyer can't judge the work → the sale is long and trust-heavy.
- You inherit maintenance forever unless the contract says otherwise.

Make this the *upsell*, not the wedge. A client already paying you $399/mo will buy a $4,000 build
after one conversation. A stranger will need four.

**Rules for custom work:** fixed scope, fixed price, written scope doc, source handed over, 30-day
warranty, then a care plan or nothing. Never hourly, never open-ended.

### 3. Toddler YouTube channel (KILL AS A BUSINESS)

The honest math:
- Channels marked **"Made for Kids"** (which yours would be, by law) have **personalized ads
  disabled** under COPPA. That removes the highest-value ad inventory — the RPM is structurally
  lower than any other category, and it is not a thing you can optimize your way out of.
- Comments are disabled. No community, no feedback loop, no audience you can ever contact.
- No funnel. A three-year-old cannot hire you. The audience has zero overlap with anyone who buys
  anything from you. It is the only item on your list that doesn't feed the others.
- The competition is industrialized studios with staff animators shipping daily, plus a flood of
  AI-generated kids' content that YouTube has been actively demonetizing as low-effort.
- You'd be spending your scarcest resource — evenings and weekends, the exact hours the SMB business
  needs — on the lowest-yield asset.

You already half-know this; you called it out and then said "mainly what I want to discuss is the AI
services." Trust that instinct.

**What to do instead:** `05-creator-track.md`. Short version — you have a creator play that pays for
itself twice, and it's the one you're already accidentally doing.

---

## One site or two?

**One. niktechai.com, with `/smb/` as a separate front door.**

- A domain registered on 2026-08-25 has zero authority. Splitting it across two domains gives you two
  zero-authority sites instead of one. Every SMB page you publish also makes the enterprise side
  rank better, and vice versa.
- It's reversible. A subfolder becomes a subdomain or its own domain later with 301s. The reverse —
  merging two established sites — is much messier.
- **The real risk is price anchoring**, in both directions: an enterprise prime seeing "$299/mo" and
  a salon owner seeing "forward-deployed AI engineering." Mitigation is separation, not a second
  domain: the homepage stays enterprise, `/smb/` has its own nav and its own language, and neither
  page shows the other's pricing.

Revisit at five paying SMB clients. At that point the SMB line may deserve its own brand — and by
then you'll know what to call it, which you don't yet.

---

## What I'd worry about that you didn't mention

1. **Directory listings will undo your privacy work.** Highest-priority fix. `03-identity-and-privacy.md`.
2. **No LLC yet.** You're personally liable for an AI that books appointments and talks to the
   public, in your own cloned voice. This is a real exposure, not a formality.
3. **Recording and disclosure.** California is an all-party consent state for call recording, and it
   has a bot-disclosure statute. An AI answering a business's phone touches both. You already
   flagged the disclosure instinct in the voice config — now it needs to be in the product spec and
   the contract, not just a note.
4. **Support hours are a promise you can't keep.** Do not offer phone support. Offer a response SLA
   you can actually hit from a phone at 9pm ("next business evening"), and put it in writing.
5. **Concentration.** Pick one vertical and go deep. Salons + barbershops + med spas: dense in the
   Inland Empire, appointment-driven, low IT sophistication, owners talk to each other, and the
   install is identical every time. Dealerships are richer but the sale is longer, the stack is more
   political, and your friend already owns that channel — better as a referral partnership than a
   thing you attack cold. See `02-go-to-market.md`.
