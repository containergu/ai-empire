# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Two things live here:

1. **Toy apps** — standalone HTML/Python apps, no build system, no dependencies
2. **MySecretary** — a Claude Code agent system (skills in `.claude/skills/`) that runs a daily routine for George (finance professor)

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
