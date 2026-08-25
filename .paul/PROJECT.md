# PROJECT — NikTech AI small-business services line

**Slug:** `niktech-smb` · **Started:** 2026-08-25 · **Owner:** Nick (Nikhil Harinath)

## What we're building

A productized AI services line for local small businesses, running alongside the existing
enterprise practice (NikTech AI / niktechai.com), plus a decision on the creator track.

**The product is the AI Front Desk** — the Twilio → agent → ElevenLabs-cloned-voice phone stack
that already runs on the hub Mac, turned into a cloud-hosted, per-client-configured, monthly
subscription for appointment-based local businesses.

**Day-90 success metric: $1,000+ MRR from 3+ paying clients.** Not leads, not revenue, not
followers. If MRR isn't growing, the model is wrong and activity won't fix it.

## Decisions already made — do not relitigate

A fresh session should treat these as settled unless Nick reopens them.

1. **Lead with the AI Front Desk, not custom software.** Recurring, identical per install,
   demoable in 30 seconds. Custom builds are the upsell to existing clients, never the wedge.
   Never quote hourly.
2. **The binding constraint is the full-time Microsoft contract.** Every offer must pass:
   *sellable in one evening call, installable on a weekend, then runs without him.* Anything
   needing daytime availability is out.
3. **Beachhead vertical: salons, barbershops, nail salons, med spas.** One vertical until it's
   boring. Dealerships are a referral partnership with his friend's IT company, not a cold-attack
   channel.
4. **One brand, one domain.** niktechai.com stays; `/smb/` is a separate front door. Homepage
   stays enterprise-facing so a prime or recruiter never lands on `$349/mo`. Revisit a separate
   brand at 5+ SMB clients.
5. **Business identity before any public listing.** LLC → registered agent → virtual business
   address → separate business phone, *then* Google Business Profile. Non-negotiable ordering —
   see guardrails.
6. **The toddler-video channel is killed as a business line.** COPPA "Made for Kids" disables
   personalized ads, comments and notifications; no contactable audience, no funnel, compounds
   with nothing. The creator play is the engineering notes + filming the SMB installs.
7. **Outbound before SEO.** SEO is the credibility backstop, not the pipeline.

## 🚧 Guardrails — hard rules for this project

- **Never publish Nick's home address or personal phone.** `2478 Nova Way, Corona, CA 92883` and
  `(310) 210-4559` are actively being removed from people-search brokers
  (`wiki/privacy-exposure-cleanup.md`). City-level "Corona, California" is fine; a street address
  is not, in copy, in schema, on an invoice, or on any directory listing.
- **Never use `+1 (833) 566-1733` as the demo or business number.** That's the recruiter-screening
  line, wrong persona, and still on a Twilio trial that gates callers.
- **Never claim a clearance.** US Citizen and clearance-eligible only.
- **Never name a client.** The beverage engagement is "a global beverage manufacturer"; the
  materials client stays generic.
- **No AI attribution on client-facing work** — no `Co-Authored-By`, no "Generated with Claude
  Code" in commits, PRs, docs or artifacts that a customer will see. (This repo is Nick's own lab
  and carries the standard trailer; `niktechai-site` must not.)
- **Never publish a blog draft, a site page, or a listing without Nick's review.** Draft mode
  exists for exactly this (`status: draft` → real URL, `noindex`, DRAFT banner, out of index and
  sitemap).
- **Never sell a phone line that depends on hardware in Nick's house.** See phase 02.
- **Anything legal, tax or entity-related is a recommendation, never an action.** Claude does not
  file, sign, or register on his behalf.

## Where things live

| Thing | Path / URL |
|---|---|
| This plan, in full | `strategy/` in this repo — start `strategy/00-assessment.md` |
| Drop-in site pages | `site/smb/`, `site/ai-front-desk/` in this repo |
| Draft PR | https://github.com/CloudDevops/pwa-hello/pull/1 |
| Read-only summary | https://claude.ai/code/artifact/2767930f-d6d9-4b0f-8581-b5e0a9104bcc |
| Live site source | `labs/niktechai-site/` — **resolve the real path first**, see below |
| Voice stack | OpenClaw voice-call plugin, `127.0.0.1:3334`, Tailscale funnel |
| Secrets | Keychain: `cf-site-token`/`cloudflare`, `r2-account-id`/`r2`; `~/.openclaw/voicecall-secrets.json` |
| Outbound/content skills | `~/.claude/skills/niktechai-outbound/`, `~/.claude/skills/niktechai-content/` |

⚠️ **`labs/` moved out of the vault on 2026-07-28** and the memories disagree on where it landed.
Resolve before assuming:

```sh
~/.claude/hook-state/resolve-handoff.sh --list
ls -d ~/projects/labs/niktechai-site ~/Info_vault/labs/niktechai-site 2>/dev/null
```

## Related memories

`niktechai-brand-site` · `niktechai-marketing-engine` · `local-llm-openclaw-setup` ·
`privacy-broker-cleanup` · `domain-web-estate` · `federal-contracting-path` ·
`user_career_strategy_2026`
