---
name: pdf-reader
description: PDF阅读专家 - 用最佳方式提取PDF文本、表格、结构化内容。支持文字PDF/扫描件/学术论文/表格
---

# 📄 PDF 阅读器 / PDF Reader Qi

Extract text and tables from PDFs using the right tool for each document type.

## Quick Decision Tree

```
PDF to read?
├── Text-based PDF (typed, not scanned)
│   ├── Simple text, no complex tables
│   │   └── Use Read tool (built-in, no setup)
│   ├── Complex layout / columns / CJK characters
│   │   └── Use PyMuPDF (fitz)
│   └── Tables / structured data
│       └── Use pdfplumber
├── Scanned PDF (images, no selectable text)
│   ├── OCR installed → Use pytesseract
│   └── OCR not installed → Use Read tool (may work partially)
└── Academic paper from arXiv
    └── Use MCP paper-search (read_arxiv_paper / mcp__paper-search__read_arxiv_paper)
```

## Setup

Run once to install all tools:

```powershell
pip install pymupdf pdfplumber markitdown pytesseract
```

> **macOS**: also `brew install tesseract` for OCR support.
> **Windows**: Tesseract OCR needs a [separate installer](https://github.com/UB-Mannheim/tesseract/wiki).

Already installed on this system:
- `PyPDF2` (basic fallback)
- `Pillow` (image support for OCR)

## Methods

### Method 1: Built-in Read Tool (Zero Setup)

Best for: **Simple text-based PDFs, academic papers**

Just use the Read tool with `pages`:

```
Read: file.pdf (pages: "1-10")
```

**Limitations**: Struggles with columns, tables, scanned images, Chinese/CJK text. When it fails → move to Method 2.

### Method 2: PyMuPDF (fitz) — Best All-Around Text Extractor

Best for: **Most text PDFs, complex layouts, CJK text**

```python
import fitz
doc = fitz.open("path/to/file.pdf")
for page in doc:
    print(page.get_text())
```

Extract specific pages:

```python
import fitz
doc = fitz.open("path/to/file.pdf")
text = ""
for i in range(5):  # pages 0-4
    text += doc[i].get_text()
print(text)
```

**Why it's the default**: Fast, handles columns and tables reasonably, good CJK support, minimal dependencies.

### Method 3: pdfplumber — Best for Tables

Best for: **Extracting tables and structured data**

```python
import pdfplumber
with pdfplumber.open("path/to/file.pdf") as pdf:
    for page in pdf.pages:
        # Extract all text
        text = page.extract_text()
        # Extract tables
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

Table extraction with cleanup:

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("path/to/file.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)

    result = pd.concat(all_tables, ignore_index=True)
    print(result.to_string())
```

### Method 4: markitdown — PDF → Markdown

Best for: **Well-structured documents, clean markdown output**

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("path/to/file.pdf")
print(result.text_content)
```

Produces clean Markdown with headers, lists, bold/italic preserved.

### Method 5: OCR (pytesseract) — For Scanned PDFs

Best for: **Image-based / scanned PDFs with no selectable text**

```python
import pytesseract
from PIL import Image
import fitz

doc = fitz.open("scanned_file.pdf")
for page_num in range(len(doc)):
    pix = doc[page_num].get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    text = pytesseract.image_to_string(img, lang="eng+chi_sim")
    print(f"--- Page {page_num+1} ---")
    print(text)
```

### Method 6: PyPDF2 — Basic Fallback (Already Installed)

Best for: **Minimal dependencies, simple text extraction**

```python
from PyPDF2 import PdfReader
reader = PdfReader("path/to/file.pdf")
for page in reader.pages:
    print(page.extract_text())
```

## Two-Line Universal Reader

When you just need the text out, no questions asked:

```python
import fitz
print("".join(page.get_text() for page in fitz.open("path.pdf")))
```

Or with MarkItDown for cleaner output:

```python
from markitdown import MarkItDown
print(MarkItDown().convert("path.pdf").text_content)
```

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| Empty text from PyMuPDF | Try `page.get_text("text")` instead of `page.get_text()` |
| Garbled CJK characters | Use PyMuPDF (best CJK support) or OCR fallback |
| Tables not detected | pdfplumber `extract_tables()` with `table_settings` param |
| Scanned PDF returns nothing | Must use OCR (Method 5) |
| MarkItDown returns error | PDF may be scanned — fall back to OCR |
| Read tool returns "file exists but..." | Try one of the Python methods above |
| Large PDF (>20 pages) | Read in chunks: pages 0-10, then 10-20, etc. |

## Example: Read Specific Pages from a PDF

```python
import fitz, sys
path = sys.argv[1]
start = int(sys.argv[2]) - 1  # 1-indexed to 0-indexed
end = int(sys.argv[3])
doc = fitz.open(path)
for i in range(start, end):
    print(f"--- Page {i+1} ---")
    print(doc[i].get_text())
```

Usage:
```powershell
python -c "import fitx, sys; doc = fitz.open(sys.argv[1]); [print(f'--- Page {i+1} ---\n{doc[i].get_text()}') for i in range(int(sys.argv[2])-1, int(sys.argv[3]))]" file.pdf 1 5
```
