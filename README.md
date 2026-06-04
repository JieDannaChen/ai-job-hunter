# AI Job Hunter

An end-to-end job hunting skill for [Devin CLI](https://devin.ai) and compatible AI coding assistants. Analyze resumes, search & match jobs, generate role-tailored resumes, write targeted cover letters, and prepare comprehensive interview guides.

**Built from real job-hunting workflows** producing production resumes, cover letters, and 900+ line interview prep documents.

## Features

| Phase | Capability | Description |
|-------|-----------|-------------|
| **1. Profile Build** | Resume Analysis & Optimization | Parse resume, extract skills matrix, identify strengths/gaps, generate optimized base resume |
| **2. Search & Match** | Job Discovery & Scoring | Multi-dimensional web search, JD parsing, 7-factor weighted fit scoring, tiered ranking, not-recommended detection |
| **3. Tailor Resume** | Per-Role Resume Generation | Persona-based reframing, section-by-section customization, internal info sanitization, MD-to-DOCX conversion |
| **4. Cover Letter** | Targeted Narrative Generation | Narrative anchor per role, story selection, tone calibration, EN/CN support |
| **5. Interview Prep** | Comprehensive Preparation | Company research, JD-experience mapping, STAR behavioral stories, technical Q&A, system design scenarios, weakness mitigation |

## Quick Start

### Installation

Copy the skill directory to your Devin CLI skills folder:

```bash
# Global (available in all projects)
mkdir -p ~/.config/devin/skills/job-hunter
cp SKILL.md ~/.config/devin/skills/job-hunter/

# Or project-specific:
mkdir -p .devin/skills/job-hunter
cp SKILL.md .devin/skills/job-hunter/
```

For Windsurf / Claude Code compatibility:

```bash
mkdir -p ~/.claude/skills/job-hunter
cp SKILL.md ~/.claude/skills/job-hunter/
```

### Usage

Invoke the skill in your AI assistant session:

```
/job-hunter
```

Or use natural language triggers:

| Language | Trigger Examples |
|----------|-----------------|
| English | "find jobs", "optimize resume", "tailor resume for [company]", "write cover letter", "prepare interview" |
| Chinese | "找工作", "优化简历", "定制简历", "写求职信", "面试准备" |

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                         JOB HUNTER SKILL                               │
├──────────┬──────────┬──────────────┬──────────────┬───────────────────┤
│ Phase 1  │ Phase 2  │   Phase 3    │   Phase 4    │     Phase 5       │
│ PROFILE  │ SEARCH   │   TAILOR     │   COVER      │     INTERVIEW     │
│ BUILD    │ & MATCH  │   RESUME     │   LETTER     │     PREP          │
├──────────┼──────────┼──────────────┼──────────────┼───────────────────┤
│ Read     │ Web      │ Per-role     │ Narrative    │ Product research  │
│ resume   │ search   │ resume gen   │ reframing    │ JD gap analysis   │
│ Extract  │ JD fetch │ Sanitize     │ Story        │ STAR stories      │
│ skills   │ & parse  │ internal info│ selection    │ Tech Q&A          │
│ Build    │ Score    │ MD -> DOCX   │ Tone match   │ System design     │
│ profile  │ & rank   │ conversion   │ EN / CN      │ Weakness plan     │
└──────────┴──────────┴──────────────┴──────────────┴───────────────────┘
```

Each phase can be invoked independently or as part of the full pipeline.

## Key Highlights

### 7-Factor Fit Scoring Model

Positions are scored with a weighted model that includes career trajectory alignment:

| Factor | Weight | Method |
|--------|--------|--------|
| Required skills | 30% | % of must-haves matched |
| Domain match | 20% | Depth of relevant experience |
| Career trajectory | 15% | Does the role advance your direction? |
| Seniority fit | 15% | Years + scope alignment (penalizes over/under) |
| Preferred skills | 10% | % of nice-to-haves matched |
| Location match | 5% | City > country > remote |
| Education fit | 5% | Meets or exceeds requirements |

### Not-Recommended Detection

Low-scoring positions are evaluated against disqualification patterns before being suggested:

- **Role type mismatch** -- fundamentally different career track
- **Seniority downgrade** -- daily work you outgrew years ago
- **Core skill direction drift** -- ignores your recent specialized investment
- **Career trajectory reversal** -- moves from specialized to generalist scope
- **Overqualified with no upside** -- no growth, title, or compensation match

### Resume Reframing Strategy

The same candidate's experience is repositioned based on the target role's "persona":

| JD Persona | Reframing Focus |
|------------|----------------|
| Platform Engineer | Infrastructure, systems, scalability, API integration |
| QA / SDET | Automation, testing strategy, CI/CD, defect metrics |
| AI + QA Hybrid | Agent architecture AND quality methodology combined |
| Test Infra Builder | From-zero framework construction, tooling, CI/CD platform |
| Domain Expert | Domain depth, architecture knowledge, SME role |
| Tech Lead / Manager | Team building, cross-team coordination, delivery |
| Engineering Manager | Org building (0-to-N), hiring, process design, delivery metrics |
| AI / ML Engineer | AI tools, LLM usage, agent systems, data pipelines |

### Cover Letter Generation

Each role gets a unique narrative anchor -- the same candidate tells different stories:

- **AI agent role**: "I've already built what you're looking to build"
- **Test infra role**: "I've built test infrastructure from zero -- multiple times"
- **Scale role**: "I've ensured quality at massive scale"
- **Team lead role**: "I've built teams and processes from zero during hyper-growth"

### Interview Prep Output

Generates 800-1200 line comprehensive preparation guides covering:

1. Company & Product Knowledge (with architecture diagrams)
2. JD-to-Experience Mapping Table
3. 8-10 STAR Behavioral Stories
4. 20-30 Technical Q&A
5. 2-3 System Design Scenarios
6. Strengths Showcase & Weakness Mitigation
7. Questions to Ask Interviewer
8. Interview Day Checklist

## Utilities

### MD-to-DOCX Conversion

The `scripts/md_to_docx.py` script converts Markdown resumes to professionally formatted DOCX:

```bash
# Requires uv (recommended) or pip-installed python-docx
uv run scripts/md_to_docx.py Resume_Company_Role.md
uv run scripts/md_to_docx.py Resume_Company_Role.md output/resume.docx
```

Features: Calibri font, professional heading hierarchy, table styling, proper page margins.

## Search Platform Notes

The skill prioritizes platforms in this order:

1. **LinkedIn** (public guest access) -- best for English keyword searches
2. **Company career pages** -- direct URL when company is known
3. **Bing search** -- works for English queries
4. **Google search** -- often blocked by CAPTCHA

**China market limitation**: Major Chinese job platforms (BOSS直聘, 拉勾, 猎聘, 脉脉) are fully JS-rendered and cannot be scraped. The skill provides manual search guides with exact keywords and direct URLs as a fallback.

## Bilingual Support

| Scenario | Resume | Cover Letter | Interview Prep |
|----------|--------|-------------|----------------|
| International company, English JD | English | English | English |
| Chinese company, Chinese JD | 中文 | 中文 | 中文 |
| Chinese company, English JD | English | English | Bilingual |
| User explicitly requests language | Follow preference | Follow preference | Follow preference |

## Requirements

- [Devin CLI](https://devin.ai), Windsurf, or Claude Code
- `python-docx` Python package (for MD-to-DOCX conversion; auto-installed by `uv run`)
- Web search / fetch capability (for job searching and company research)

## License

MIT -- Jie Chen (Danna)
