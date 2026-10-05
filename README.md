# pwa-hello

Minimal "Hello World" Progressive Web App, designed to be deployed to GitHub Pages and installed on an iPad's home screen via Safari → Share → Add to Home Screen. It now also carries a **Congress Trades** tracker (`trades.html`) that shows the stock trades politicians disclose under the STOCK Act.

## What's here

- `index.html` — the page (clock + tap counter, dark theme, safe-area aware) with a link to the tracker
- `trades.html` — the Congress Trades tracker (filters, watchlist, aggregate "signals", President's filings, background notes)
- `scripts/fetch_trades.py` — pulls the official House, Senate and White House disclosures into `data/*.json` (stdlib only + `pdftotext`)
- `data/` — the generated JSON the tracker reads (refreshed daily by GitHub Actions)
- `.github/workflows/update-trades.yml` — the daily refresh job
- `docs/congress-trades-research.md` — research notes: how disclosure works, who to follow, whether copying works, data sources
- `manifest.json` — PWA manifest with `display: standalone` (plus a home-screen shortcut to the tracker)
- `icon-192.png`, `icon-512.png` — PWA icons
- `apple-touch-icon.png` — iOS home-screen icon (180x180)

All asset paths are relative (`./...`), so it works at any GitHub Pages subpath without changes.

## Congress Trades tracker

Live page once deployed: `https://clouddevops.github.io/pwa-hello/trades.html`

**Where the data comes from.** Members of Congress (and their spouses and dependent children) must file a Periodic Transaction Report for any trade over $1,000 within 30 days of learning about it and no later than 45 days after the trade. The script reads the primary sources directly:

| Source | What | How it is read |
| --- | --- | --- |
| House Clerk (`disclosures-clerk.house.gov`) | Yearly ZIP index of filings + one PDF per report | Index is tab-separated text; e-filed PDFs are converted with `pdftotext -layout` and parsed row by row. Paper filings are image scans and are listed as unparsed. |
| Senate eFD (`efdsearch.senate.gov`) | Search endpoint + one HTML table per report | Script accepts the portal's prohibition notice, pages through the PTR search results and parses each report's table. |
| White House (`whitehouse.gov/disclosures`) | OGE Form 278-T PDFs for the President and senior staff | Scanned images without a text layer, so only the list of filings and links is kept. |
| `unitedstates/congress-legislators` | Party and state for every sitting member | Joined by state/district (House) or name (Senate). |

**Output.** `data/house-<year>.json` and `data/senate-<year>.json` hold one record per filing with its parsed trades (owner, ticker, asset, asset class, buy/sell/exchange, trade date, amount bracket, notes, parsed option strike/expiry). `data/president.json` lists the White House PTRs. `data/index.json` says what exists and when it was generated. Runs are incremental: a filing already in the output is not fetched again.

**Refresh.** The workflow runs daily at 14:17 UTC (and on demand via *Actions → Update congressional trades data → Run workflow*) and commits any changes to `data/`. Because Pages deploys from `main`, that commit is what updates the page. The schedule only runs on the default branch, so merge first. If a bot commit ever fails to trigger a Pages rebuild, switch *Settings → Pages → Source* to **GitHub Actions** or run the workflow manually.

**Run locally.**

```sh
sudo apt-get install poppler-utils      # provides pdftotext (brew install poppler on macOS)
python3 scripts/fetch_trades.py          # current + previous year, writes ./data
python3 scripts/fetch_trades.py --years 2026 --limit 20   # quick smoke test
python3 -m http.server 8080              # then open http://localhost:8080/trades.html
```

The first full run downloads every PTR PDF for the requested years (roughly 40 MB per year) into `.cache/trades/`, which is git-ignored.

**Caveats.** Amounts are brackets, not exact values. Filings arrive weeks after the trade. Around 10% of House reports and a few Senate reports are paper scans that are linked but not parsed. The President's filings are not parsed at all. None of this is investment advice; see the research notes for what the evidence says about copying these trades.

## Test locally

```sh
cd ~/Info_vault/labs/pwa-hello
python3 -m http.server 8080
```

Open http://localhost:8080 in any browser. To test from the iPad on the same Wi-Fi: replace `localhost` with the Mac's LAN IP (`ipconfig getifaddr en0`).

## Deploy to GitHub Pages

One-time, from this directory:

```sh
git init -b main
git add .
git commit -m "Initial PWA hello world"

# Create the repo on GitHub and push (needs gh CLI logged in)
gh repo create pwa-hello --public --source=. --push
```

Then enable Pages:

1. Open the repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)` → Save
4. Wait ~1 min. Site lives at: `https://clouddevops.github.io/pwa-hello/`

## Install on iPad

1. Open `https://clouddevops.github.io/pwa-hello/` in **Safari** (must be Safari)
2. Tap **Share** → **Add to Home Screen** → **Add**
3. Launch from the home-screen icon — it opens fullscreen, no Safari chrome

## Iterating

Edit files locally → `git commit && git push` → GitHub Pages re-deploys in ~30-60s. On the iPad, force-quit the installed app and re-launch to pick up changes (or pull-to-refresh inside it).

## Related

- [Toddler games: store publishing and monetization plan](docs/toddler-games-store-publishing.md) (research dated October 4, 2026). This repo is the install-on-iPad rehearsal that plan builds on.
