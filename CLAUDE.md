# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Two things live here:

1. **Toy apps** — standalone HTML/Python apps, no build system, no dependencies
2. **MySecretary** — a Claude Code agent system (skills in `.claude/skills/`) that runs a daily routine for George (finance professor)

## Global Behavioral Rules

These rules apply across ALL conversations and sessions for George:

### Research Output Convention
- All industry/market research reports are saved to `research/` directory as formatted Markdown files
- Naming convention: `YYYY-MM-DD_topic.md`
- Format: proper heading hierarchy, aligned tables, citation index, bilingual (中文 + English)

### Language Handling
- **Always**: George types in Chinese → first show "> **Your prompt in English:**" + English translation → then respond
- **Research**: English prompt → bilingual report (中文 section first, English second, `---` divider)
- **Non-research**: English prompt → respond naturally (English or Chinese as fits)
- **Exception**: `/reflection-qi` — fully Chinese, skip English preview

## Toy Apps

| File | Description | How to Run |
|---|---|---|
| `star_garden.html` | HTML5 Canvas game — catch falling stars/flowers with a cute cat | Open in browser |
| `tomato_clock.py` | Python Tkinter Pomodoro timer | `python tomato_clock.py` |
| `tomato_clock.html` | HTML/CSS/JS Pomodoro timer | Open in browser |

Conventions: HTML apps are fully self-contained (inline CSS/JS). Python apps use stdlib only. No build step.

## MySecretary Agent System

A chain of Claude Code skills that run a daily personal secretary workflow. The user invokes skills via slash commands in the chat.

### Skills (`.claude/skills/`)

| Command | Agent | What it does |
|---|---|---|
| `/morning-qi` | **Orchestrator** | Runs news → outfit → coach → daily in sequence |
| `/news-qi` | 新闻奇 | Scrapes financial news, summarizes, saves to archive, sends to Discord |
| `/outfit-qi` | 穿搭奇 | Asks today's occasion, checks weather, recommends outfit |
| `/coach-qi` | 教练奇 | Logs weight, tracks health trends, recommends exercise/diet |
| `/daily-qi` | 日报奇 | Plans daily schedule, generates morning report, sends to Discord |
| `/reflection-qi` | 反思奇 | Evening reflection guide — reviews today's files, leads structured复盘 |
| `/literature-qi` | 文献奇 | Searches academic papers (arXiv, Semantic Scholar, Google Scholar), saves results |
| `/reference-qi` | **推荐信奇** | 根据学生CV生成推荐信Word文件，模仿George的写作风格 |
| `/stock-qi` | **股票奇** | 每日自动推荐 A股+港股+ETF 三支标的，深度研报 + PDF + 微信推送 |

### Context Data (`mysecretary/contexts/`)

| Folder | Written by | Content |
|---|---|---|
| `news_archive/` | news-qi | Daily financial news summaries |
| `outfit_log/` | outfit-qi | Daily outfit recommendations |
| `health_records/` | coach-qi | Weight log (`data.json`) + daily notes |
| `schedules/` | daily-qi | Daily schedule reports |
| `reflections/` | reflection-qi | Evening reflection journals |
| `literature/` | literature-qi | Paper search results + `reading_list.json` |

### Config

`mysecretary/config.json` — user profile, Discord webhook URLs, fitness goals, weather city, news preferences, Server酱 WeChat push key.

### Integration

- **Discord**: news summaries and daily reports sent via webhook (`Invoke-RestMethod` POST)
- **Weather**: fetched via `wttr.in` API (PowerShell `curl`)
- **News**: scraped via `WebFetch` from 华尔街见闻, 财联社, Yahoo Finance, Investing.com
- **WeChat**: stock research reports pushed via Server酱 (sct.ftqq.com) using SendKey from `config.json`

### Key Workflow Pattern

The morning orchestration (`/morning-qi`) is sequential — each step writes to context and the next step reads it. Skills that need user interaction ask inline and wait for a response. Skills that auto-send to Discord use the webhook URL from config.json.

## Karpathy Coding Guidelines

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.
