# Toddler Games: Store Publishing and Monetization Plan

Research date: October 4, 2026. Scope: Dino Valley (primary), Little Cybertruck Garage, Jev ABC,
Picture Finder, Tiny Colors. Every store rule below was checked against the live source on the
research date; measurements of the games were taken the same day. Earlier research lives in the vault
note `wiki/toddler-game-dev.md` (sections dated 2026-08-25 and 2026-09-27); this document corrects two
of its conclusions (see "What changed since the last research").

## Bottom line

1. **Publish, in two tracks.** Track A (this month, $0 in fees): a free web demo plus a paid web
   edition sold through itch.io and a merchant-of-record checkout. Track B (weeks 2 to 6): the Apple
   App Store first, then Google Play and the Amazon Appstore from the same packaged build.
2. **The "easy" Play route is closed for kids' apps.** PWABuilder / Trusted Web Activity packaging is
   blocked by Google's Families policy for any app whose audience includes children. The Android path
   is therefore a bundled Capacitor app, the same project that produces the iOS build.
3. **Apple before Google.** The games are built for the iPad, Apple has no tester gate, and the
   Kids Category rules are easy to meet with a game that ships zero SDKs, zero links and zero network
   calls. Google Play's personal-account rule (12 testers for 14 continuous days) is the real
   schedule risk, and the exemption (an organization account with a D-U-N-S number) sits behind the
   same LLC paperwork the federal-contracting path already needs.
4. **Three fixes gate every paid listing:** remove Tesla and Cybertruck branding, re-voice the 41
   narration clips under a commercial license, and publish a privacy-policy page on hosting Nick
   controls. Each is weekend-sized.
5. **Costs:** $0 web and itch.io, $99 per year Apple, $25 once Google, $0 Amazon. The hub Mac already
   has JDK 17 and the Android SDK; Xcode 26 (about 15 GB) is the one large install.

## What changed since the last research

| Earlier conclusion (vault) | Status on October 4, 2026 |
|---|---|
| "This Mac cannot currently build a mobile app at all" (2026-08-25) | Stale. JDK 17, the Android command-line SDK (platform 34, build-tools 34) and Gradle 8.14.3 were installed on the hub Mac on 2026-09-12. Only Xcode is missing. |
| PWA packaging (PWABuilder) was treated as the low-friction Play route | Not available for this audience. PWABuilder's own instructions: "PWAs on Android cannot currently target children as their audience" because "PWAs potentially have full access to the web." |
| Apps parked, KDP first (decision 2026-08-25) | Historical, not a prohibition (noted 2026-09-27). This document assumes the question is reopened. |

## 1. Inventory, measured October 4, 2026

| Game | Where it lives | What the probe found | Store candidate? |
|---|---|---|---|
| Dino Valley v17 | `dino-valley-meadow.mindrunner.chatgpt.site` (ChatGPT Sites, public) | One 21.1 MB HTML file: 13.9 MB PNG (7 images), 1.0 MB WAV music loop, 0.85 MB MP3 (41 narration clips), 72 KB of code. No network calls, no analytics, no outbound links, no manifest, no service worker. "Cybertruck" and "Tesla" appear in UI text, one narration line and sprite code. | Yes, the lead title. |
| Little Cybertruck Garage | same hosting, private (HTTP 401) | Silent, customization loop. Same branding problem. | Later: a second "world" inside the same app. |
| Jev ABC | `jev-abc.pages.dev` (Cloudflare Pages) | Has a manifest. Sends what the child says to a third-party decision API through a Cloudflare Function. | Not as-is: third-party data flow from a child-directed app conflicts with Apple 1.3, Play Families and COPPA. |
| Picture Finder | `~/toddler-search`, local only | Mic plus Openverse and Wikimedia image search. | No. A household tool, not a product. |
| Tiny Colors | `Archive/labs/toddler-coloring` | Kotlin sources lost; targetSdk 34 (Play now requires 36). | No. Do not revive. |

**Hosting finding.** ChatGPT Sites returns the game page for every path. Requests for
`/.well-known/assetlinks.json`, `/manifest.json` and `/sw.js` all returned HTTP 200 with the 21 MB
HTML body. That means the current host cannot serve the separate files a PWA (manifest, service
worker) or a Trusted Web Activity (asset links) needs. Custom domains are supported by Sites but do not
change this behaviour. Cloudflare Pages (already used for Jev ABC) or GitHub Pages (this repo's
pattern) both serve arbitrary static paths.

## 2. Three ways to put a web game in a store

Think of the game as a stage play and the stores as theatres with house rules.

