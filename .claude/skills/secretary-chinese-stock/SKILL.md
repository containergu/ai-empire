---
name: secretary-chinese-stock
description: 股票奇 - 每日推荐 A股+港股+ETF 三支标的，深度研究 + PDF + 微信推送
---

# 股票奇 (Chinese Stock Qi)

每日 A 股 + 港股 + ETF 三支标的深度研究。自动选取当前最具关注价值的标的，多维度并行分析，生成全中文研报，保存为 Markdown + PDF，并通过 Server酱 推送到微信。

## Config

Read `mysecretary/config.json`:
- `wechat.serverchan_key` — Server酱 SendKey（必填，否则无法推送）

## 自动运行

本 skill 通过 CronCreate 设置为每天定时自动执行。自动模式下：

### Step 1: 选标的

自动从以下三类各选 1 支，共 3 支：

**A 股（深/沪）：**
- 选股逻辑：近期有催化剂的龙头股（业绩超预期、政策利好、行业拐点）
- 覆盖范围：消费、新能源、科技、金融、医药等主要板块轮动

**港股（HKEX）：**
- 选股逻辑：估值有吸引力、有独特性的港股标的（互联网、生物医药、消费）
- 优先选择 A 股没有的稀缺标的

**ETF（国内可买）：**
- 选股逻辑：近期热门主题 ETF（科创50、恒生科技、芯片、证券、红利等）
- 偏向宽基指数或政策主题

> 每日更换，避免连续推荐同一标的。周一轮动消费/金融，周二科技/新能源，周三医药/制造，周四互联网/ETF，周五综合复盘型。

### Step 2: 多维度并行研究

对每支标的，使用 **Perplexity MCP** (`perplexity_research`) 并行研究5个维度：

| 维度 | 搜索关键词 | 收集数据 |
|:----|:---------|:---------|
| 基本面 | `{ticker} {name} 财务数据 营收 净利润 毛利率` | 营收、净利润、毛利率、增长率、现金流 |
| 估值 | `{ticker} {name} 估值 PE PB` | PE、PB、历史估值区间、同业对比 |
| 机构观点 | `{ticker} {name} 分析师评级 目标价` | 评级、目标价、consensus、变化趋势 |
| 新闻风险 | `{ticker} {name} 最新新闻` | 头条利好、风险事件、政策变化 |
| 行业格局 | `{ticker} {name} 竞争格局 行业趋势` | 市场份额、竞争地位、行业趋势 |

### Step 3: 撰写三合一深度研报

合成一份研报，按标的分为三个 section：

```markdown
# 每日三支深度研报 — YYYY-MM-DD

> **声明:** 本报告仅供研究参考，不构成投资建议

## 今日推荐组合

| 类别 | 标的 | 代码 | 核心理由 | 风险等级 |
|:----|:----|:----|:--------|:-------:|
| A股 | ... | ... | ... | 中/高 |
| 港股 | ... | ... | ... | 中/高 |
| ETF | ... | ... | ... | 低/中 |

---

## 一、A股推荐：{name} ({ticker})

### 公司概览
### 财务分析
### 估值水平
### 机构观点
### 头条风险与利好
### 投资逻辑

---

## 二、港股推荐：{name} ({ticker})

...（同上结构）

---

## 三、ETF推荐：{name} ({ticker})

### 产品概况
### 持仓与跟踪标的
### 近期表现
### 配置逻辑

---

**风险提示：** 以上分析基于公开信息，不构成投资建议。
```

Save to: `research/YYYY-MM-DD_daily-picks.md`

### Step 4: 转 PDF

```bash
md-to-pdf "research/YYYY-MM-DD_daily-picks.md"
```

### Step 5: 推送到微信

```powershell
$cfg = Get-Content "mysecretary/config.json" -Raw | ConvertFrom-Json
$mdContent = Get-Content "research/YYYY-MM-DD_daily-picks.md" -Encoding UTF8 -Raw
$uri = "https://sctapi.ftqq.com/$($cfg.wechat.serverchan_key).send"
$body = @{ title = "每日三支 | YYYY-MM-DD"; desp = $mdContent; short = "今日推荐: ..." }
Invoke-RestMethod -Uri $uri -Method Post -Body $body
```

Verify `code: 0` in response.

### Step 6: 汇报完成

> "今日三支推送完成！A股：xxx | 港股：xxx | ETF：xxx"
> "研报已保存至 research/YYYY-MM-DD_daily-picks.pdf"

## Skill Invocation

用户主动使用时：
> `/stock-qi`

每日定时自动推送由 CronCreate 管理。
