---
name: secretary-reference
description: 推荐信奇 - 参考过去推荐信风格，根据CV生成推荐信Word文件
---

# 推荐信奇 (Reference Letter Qi)

根据学生简历/CV生成推荐信，输出为 Word (.docx) 文件。模仿 **George (Yuqi Gu)** 的写作风格、语气和结构。

Call via: `/reference-qi`

---

## George's Writing Style (Analyzed from 6 historical letters, 2015–2026)

### Structural Template

```
[Date]

[Recipient — "To Whom It May Concern" / "To the Admissions Committee" / specific committee]

Subject: [optional — for specific scholarships/programs]

**Para 1 — Opening & Relationship**
  "It gives me great pleasure to write this letter of recommendation for [Name]..."
  / "It is my great pleasure to recommend [Name] for [program/position]..."
  State: which courses they took, duration of acquaintance, context (semester, year)

**Para 2 — Academic Engagement**
  "always came prepared with the reading assignments, and was a good participant in class"
  "impressed me with [his/her] thoughtful questions"
  Shows commitment to learning / intellectual curiosity

**Para 3 — Skills & Project Example**
  "excellent communication skills" + "extremely organized, reliable and hard-working"
  Specific project: case study / financial analysis / valuation
  "ability to appropriately apply [theory] to real world practice"
  "work both independently and in group"

**Para 4 — Beyond the Classroom**
  Extracurriculars: leadership roles, clubs, honors (Senior Key, Fulbright, etc.)
  Professional experience relevant to application
  Quantify when possible (budgets, team sizes, etc.)

**Para 5 — Personal Qualities**
  "personable, humble and engaging"
  "open-minded and intellectually curious"
  "responds well to constructive criticisms"

**Para 6 — Closing & Endorsement Level**
  "[Name] has my highest recommendation" / "I highly recommend [Name] without reservation"
  For top candidates: "I would rank [Name] in the top 1% of students I have taught"
  "If I can provide additional information to support [Name]'s application, please feel free to..."

[Sincerely / Best regards,]
Yuqi (George) Gu
[Title — Assistant/Associate Professor of Finance]
[School — Atkinson Graduate School of Management, Willamette University / etc.]
[Contact: phone + email]
```

### Evolution of Style

| Era | Title | Tone | Key Feature |
|-----|-------|------|-------------|
| 2015 (Amanda) | Assistant Prof, WNEU | Warm, basic structure | Shorter, simpler |
| 2021 (Ahmed) | Assistant Prof, Willamette | Brief, supporting letter | Short program endorsement |
| 2023 (Tony) | Assistant Prof, Willamette | Solid, formulaic | Standard template |
| 2024 (Eliete) | Associate Prof, Willamette | Polished, detailed | Professional experience, Fulbright |
| 2026 (Sarah) | Associate Prof, Willamette | Deeply personal | "All in" language, specific scholarship alignment |
| 2026 (Sean) | Associate Prof, Willamette | Confident, specific | Top 1% ranking, growth area, highest rec without reservation |

**2026 Mature Style Features** (use for new letters):
- Ranking: "top 1% of students I have taught" for exceptional candidates
- Growth area: A brief, constructive growth suggestion (shows thoughtful assessment)
- Stronger endorsement: "without reservation," "highest recommendation"
- Specific anecdotes: Name the actual project/company/analysis done
- Quantified impact: Dollar amounts, percentages, team sizes

### Signature Evolution

Current signature (use this):
```
Yuqi (George) Gu
[Title]
[School]
[Email]
```

---

## Workflow

### Step 1: Greet & Collect Info

Ask the user for:
1. **Student's name**
2. **CV/Resume** — user will upload or paste
3. **Target**: What is this for? (grad school admissions, scholarship, internship, job)
4. **Recipient**: Who should the letter be addressed to? (Admissions Committee, specific name, "To Whom It May Concern")
5. **Relationship**: How long have you known the student? Which course(s) did they take with you? When?
6. **Strength anecdote**: Any specific project, paper, or moment where the student excelled?
7. **Program specifics**: If grad school, what program? If scholarship, what's the scholarship about?
8. **Ranking**: Is this student truly top-tier? (Controls whether to include "top 1%" language)

### Step 2: Analyze the CV

Extract key highlights:
- GPA, relevant coursework
- Previous internships/work experience
- Leadership roles and extracurriculars
- Honors and awards
- Skills (quantitative, communication, technical)

### Step 3: Draft the Letter

Follow the template structure above. Use George's signature phrases naturally. Adapt the tone:
- **Top student** → "top 1%", "without reservation", growth area section
- **Good student** → Standard template, omit ranking
- **Brief letter** → For simple program endorsements (like Ahmed's GAME Forum letter), keep to 2-3 paragraphs

### Step 4: Generate Word File

Use `generate_docx.py` (in this directory) to create a properly formatted .docx file:

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Write the letter content into a Document
# Use Times New Roman 12pt, single spacing
# Date right-aligned, body justified
```

### Step 5: Save & Confirm

Save to: `Writing reference letter/{StudentName}/Recommendation letter for {StudentName}.docx`
(Also save a PDF copy if possible.)

Confirm with the user: "Letter saved. Any revisions needed?"

### Step 6: Print user-facing summary

In Chinese (since George types in Chinese):
> 推荐信已生成并保存到 Writing reference letter/{Name}/ 目录。
>
> 主要内容要点：
> - 推荐程度：[highest / strong / standard]
> - 重点突出了：[key亮点]
> - 如需修改请告诉我。

---

## Important Notes

- **Honesty first**: Never fabricate specific details about the student's performance. If George says they took a specific course, that must be true. If he says they did a specific project, confirm it happened.
- **Consistency**: Use George's voice — warm, professional, measured. Not overly flowery, not too dry.
- **Contact info**: Always include "feel free to contact me" with phone and email.
- **Chinese prompt handling**: When George types in Chinese, follow the CLAUDE.md convention — show English translation, then respond in Chinese.
