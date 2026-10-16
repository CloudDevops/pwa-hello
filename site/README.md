# Drop-in pages for niktechai.com

Two new pages for the small-business line, written to match the live site exactly — same CSS
variables, same header/nav/footer, same theme toggle (`ntai-theme`), same `/api/contact` form
contract, zero third-party JS.

```
site/smb/index.html            →  public/smb/index.html            →  https://niktechai.com/smb/
site/ai-front-desk/index.html  →  public/ai-front-desk/index.html  →  https://niktechai.com/ai-front-desk/
site/_partials/style.css       →  reference only, already inlined in both pages
```

---

## 🔴 Blocker before deploying

Both pages contain **`{{DEMO_NUMBER}}`** and **`{{DEMO_NUMBER_E164}}`** placeholders. Do not deploy
until a real demo number exists.

```sh
grep -rn 'DEMO_NUMBER' site/          # 6 occurrences across the two pages
```

**Do not use `+1 (833) 566-1733`.** That's the recruiter-screening line, it's still on a Twilio
**trial** (callers hear a trial notice and only verified numbers get through), and the persona is
wrong. Provision a separate number after the ~$20 Twilio upgrade — see `strategy/03-identity-and-privacy.md`.

Replace with e.g.:

```sh
cd site
sed -i '' 's/{{DEMO_NUMBER_E164}}/+19515550123/g; s/{{DEMO_NUMBER}}/(951) 555-0123/g' \
  smb/index.html ai-front-desk/index.html
```

Everything else on the pages is real and ready.

---

## Deploy

```sh
cd ~/Info_vault/labs/niktechai-site
mkdir -p public/smb public/ai-front-desk
cp /path/to/site/smb/index.html            public/smb/index.html
cp /path/to/site/ai-front-desk/index.html  public/ai-front-desk/index.html

# bare deploy — wrangler.toml supplies name + pages_build_output_dir,
# and args here would skip the Functions bundle and the R2 binding
npx wrangler pages deploy
```

⚠️ If `build.py` regenerates `public/`, put these under whatever `build.py` treats as static pages
(same place `capability/` lives) or it'll wipe them on the next build.

## Post-deploy checklist

- [ ] `curl -o /dev/null -w '%{http_code}\n' https://niktechai.com/smb/` → 200
- [ ] `curl -o /dev/null -w '%{http_code}\n' https://niktechai.com/ai-front-desk/` → 200
- [ ] `curl -o /dev/null -w '%{http_code}\n' https://niktechai.com/nonexistent` → **404, not 200**
      (the soft-404 regression — re-verify after every build change)
- [ ] Both URLs added to `sitemap.xml` (priority `0.9`) and to `llms.txt`
- [ ] IndexNow POST for both URLs (Bing/Yandex — Google doesn't participate)
- [ ] Submit both in Google Search Console
- [ ] Rich Results Test on both — `Product` + `FAQPage` on `/ai-front-desk/`,
      `Service` + `FAQPage` on `/smb/`
- [ ] Contact form: submit one test on each, confirm the R2 object lands under `claude/contact/<date>/`
- [ ] Check both in light and dark, and at 375px wide

## One-line homepage edit

Add the SMB front door to `public/index.html`'s nav so the two sides link to each other:

```html
<nav>
  <a class="hide-sm" href="#services">Services</a>
  <a class="hide-sm" href="#experience">Experience</a>
  <a class="hide-sm" href="/smb/">Small business</a>   <!-- add this -->
  <a href="/blog/">Notes</a>
  <a href="#contact">Contact</a>
  <button id="tt" title="Toggle theme" aria-label="Toggle theme">◐</button>
</nav>
```

And in the footer:

```html
<a href="/smb/">Small business</a> ·
```

Deliberately **not** added to the homepage hero or body copy — the homepage stays enterprise-facing
so a prime or a recruiter never lands on `$349/mo`. See the price-anchoring note in
`strategy/00-assessment.md`.

---

## Notes on choices made

- **Prices are published.** Unusual for services, deliberate here: it filters tyre-kickers before
  they cost you an evening, and "what does an AI receptionist cost" is exactly the question an AI
  assistant gets asked — a page with real numbers gets cited, a "contact us for pricing" page never
  does.
- **`/ai-front-desk/` has a "What it doesn't do" section.** Counterintuitive, and it's the section
  that will close deals. It's also the kind of specificity that gets a page cited rather than
  skimmed.
- **JSON-LD references the existing org** via `{"@id": "https://niktechai.com/#org"}` rather than
  redeclaring the organisation — no competing entity definitions across pages.
- **No street address anywhere**, in copy or schema. `areaServed` only, matching the homepage.
  See `strategy/03-identity-and-privacy.md`.
- **Calendly is not embedded** — embeds are a paid feature on the free plan and render "This calendar
  is currently unavailable." Neither page loads any third-party JS. Worth creating a separate
  SMB-specific Calendly event type rather than reusing `intro-call-niktech-ai`, which is worded for
  enterprise.
- **Contact form reuses `/api/contact`** exactly as-is — same field names (`name`, `email`, `org`,
  `message`, `website` honeypot), so submissions land in R2 with no Function changes.
