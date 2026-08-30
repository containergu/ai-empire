# AI Empire (AI 帝国塔防)

A bilingual (中文/English) **tower-defense** game with a tech-startup theme: place towers, fend off waves of bugs, viruses, bad models, regulators, and the AGI boss, and climb from a Silicon Valley garage to the cloud.

## Play Online

**https://containergu.github.io/ai-empire/**

Open in mobile browser → **Add to Home Screen** to install as an offline PWA.

## The Game

- **Tower defense**: 15 levels across 3 maps (Silicon Garage → Shenzhen Factory → Cloud Battle)
- **5 tower types** (GPU Tower, Firewall, Data Miner, Neural Net, Transformer), each upgradeable to Lv.3
- **3 heroes** (Jacket King, Rocket Bro, The Oracle) with active + passive abilities
- **Star ratings** (1–3 stars per level), level unlocking, and a persistent wallet (20% of earnings carries over between levels)
- **Rewarded ads**: revive on death, double the level reward, and a 60s 2× earnings boost
- **Remove Ads** purchase (banner + rewarded ads disabled)
- **Offline PWA** — play in browser or install to home screen

## How to Update (edit once, deploy anywhere)

`www/index.html` is the **single source of truth**. The live site is served directly from `www/` by GitHub Actions — there is nothing else to keep in sync.

**Update the website:**
```bash
# 1. Edit www/index.html
# 2. Commit and push — GitHub Actions auto-deploys to GitHub Pages
git add ai-empire/www/index.html
git commit -m "Update AI Empire"
git push origin main
```

**Update the mobile app (Android / iOS):**
```bash
npx cap sync               # copies www/ into ios/ and android/
npx cap open android       # or: npx cap open ios
# rebuild from Android Studio / Xcode
```

> `docs/` is an unused copy from an earlier setup and is safe to delete — deployment reads `www/`, not `docs/`.

## Monetization Setup (AdMob + Remove Ads)

- **Ad unit IDs** live in one place: the `AD_UNITS` constant at the top of the AD INTEGRATION section in `www/index.html`. Replace the test IDs there with your real ones.
- **AdMob app IDs** live in `capacitor.config.json` (`admobIOSAppId` / `admobAndroidAppId`). Replace with your real app IDs.
- **Remove Ads** is currently a demo purchase. Wire a real IAP plugin (e.g. `@capacitor-community/purchases` or `cordova-plugin-purchase`) inside `purchaseRemoveAds()` in `index.html` before shipping.

## Build as Mobile App (Capacitor)

### Prerequisites
- Node.js 18+
- Xcode (iOS) — macOS only
- Android Studio (Android)
- CocoaPods (iOS): `sudo gem install cocoapods`

### Steps
```bash
npm install
npx cap sync
npx cap open ios      # or: npx cap open android
# build & run from Xcode / Android Studio
```

## File Structure
```
ai-empire/
├── www/                  # ← the game (single source of truth)
│   └── index.html        # complete self-contained game
├── ios/                  # Xcode project (Capacitor)
├── android/              # Android Studio project (Capacitor)
├── capacitor.config.json # Capacitor + AdMob app IDs
├── package.json
└── README.md
```