| Approach | What it is | Who accepts it for a toddler audience |
|---|---|---|
| **PWA** (Progressive Web App) | The website itself, plus a manifest and a service worker so a browser can "Add to Home Screen" and run it offline. No store, no fee, no review. | Not a store. On the iPad it installs only through Safari. Fine for a demo and for direct sales; invisible to store shoppers. |
| **TWA** (Trusted Web Activity; what PWABuilder and Bubblewrap produce) | An Android shell that opens your live website inside Chrome, full screen, after you prove you own the domain with `/.well-known/assetlinks.json`. The content stays on your server. | Google Play: **no** for children. The Families policy forbids apps that "merely provide a webview of a website", and PWABuilder tells kids' developers to declare "Older Users" instead. Apple has no TWA equivalent. |
| **Bundled WebView app** (Capacitor or Cordova) | A real Xcode and Gradle project. Your HTML, JS, PNG and MP3 files are packaged inside the app and run in the system web view (WKWebView on iOS). No server is needed at runtime. | Apple App Store, Google Play and Amazon Appstore all treat this as a normal app. It is how Construct 3, GDevelop and Phaser games ship. Apple's guideline 4.2 ("repackaged website") targets thin wrappers around live sites; an offline game packaged in the binary is not that. |

Design consequence: make the store app the full game and keep the web version a shorter demo. That
answers Apple's "what does the app add" question and gives parents a reason to buy.

## 3. Store rules that matter for a two-year-old's game

### Apple App Store

- Apple Developer Program: $99 per year. Individual enrollment is allowed; the seller name is the
  person's legal name. Apps can be transferred to another account (for example an LLC) later.
- Kids Category age bands: 5 and under, 6 to 8, 9 to 11. Age ratings were reworked in 2025 to
  4+, 9+, 13+, 16+ and 18+; apps rated 4+ or 9+ may sit in the Kids Category.
- Guideline 1.3 (Kids Category): no third-party advertising or analytics except narrow exceptions,
  no links out of the app or purchases outside a parental gate, no personal or device data sent to
  third parties. The cheapest compliance is a game with no SDKs, no links and no network.
- A privacy policy URL is required even when the app collects nothing.
- Guideline 5.2 (intellectual property): third-party trademarks such as Tesla and Cybertruck in a
  commercial app invite rejection or a takedown. Rename and redraw the vehicles.
- Toolchain: Capacitor 8 requires Xcode 26 on macOS and Node 22 or newer. TestFlight gets the build
  onto the iPad before review.
- Apple's Small Business Program keeps the commission at 15 percent under $1M per year.

### Google Play

- Registration: $25 one-time plus identity verification. New apps and updates must target
  Android 16 (API level 36) since August 31, 2026.
- Personal accounts created after November 13, 2023 must run a closed test with at least 12 testers
  opted in for 14 continuous days before applying for production, and Google now checks that testers
  actually used the build. Organization accounts (D-U-N-S number) are exempt.
- Families policy (target audience includes children): the app must not "merely provide a webview of
  a website"; it must not contain APIs or SDKs that are not approved for child-directed services; it
  must not transmit the advertising identifier or hardware identifiers; it needs a Data safety
  declaration, a privacy policy and an IARC content rating. Ads, if any, must come from Families
  self-certified SDKs. This game has none, which keeps the forms trivial.
- Every app accepted into Designed for Families is placed in the "Teacher Approved" review queue;
  approved apps get the badge and the Kids tab.
- Service fee is 15 percent on the first $1M per year.
- Separate from Play: Android developer verification is being enforced for apps installed on
  certified Android devices from September 30, 2026 in Brazil, Indonesia, Singapore and Thailand, and
  globally in 2027. Publishing through Play already verifies identity; it matters only for
  side-loaded builds.

### Amazon Appstore

- Developer account is free. The Appstore was discontinued for general Android phones on August 20,
  2025 but continues on Fire tablets and Fire TV. Fire HD Kids tablets are the most common toddler
  tablet, so this is a real channel for the same Android build.
- Amazon Kids+ (the subscription catalogue) is invitation-only; Amazon contacts developers. A normal
  paid listing is the way in.

### COPPA

The amended FTC rule has been fully in force since April 22, 2026. The game collects no personal
information, and the plan keeps it that way: no accounts, no analytics, no crash reporting, no
microphone, no outbound links. Collecting nothing is what makes both stores' children's forms a
single "no data collected" answer.

## 4. Monetization channels ranked by friction

