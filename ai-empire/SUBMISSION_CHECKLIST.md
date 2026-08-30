# Submission Checklist

Do these in order. First two steps are "free, fastest feedback"; Google Play is the first paid store.

---

## Step 0 — Push the updated game to GitHub (do once)

✅ **GitHub works.** Repo = **`containergu/ai-empire`** (your SSH key authenticates as `containergu`), default branch `main`. The game lives at `ai-empire/www/index.html` inside it; the live site is deployed from there by `.github/workflows/pages.yml`.

**Safe way to push (recommended — fresh clone + copy your changed files):**

```bash
# 1. Clone the repo to a clean folder:
git clone git@github.com:containergu/ai-empire.git "D:\AI functionsfromOther\ai-empire-repo"

# 2. Copy your updated game files into the clone (paths match your working folder):
#    ai-empire/www/index.html           <- the edited game
#    ai-empire/README.md                <- rewritten
#    ai-empire/package.json             <- fixed description
#    ai-empire/STORE_LISTING.md         <- new
#    ai-empire/SUBMISSION_CHECKLIST.md  <- new
#    ai-empire/MARKET_SURVEY.md         <- new

# 3. Commit and push:
cd "D:\AI functionsfromOther\ai-empire-repo"
git add ai-empire/
git commit -m "Update AI Empire: de-risk names, add rewarded ads + remove-ads, docs"
git push origin main
```

**After the first push**, updating the website is just: edit `www/index.html` → `git add` → `git commit` → `git push`. GitHub Actions auto-deploys.

> Note: your `D:\AI functionsfromOther\Cursor Claude` folder is a working copy of this repo (its root = the repo root), but its `.git` is missing and it holds many extra files not in the repo. That's why a fresh clone + copy is safer than re-initializing git in place.

---

## Before any submission — finish monetization wiring

- [ ] **Create an AdMob account** (admob.google.com)
- [ ] Get real **ad unit IDs** → paste into the `AD_UNITS` constant in `www/index.html`
- [ ] Get real **app IDs** → paste into `capacitor.config.json` (`admobIOSAppId` / `admobAndroidAppId`)
- [ ] **Remove Ads IAP**: wire a real purchase plugin in `purchaseRemoveAds()` and create a "remove_ads" product ID (only needed for Google Play / App Store, not web portals)
- [ ] Write a **Privacy Policy URL** (required by Google Play; host a free one on GitHub Pages or a Google Doc — must mention AdMob data collection)

---

## 1. CrazyGames (free, fastest feedback)

1. Create account at developer.crazygames.com
2. Submit the web build (upload a .zip of `www/`, or link the GitHub Pages URL)
3. Fill title, description, tags, thumbnail (see STORE_LISTING.md)
4. **Integrate their SDK (CAAS)** to earn ad revenue on their platform — otherwise the game runs but doesn't monetize through them. Their SDK replaces/injects ads; your AdMob code stays for the mobile app.
5. Submit for review (~1–2 weeks). They're responsive with feedback.

## 2. GameDistribution (free)

1. Create account at gamedistribution.com
2. Upload the build; they provide their ad SDK to drop in
3. Publish — their network pushes your game to many portals
4. Payment is monthly rev-share once you hit their minimum threshold

## 3. Google Play ($25, one-time — your real app store)

1. Create a Play Console account → pay $25
2. **Build the Android AAB**: open `android/` in Android Studio → Build → Generate Signed App Bundle (follow the Play Console signing steps)
3. Create app, fill listing (STORE_LISTING.md), upload icons + screenshots
4. Set content rating (questionnaire — no violence/gambling, so quick)
5. Add AdMob (already in code) + Privacy Policy URL
6. Set price "Free", enable "Contains ads"
7. Submit for review (usually 1–3 days)

## 4. 4399 (free, China market — game is already bilingual)

1. Register at 4399's developer platform (open.4399.com / 4399 开发者平台)
2. Submit the H5 game per their format; they'll ask for title/desc/screenshots
3. Integrate **their** ad SDK (their revenue share, not AdMob) — note this may require a Chinese 实名/ICP (备案) for some placements; confirm their current requirements with them
4. Review is manual and can be competitive

## 5. Apple App Store — DEFER

- $99/year **and** requires a Mac + Xcode to build/sign (you're on Windows)
- Revisit only if the game earns enough to justify it (roughly $200+)

---

## Quick reference — asset checklist

- [ ] App icon 512×512 (exists at `www/icon-512.png`)
- [ ] Screenshots: menu, gameplay, hero-select (at least 3, portrait)
- [ ] 16:9 thumbnail for CrazyGames/GameDistribution
- [ ] Privacy Policy URL
