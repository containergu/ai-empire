# AI Empire (AI 帝国)

Idle clicker game — build an AI startup from a garage to the cloud.

## Quick Start (Browser)

Open `www/index.html` in any browser. That's it.

## Build as Mobile App

### Prerequisites

- Node.js 18+
- Xcode (for iOS) — macOS only
- Android Studio (for Android)
- CocoaPods (for iOS): `sudo gem install cocoapods`

### Steps

```bash
# 1. Install deps
npm install

# 2. Sync Capacitor (copies web assets to native platforms)
npx cap sync

# 3. Open in native IDE
npx cap open ios    # or
npx cap open android

# 4. Build & run from Xcode / Android Studio
```

### AdMob

Test ad units are already configured. Before publishing:

1. Create AdMob accounts for iOS and Android
2. Replace `admobIOSAppId` and `admobAndroidAppId` in `capacitor.config.json`
3. Update banner and rewarded video ad unit IDs in the AdMob dashboard

### Building for Production

```bash
# iOS
npx cap sync ios
# Open ios/ in Xcode, select Generic iOS Device, Product > Archive

# Android
npx cap sync android
# Open android/ in Android Studio, Build > Generate Signed Bundle / APK
```

## Game Overview

- **Click** the GPU/Server/AI core to earn Compute
- **Buy upgrades** (16 total across 4 stages) to boost earnings
- **Unlock stages**: Garage → Office → Datacenter → Cloud
- **Prestige**: "Train Foundation Model" to earn AI Progress points (permanent multiplier)
- **Offline earnings**: Compute accumulates while away (up to 8 hours)
- **Ads**: Banner (bottom) + Rewarded video (2x boost / compute pack)

## File Structure

```
ai-empire/
├── www/                  # Web assets
│   └── index.html        # Complete game (self-contained)
├── ios/                  # Xcode project (Capacitor)
├── android/              # Android Studio project (Capacitor)
├── capacitor.config.json # Capacitor configuration
├── package.json          # Dependencies
└── README.md
```
