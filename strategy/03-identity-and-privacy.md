# Identity and privacy — do this before the first listing

## The conflict

Today you started a data-broker opt-out campaign because your home address was on **page 1 of Google**
via FastPeopleSearch, CyberBackgroundChecks, USPhoneBook and Information.com — traced back to a
doxxing incident.

Today you also said you want to register in the Yellow Book and elsewhere.

**Business directories are data brokers with better manners.** They publish name + address + phone,
and — this is the part that matters — the aggregators *scrape each other*. One listing with your home
address on it will be copied into dozens of sites within months, including the exact people-search
brokers you are currently paying attention to removing yourself from. You would be re-seeding the
thing you're cleaning up, from an authoritative source, permanently.

This is not a reason to skip local listings. Local listings are how a service business gets found.
It's a reason to **build a business identity that is not your personal identity first** — then list
that, freely and aggressively, forever.

---

## The fix: four separations, in this order

### 1. Legal entity — form the LLC

Register **NikTech AI LLC** in California. This is already half-decided (the domain WHOIS registrant
org is deliberately blank waiting for it, and the LinkedIn page says "Self Employed" pending it).

Three reasons it's now urgent rather than eventual:
- **Liability.** An AI answering a business's phone, in a cloned voice, booking appointments and
  quoting prices. If it books a customer wrong, misquotes, or mishandles someone's information,
  "Nikhil Harinath personally" should not be the defendant.
- **The listing problem.** An LLC gives you a business name and a registered business address to list
  instead of your own.
- **Federal path.** SAM.gov registration is already blocked on LLC + EIN. This unblocks that too.

⚠️ **California specifics to budget for:** the $800 annual franchise tax applies to LLCs, and there's
a Statement of Information filing. Confirm current amounts and first-year rules with a CPA — it is
the one recurring cost that surprises people.

**Use a registered agent service, not your home address.** The registered agent's address goes on the
public filing. If you use your own, `2478 Nova Way` becomes a permanent public record on the
Secretary of State's website — which is *precisely* where several people-search brokers source from,
and unlike a broker listing you cannot opt out of it.

### 2. Address — get a real business address

You need something that is not your house and is not obviously a mailbox.

| Option | Cost | Works for Google Business Profile? | Notes |
|---|---|---|---|
| **Registered agent only** | ~$50–150/yr | No | For the state filing. Do this regardless. |
| **Virtual office w/ mail** (Regus, Opus, local) | ~$50–100/mo | Usually | Best balance. Some offer occasional meeting-room use, which is genuinely useful for a client meeting. |
| **UPS Store / CMRA mailbox** | ~$25–40/mo | Often rejected | Google actively filters CMRA addresses. Fine for mail, risky as your listing address. |
| **Coworking membership** | $100–300/mo | Usually | Overkill unless you'd use the desk. |

**Recommendation:** registered agent for the filing + a virtual office address in Corona/Riverside or
Orange County for everything public. Pick the city you want to rank in — the address is a ranking
input, not just a mailing detail.

### 3. Phone — a business number, permanently separate

`(310) 210-4559` is already on broker lists. Never put it on a listing again.

Get a new business number and use it everywhere public. Options: Google Voice (free, fine to start),
or — better — **a second Twilio number, since you already run Twilio.** That gives you something the
free options don't: your own AI Front Desk can answer your business line. Which means every prospect
who calls you gets a live demo of the product before you say a word. That is a genuinely strong sales
asset and costs about a dollar a month.

⚠️ Your current Twilio account is on a **trial** — callers hear a trial notice and only verified
numbers can reach it. The ~$20 upgrade is a prerequisite for using it as a real business line *or*
for selling the product. Do it before the first sales call, not after.

### 4. Email and web — already done

`nick@` / `hello@` / `info@` → Gmail via Cloudflare Email Routing, catch-all dropped. WHOIS redacted.
Site says "Corona, California" with no street address; LinkedIn page has "no street address" ticked.
This part of your setup is already correct — keep it that way and use the business address only where
one is structurally required.

---

## Then list aggressively

Once the entity, address and phone exist, listings stop being a risk and become pure upside. Order of
value:

1. **Google Business Profile** — worth more than every other directory combined. Register as a
   **service-area business**: you enter an address for verification, then **hide it** and define
   service areas instead (Corona, Riverside, Orange County, LA metro, San Diego). This is a supported,
   normal configuration for businesses that go to the customer. Set service areas to match the site's
   existing `areaServed` JSON-LD.
2. **Bing Places** — cheap, takes ten minutes, and feeds Copilot.
3. **Apple Business Connect** — free, feeds Apple Maps and Siri, almost nobody bothers.
4. **Yelp** — for service businesses it still drives real calls in SoCal. Claim it even if you never
   pay them.
5. **Nextdoor Business** — this is the actual "neighborhood" channel you were describing, and it's
   far more effective locally than Yellow Pages.
6. **Chamber of Commerce** (Corona, Riverside, whichever OC city you target) — the membership fee is
   mostly a networking cost, but the backlink and the referral flow are real.
7. **Alignable, Thumbtack, local BNI chapter** — situational; test one at a time.
8. **yellowpages.com** — do it for completeness, expect nothing. It is a legacy aggregator now, not a
   discovery channel. The instinct behind it (be findable locally) is right; Google Business Profile
   is where that instinct actually pays.

**One hard rule: NAP consistency.** Name, Address, Phone must be byte-identical everywhere —
"NikTech AI LLC", one address string, one phone. Inconsistent NAP is the single most common reason
local rankings stall. Keep the canonical strings in one file and copy-paste from it every time.

---

## Ongoing hygiene

- Re-run the broker opt-out sweep quarterly — brokers re-list people every few months. Tracker is at
  `wiki/privacy-exposure-cleanup.md`.
- Before any new listing, check what it will publish. If the form requires a street address that will
  be shown publicly, use the business address or skip the listing.
- Never let a client's invoice, contract, or Stripe receipt carry the home address — those get
  forwarded, and they end up in inboxes you don't control.
