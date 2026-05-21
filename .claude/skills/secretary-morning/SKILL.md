---
name: secretary-morning
description: 早晨全流程 - 依次执行新闻奇 → 穿搭奇 → 教练奇 → 日报奇
---

# 早晨好！(Morning Secretary)

一键执行完整的早晨秘书流程。依次运行四个步骤，每步与你交互完成后自动进入下一步。

## Workflow

执行完整的早晨流程，按顺序：

### Step 1: 新闻奇（自动为主）

参照 `secretary-news` skill 的流程：
1. WebSearch/WebFetch 搜刮今日金融新闻
2. 分类整理（宏观经济、A股、美股、产业、政策）
3. 生成摘要 → 保存到 `mysecretary/contexts/news_archive/YYYY-MM-DD.md`
4. 如果配置了 Discord webhook，发送摘要
5. 简要向用户汇报结果（2-3句话）

完成后自动进入下一步（无需用户确认）。

### Step 2: 穿搭奇（需交互）

参照 `secretary-outfit` skill 的流程：
1. 问用户今天的场合
2. 查天气
3. 给出穿搭推荐
4. 保存到 `mysecretary/contexts/outfit_log/YYYY-MM-DD.md`

完成后自动进入下一步。

### Step 3: 教练奇（需交互）

参照 `secretary-coach` skill 的流程：
1. 问用户今天的体重
2. 读历史数据，分析趋势
3. 给反馈
4. 问运动/饮食计划，给建议
5. 保存记录

完成后自动进入下一步。

### Step 4: 日报奇（需交互 + 自动）

参照 `secretary-daily` skill 的流程：
1. 问今日安排
2. 读取前面三步的产出作为上下文
3. 生成结构化日程早报
4. 如果配置了 Discord webhook，发送给工作群
5. 保存到 `mysecretary/contexts/schedules/YYYY-MM-DD.md`

### 完成

总结今天早晨的产出，给用户一句鼓励：
> "好的 George，今早的秘书工作完成啦！今天的新闻摘要、穿搭建议、健康记录和日程早报都已经准备好了。祝你今天顺利！"
