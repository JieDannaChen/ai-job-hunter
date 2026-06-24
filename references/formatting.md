## File Conventions

| Artifact | Naming | Location |
|----------|--------|----------|
| Base resume (EN) | `Resume_Optimized_EN.md` | User's resume directory |
| Base resume (CN) | `简历-优化版.md` | User's resume directory |
| Tailored resume | `Resume_[Company]_[Role_Short].md/.docx` | User's resume directory |
| Cover letter (EN) | `CoverLetter_[Company]_[Role_Short].md` | User's resume directory |
| 求职信 (CN) | `求职信_[公司]_[岗位].md` | User's resume directory |
| Interview prep | `Interview_Prep_[Company]_[Role_Short].md` | User's resume directory |
| JD analysis | `JD_Analysis.md` | User's resume directory |

---

## Markdown to DOCX Conversion

Use `scripts/md_to_docx.py` (included in this repo) or inline `python-docx` for conversion.

```bash
# Convert with the included script (uses PEP 723 inline dependencies):
uv run scripts/md_to_docx.py Resume_Company_Role.md

# Or specify output path:
uv run scripts/md_to_docx.py Resume_Company_Role.md output/resume.docx
```

Key formatting rules:

| Element | Format |
|---------|--------|
| Page margins | 1.5cm top/bottom, 2.0cm left/right |
| Body font | Calibri 10pt |
| H1 (Name) | Calibri 22pt, centered, dark blue (#2C3E50) |
| H2 (Sections) | Calibri 12pt, bold, dark blue |
| H3 (Roles) | Calibri 11pt, bold, accent blue (#2D5A8E) |
| Bullets | Calibri 10pt, 0.25" indent |
| Tables | Alternating row shading (#F0F4F8), dark header (#2D5A8E) |
| Contact line | Calibri 9pt, centered, gray (#555555) |

---

## Language Support

This skill supports bilingual operation:

| Scenario | Resume Language | Cover Letter | Interview Prep |
|----------|---------------|--------------|----------------|
| International/multinational company, English JD | English | English | English |
| Chinese company, Chinese JD | 中文 | 中文 | 中文 |
| Chinese company, English JD | English | English | Bilingual (EN structure + CN talking points) |
| Global company, JD mentions Chinese market | English | English | English with CN product knowledge |
| User explicitly requests language | Follow user preference | Follow user preference | Follow user preference |

### Chinese Resume Conventions (中文简历规范)

Chinese tech resumes differ from English resumes in several ways:

| Element | English Convention | 中文惯例 |
|---------|-------------------|---------|
| Title | Role-focused (e.g., "Senior SWE") | 方向+定位 (e.g., "质量工程专家 — AI测试智能体") |
| Summary | 3-4 sentences | 可以更长，突出核心成果全景 |
| JD alignment | Implied through experience bullets | 显式 "核心能力-JD对标" 表格更有效 |
| Metrics | Numbers inline in bullets | 加粗关键数字 (**95%**) |
| Length tolerance | 2-3 pages max | 可接受3-4页（经验丰富的候选人） |

---

## Examples
