# Go to market — how the first ten clients actually arrive

## Channel priority (the same correction as the enterprise side)

Outbound produces clients in weeks. SEO produces clients in six to twelve months and its real job is
to *exist* when someone Googles you after you've already contacted them. Don't spend a month on
content while the pipeline is empty.

| Rank | Channel | Time to first client | Effort |
|---|---|---|---|
| 1 | **Walk-in / drive-by, local** | 1–3 weeks | Saturday mornings |
| 2 | **Warm network + your friend's dealership channel** | 1–4 weeks | A few conversations |
| 3 | **Cold call / cold email to a tight vertical list** | 2–6 weeks | 30 min/evening |
| 4 | **Google Business Profile + local SEO** | 2–6 months | Setup, then trickle |
| 5 | **Nextdoor / local Facebook groups** | 1–3 months | Low |
| 6 | **Content / YouTube** | 6–12 months | High, compounds |

The SMB channel that works differently from enterprise: **you can walk in the door.** A salon owner
at 10am on a Saturday will talk to you. A VP of Data at a Fortune 500 will not. Use the advantage you
have — this is the one part of the local business that your day job doesn't block, because it happens
on weekends.

---

## Beachhead: pick one vertical, not five

You listed salons and (via your friend) car dealerships. Don't do both at once.

**Start with appointment-based personal services: hair salons, barbershops, nail salons, med spas.**

Why this one:
- The pain is acute and obvious: the phone rings while both hands are in someone's hair.
- Every install is identical — hours, services, prices, book an appointment. That's the whole domain
  model. Client #10 is the same work as client #2.
- Dense in Corona / Riverside / Inland Empire. You can hit fifteen in one Saturday on foot.
- Low IT sophistication → your enterprise background reads as extraordinary rather than table stakes.
- Owners talk to each other constantly. Vertical referral loops are tight and fast.
- Low stakes if something goes wrong. Nobody dies because a haircut got double-booked.

**Second wave (month 3+):** auto repair, dental, HVAC/plumbing, veterinary. Same product, same
install, bigger budgets, longer sale.

**Car dealerships: partner, don't attack.** Your friend already runs IT for that vertical. He has the
relationships, the trust and the door. Going in cold behind him is the worst of both worlds. Instead:
take him to lunch and propose (a) he refers AI work to you for a cut of year one, (b) you refer
break/fix and infrastructure to him, (c) you ask him for his actual playbook — how he got the first
dealership, what the objections were, what he charges. That conversation is worth more than fifty
cold calls, and it costs you lunch.

---

## The Saturday walk-in routine

The single highest-yield thing on this list, and the one most people won't do.

**Before you go (Friday evening, 30 min):**
- Pick a 2-mile radius. List 15 salons from Google Maps.
- Call each one during business hours from a blocked number. **Log who doesn't answer.** That's your
  lead score, gathered in fifteen minutes, and it makes your pitch specific.
- Note which use Square/Booksy/Vagaro (visible on their site or Google listing).

**The visit (Saturday 9–11am, before they get busy):**
- Walk in. Ask for the owner. If busy, leave a card and come back.
- 20 seconds: *"I build AI systems for large companies during the week. I've built a small version
  that answers the phone for shops like yours when you're with a client. I called on Thursday at 2pm
  and it rang out — that's a booking you didn't get. Want to hear it? Call this number right now."*
- Hand them a card with the demo number. **Let them call it while standing there.**
- Don't close. Ask for 15 minutes next week, by phone, in the evening.

**Why this works:** you're not selling AI, you're pointing at a missed call they already know about.
The demo does the persuading. And the "I do this for large companies" line resolves the only real
objection — why should I trust this guy — in one sentence.

**Target:** 15 doors, 5 real conversations, 2 demos, 1 client. Do it four Saturdays in a row before
judging it. The first Saturday will be terrible. That's normal and it's not information.

---

## Cold outreach cadence

For the doors you can't walk into. Templates in `outreach/email-templates.md`.

- **Batch of 20** per evening session, one vertical, one city.
- Day 1: email. Day 4: call (leave a voicemail that mentions the email). Day 8: second email, new
  angle. Day 15: break-up email. Then stop.
- **Measure replies per 20 sent, not sends.** Sends are activity; replies are signal. Below 2 replies
  per 20, the message is wrong — rewrite it, don't send more.
- Personalize one line, always, and make it something only a human would notice: their booking
  system, a recent review, the fact that their voicemail is full.

---

## Local SEO — set it up once, then leave it

Runs in the background while outbound does the work. Setup order:

1. **Google Business Profile**, service-area business, address hidden. Categories, hours, services
   with prices, 10+ photos. Post weekly for the first month.
   ⚠️ Do not create this until the LLC, business address and business phone exist —
   see `03-identity-and-privacy.md`. Changing NAP later resets trust signals.
2. **`/smb/` and `/ai-front-desk/` pages** on niktechai.com (built — see `site/`).
3. **One page per vertical per city** as you win each one:
   `/ai-phone-answering-for-salons/`, `/ai-receptionist-corona-ca/`. Thin pages are worse than no
   pages — each needs real content and ideally a named local result.
4. **Reviews.** Ask every happy client at day 14, with a direct link. Five real Google reviews
   outrank almost anything else you can do locally.
5. **Local citations** — the list in `03-identity-and-privacy.md`, identical NAP everywhere.

**GEO note:** the same advantage applies here as enterprise. "AI phone answering for a salon in
Corona CA — what does it cost?" is a question an AI assistant will answer, and specificity beats
domain age. A page that names actual prices, actual booking tools (Square, Booksy, Vagaro) and actual
failure modes gets cited. A vague "AI solutions for your business" page does not.

---

## Proof assets to build in the first 60 days

Ranked by how much they shorten the sale:

1. **A live demo number anyone can call.** Non-negotiable. This *is* the sales collateral. Put it on
   the site, the card, the GBP listing, and your business line.
2. **A 60-second phone video of a real client saying it books appointments while they work.** Worth
   more than any amount of copy.
3. **One written case study with a number in it** — calls answered, appointments booked, in a month.
4. **A physical card** with the demo number and a QR code. Cheap, and you're doing walk-ins.

---

## Metrics to track weekly

Keep it in `outreach/prospects.csv` and one line in your weekly note. Four numbers:

- Doors knocked / emails sent
- Conversations had
- Demos given
- Clients closed + MRR

**The one number that matters at month 3: MRR.** Not revenue, not leads. If MRR isn't growing, the
model is wrong and no amount of activity fixes it.
