# AI Empire (AI 帝国) - Game Design Doc

## Overview
Idle clicker game about building an AI startup. Hand-drawn doodle art style. Cross-platform (iOS + Android via Capacitor). Monetized via AdMob.

## Platform
- HTML5 Canvas game wrapped with Capacitor
- One codebase → iOS App Store + Google Play
- Also playable directly in browser for testing

## Core Loop
Click GPU/Server → earn Compute → buy upgrades → unlock stages → prestige (Train Foundation Model) → permanent bonuses → repeat

## Game Systems

### Economy
- **Compute** - main currency, earned by clicking + passive generation
- **AI Progress** - prestige currency, earned by resetting

### 4 Stages
| Stage | Scene | Unlock | Visual Theme |
|-------|-------|--------|-------------|
| 0 - Garage | PC on a desk | Start | Warm, messy, late-night coding |
| 1 - Office | Standing desk + whiteboard | 1K total compute | Bright, productive |
| 2 - Datacenter | Server racks | 100K total compute | Cool blues, blinking lights |
| 3 - Cloud | AI in the sky | 10M total compute | Ethereal, glowing |

### Upgrades (16 total, 4 per stage)
Each upgrade boosts Click Power (CPC) or Per-Second (CPS). Costs scale exponentially. Later upgrades unlock stage-appropriate visuals.

### Prestige ("Train Foundation Model")
- Unlocks at 1M total compute
- Resets all compute, keeps AI Progress
- Formula: `prestigePoints = floor((totalEarned / 1e6) ^ 0.5)`
- Each point = +10% permanent earnings bonus

### Offline Earnings
- Compute accumulates while away (up to 8 hours)
- Calculated from CPS at time of closing
- Show summary on return

### Save System
- Auto-save every 30 seconds (localStorage)
- Manual save button
- Load on startup

## Art Style
- Hand-drawn doodle (thick black strokes, slight wobble)
- AI blue (#4A90D9) accent color
- All Canvas 2D - no image assets needed
- Animated elements: GPU fan spin, floating +N numbers, blinking LEDs, data streams

## Ads (AdMob via Capacitor)
| Type | Placement | User Action |
|------|-----------|-------------|
| Banner | Bottom of screen fixed | Passive view |
| Rewarded Video | "2x Boost 30min" button | Opt-in tap |
| Rewarded Video | "Compute Pack" button | Opt-in tap |

## Technical Stack
- HTML5 Canvas 2D rendering
- Vanilla JS (no frameworks)
- CSS responsive layout (mobile-first)
- Capacitor 7 for native wrapper
- @capacitor-community/admob for ads

## Monetization Flow
1. User plays game (fun!)
2. Banner ad displays at bottom (passive revenue)
3. When waiting for compute: watch rewarded video for boost (active revenue)
4. No forced ads, no popups - keep players happy
