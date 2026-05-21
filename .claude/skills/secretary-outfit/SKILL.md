---
name: secretary-outfit
description: 穿搭奇 - 根据场合和天气提供每日穿搭建议
---

# 穿搭奇 (Outfit Qi)

穿搭顾问。根据今天的场合和天气，给出专业的穿搭建议。

## Config

Read `mysecretary/config.json` for user location/city.

## Workflow

### Step 1: 问场合

Ask the user what occasions they have today. Example prompt:
> "早上好！今天有什么场合呀？比如：上课、会议、学术报告、 casual 办公、外出调研……"

List common options based on being a professor:
- 上课 (teaching)
- 会议/讲座 (meetings/seminars)
- 学术报告 (academic presentations)
- 办公室办公 (office work)
- 外出调研 (field research)
- 休闲 (casual)

### Step 2: 查天气

Use **WebFetch** or `curl` to get today's weather for the user's city (from config.json):

```
curl -s "wttr.in/{city}?format=j1" | ...
```

Extract: current temp, high/low, humidity, precipitation chance, wind.

### Step 3: 穿搭推荐

Combine occasion + weather to give a tailored recommendation covering:
- **上装** (top) - shirt, jacket, layering
- **下装** (bottom) - pants, skirt
- **鞋子** (shoes)
- **配饰** (accessories) - tie, scarf, watch
- **特别提醒** - umbrella, extra layers, sun protection

### Step 4: 存档

Save recommendation to: `mysecretary/contexts/outfit_log/YYYY-MM-DD.md`
