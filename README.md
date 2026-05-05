# pwa-hello

Minimal "Hello World" Progressive Web App, designed to be deployed to GitHub Pages and installed on an iPad's home screen via Safari → Share → Add to Home Screen.

## What's here

- `index.html` — the page (clock + tap counter, dark theme, safe-area aware)
- `manifest.json` — PWA manifest with `display: standalone`
- `icon-192.png`, `icon-512.png` — PWA icons
- `apple-touch-icon.png` — iOS home-screen icon (180x180)

All asset paths are relative (`./...`), so it works at any GitHub Pages subpath without changes.

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