| Channel | Upfront | Platform take | Friction | Fit for a toddler iPad game | Verdict |
|---|---|---|---|---|---|
| Free web demo plus paid unlock through a merchant of record (Lemon Squeezy: 5% + $0.50; handles sales tax; still accepting new sellers as of September 2026; its team now builds Stripe Managed Payments, so expect a migration offer) | $0 | about 5% + $0.50 | Low | Good for the first paying parents; proves willingness to pay | Do first |
| itch.io paid HTML5 listing (paid games are playable only after purchase; developer keeps 90% by default) | $0 | 10% | Low | No parent audience, but a payment rail with no paperwork | Do first |
| Apple App Store, paid app $3.99 to $4.99 | $99/yr | 15% | Medium (Xcode, Kids review) | Highest: the game was built for the iPad | Do, weeks 2 to 4 |
| Google Play, paid app | $25 | 15% | Medium-high (12 testers x 14 days, or org account) | Good: Android tablets | Do after the Android build; start the test at once |
| Amazon Appstore, paid app | $0 | 30% standard | Low once an APK exists | Good: Fire Kids tablets | Do after Play |
| Gumroad | $0 | 10% + $0.50 plus processing (about 13%) | Low | Same job as Lemon Squeezy at double the fee | Alternative only |
| Portals (Poki, CrazyGames) revenue share or license | $0 | 40 to 50% | Selective acceptance | CrazyGames main site is 13+; toddler fit unproven | Skip for now |
| Ads | $0 | varies | Kids ad SDK certification on both stores | Poor eCPM for toddlers; conflicts with the zero-SDK compliance plan | Skip |
| Subscription | $0 | 15% | Needs a content catalogue | Premature with one world | Defer |
| Microsoft Store via PWABuilder | small one-time fee | 12 to 15% | Low | Wrong device for toddlers | Skip |
| Steam ($100 per app), Teachers Pay Teachers, preschool licensing | $100 / $0 | varies | High or unverified fit | Not an iPad-toddler channel | Later or never |

Price hypothesis: $3.99 one-time, promise "no ads, no accounts, works offline". This is a test, not
measured demand. Revenue expectations should stay modest until real parents have paid.

## 5. Fix list before any paid listing

1. **De-brand the vehicles.** Rename Cybertruck (for example "Steel Truck") and Tesla ("Red Car"),
   regenerate the two sprite sets, change the narration line "C is for Cybertruck" (for example
   "C is for Car"), and update the alphabet word list. The probe counted 15 mentions across UI text,
   narration and sprite code.
   Status, October 4: names and code tokens are done. `tools/debrand-dino-valley.py` rewrites the
   single-file game (15 mentions to 0, asset payloads byte-identical) and renames the rides to
   "Silver truck" and "Red car". Because the camp sign already teaches C with its own clip, tapping the
   silver truck now plays the existing "H is for horn" line, so no brand-bearing audio remains and no new
   recording was needed. Still open: the silver truck sprite is a Cybertruck-shaped render and needs new
   artwork from the image tool on the Mac (frame 0 of the sprites atlas; the red car is a generic crossover).
2. **Re-voice the 41 narration clips with a commercially licensed voice.** The current clips were
   produced with edge-tts, which has no commercial output rights. Options:
   Azure AI Speech on the paid Standard tier (the paid tier grants commercial use of prebuilt neural
   voice output; about $16 per million characters, so this script costs cents; the free F0 tier does
   not carry those rights; Nick has no personal Azure subscription today, so this needs one with a
   payment method), or record his own voice (free, and parents like it), or speak at runtime with the
   device's built-in `speechSynthesis` (no audio files to license; the voice varies by device).
3. **Privacy policy page.** One page stating that the app collects no data. Host it with the web
   edition; both stores require the URL.
4. **Move the web edition to hosting Nick controls.** Cloudflare Pages with the Jev ABC recipe
   (`npx wrangler pages deploy`). Split the 21 MB single file into separate asset files, add
   `manifest.webmanifest` and a service worker that precaches them. Base64 inside HTML inflates the
   download by a third and forces the browser to parse 21 MB before the first frame; separate files
   fix both and make repeat launches instant and offline.
5. **Real-device QA.** iPad Safari and one Android tablet: touch targets, audio starting on the first
   tap, orientation lock, no way for a toddler to leave the game by accident.
6. **Store assets.** 1024 px icon, iPad screenshots, a 30-second gameplay capture, a description that
   leads with what parents care about.

## 6. Packaging recipe (Capacitor 8)

```sh
# in a new folder with the game files under www/
npm init -y
npm install @capacitor/core @capacitor/cli
npx cap init "Dino Valley" com.niktech.dinovalley --web-dir www
npm install @capacitor/ios @capacitor/android
npx cap add ios
npx cap add android
npx cap sync

npx cap open ios        # Xcode: team, bundle id, iPad, orientation; Product > Archive > TestFlight
cd android && ./gradlew bundleRelease   # .aab for Play; assembleRelease gives the APK for Amazon
```

Settings worth fixing on day one:

- No Capacitor plugins beyond core. Every plugin is an SDK the Kids forms must account for.
- Lock orientation to the one the game is drawn for (Xcode Device Orientation; Android
  `android:screenOrientation`).
