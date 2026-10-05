# CLAUDE.md

This repo holds two unrelated things. Check which one the task is about before acting.

## 1. `niktech-smb` — the NikTech AI small-business services line

**Read `.paul/` before doing anything on this.** In order, it's about five minutes:

1. `.paul/STATE.md` — where we are right now and what's blocked, on whom
2. `.paul/PROJECT.md` — decisions already made, and the guardrails below in full
3. `.paul/HANDOFF-niktech-smb-2026-08-25.md` — the handoff, including what's unblocked today
4. `.paul/ROADMAP.md` and the relevant `.paul/phases/*.md`

Full reasoning behind every decision is in `strategy/` (start `strategy/00-assessment.md`).
**Don't re-derive the strategy.** If something looks wrong, say so in one line and carry on.

Drop-in site pages for niktechai.com are in `site/` — see `site/README.md`, and note they carry
`{{DEMO_NUMBER}}` placeholders that must be resolved before any deploy.

### 🚧 Guardrails — these are hard rules, not preferences

- **Never publish Nick's home address or personal phone**, in copy, schema, an invoice, or a
  directory listing. City-level "Corona, California" is fine; a street address is not. Both are
  actively being removed from people-search brokers.
- **Never use `+1 (833) 566-1733`** — recruiter-screening persona, still on a Twilio trial.
- **Never name a client** — "a global beverage manufacturer", "a materials manufacturer".
- **Never claim a clearance** — US Citizen and clearance-eligible only.
- **No AI attribution on client-facing work** — no `Co-Authored-By`, no "Generated with Claude
  Code" in anything a customer sees. This lab repo carries the trailer; `niktechai-site` must not.
- **Never publish a blog draft, site page or listing without Nick's review.**
- **Never sell or deploy a client phone path that depends on hardware in Nick's house.**
- **Legal, tax and entity work is a recommendation, never an action.** Don't file, sign or
  register anything on his behalf.

### Optional: the topic registry and PAUL hook

If `~/.claude/hook-state/` exists on this machine, registering the slug makes the handoff
resolvable from any cwd:

```sh
mkdir -p ~/.claude/hook-state/topics
echo "$PWD" > ~/.claude/hook-state/topics/niktech-smb.txt
~/.claude/hook-state/resolve-handoff.sh niktech-smb
```

If it doesn't exist, skip it — this file is the entry point and needs no infrastructure. The
`~/bin/claude-paul-context` SessionStart hook that auto-injects `.paul/STATE.md` is likewise a
convenience; it was installed on the hub Mac only and is not in claude-sync.

## 2. `pwa-hello` — the original lab project

A minimal Hello World PWA for testing home-screen install on an iPad. `index.html`,
`manifest.json`, icons. Deployed to GitHub Pages from `main`. See `README.md`.

Unrelated to the strategy work above — don't let a change to one touch the other.