- iOS: disable link previews and keep the status bar hidden; the game already uses a Play button, so
  audio unlock on first tap keeps working inside WKWebView.
- App Store Connect: Kids Category, age band 5 and under, rating 4+, privacy policy URL, "Data Not
  Collected".
- Play Console: target audience 5 and under, Data safety "no data collected", IARC questionnaire,
  Designed for Families opt-in, closed testing track first.
- Hub Mac toolchain delta: add `platforms;android-36` and `build-tools;36.0.0` with `sdkmanager`;
  Capacitor 8 expects Android Studio 2025.2.1 (which bundles its JDK) or an equivalent JDK 21 for
  Gradle; Node 22 or newer; Xcode 26.

## 7. Sequence

| When | Track A (web, $0) | Track B (stores) |
|---|---|---|
| Week 1 | Fixes 1 to 4. Demo live on Cloudflare Pages. itch.io listing and merchant-of-record checkout live. | Enroll in the Apple Developer Program (identity check takes days). Install Xcode 26. Register the Play Console account ($25) and start recruiting 12 testers. |
| Week 2 | First paying parents or first "no". Fix what real families report. | Capacitor iOS build, TestFlight on the iPad, submit to App Store review in the Kids Category. |
| Weeks 3 to 4 | Keep the demo and the listing in sync with fixes. | Apple review. Android build. Closed test running (14 continuous days). Amazon Appstore submission with the APK. |
| Weeks 5 to 6 | | Play production once the tester window closes, or switch to an organization account when the LLC and D-U-N-S exist. |

## 8. Decisions only Nick can make

- **Seller identity now or after the LLC.** Personal enrollment on both stores works today and both
  stores allow transferring the app to another account later. Waiting for the LLC and D-U-N-S removes
  the 12-tester gate but delays Play by however long the paperwork takes.
- **Narration voice.** Own voice, a paid Azure Speech resource (needs a personal subscription), or
  device speech at runtime.
- **New vehicle names and art.**
- **Price and demo length.** $3.99 or $4.99; how much of the valley the free demo shows.
- **Budget to approve.** $99 Apple, $25 Google, a few dollars of speech synthesis.

## Sources

Store rules and fees
- Apple Kids Category and guideline 1.3: https://developer.apple.com/kids/ and https://developer.apple.com/app-store/review/guidelines/
- Apple age ratings and Kids Category eligibility: https://developer.apple.com/app-store/categories/
- Apple Developer Program enrollment: https://developer.apple.com/programs/enroll/
- Google Play Families policy: https://support.google.com/googleplay/android-developer/answer/9893335
- Google Play target audience and content settings: https://support.google.com/googleplay/android-developer/answer/9867159
- Google Play closed-testing requirement for personal accounts: https://support.google.com/googleplay/android-developer/answer/14151465
- Google Play target API level requirement: https://support.google.com/googleplay/android-developer/answer/11926878
- Google Play Teacher Approved program: https://play.google.com/console/about/programs/teacherapproved/
- PWABuilder Google Play next steps (children restriction): https://github.com/pwa-builder/pwabuilder-google-play/blob/main/Next-steps.md
- Android developer verification rollout: https://android-developers.googleblog.com/2026/03/android-developer-verification-rolling-out-to-all-developers.html
- Amazon Appstore submission FAQ: https://developer.amazon.com/docs/app-submission/faq-submission.html
- Amazon Kids+ inclusion (invitation only): https://community.amazondeveloper.com/t/how-to-get-apps-in-kids/7040
- FTC COPPA compliance guidance: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions

Packaging and tooling
- Capacitor environment setup (v8): https://capacitorjs.com/docs/getting-started/environment-setup
- Trusted Web Activities overview: https://developer.android.com/develop/ui/views/layout/webapps/trusted-web-activities
- Bubblewrap CLI (fallback types): https://github.com/GoogleChromeLabs/bubblewrap/blob/main/packages/cli/README.md
- ChatGPT Sites (custom domains): https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites
- Azure AI Speech pricing and output rights: https://azure.microsoft.com/en-us/pricing/details/speech/ and https://learn.microsoft.com/en-us/answers/questions/1192398/can-i-use-azure-text-to-speech-for-commercial-usag

Sales channels
- itch.io HTML5 and payments: https://itch.io/docs/creators/html5 and https://itch.io/docs/creators/payments
- Lemon Squeezy 2026 update: https://www.lemonsqueezy.com/blog/2026-update
- Gumroad fees: https://gumroad.com/help/article/66-gumroads-fees
- Poki revenue deal types: https://developers.poki.com/guide/revenue-deal-types
- CrazyGames gameplay requirements (13+): https://docs.crazygames.com/requirements/gameplay/
