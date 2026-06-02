# AI Job Hunter

An end-to-end job hunting skill for [Devin CLI](https://devin.ai) and compatible AI coding assistants. Analyze resumes, search & match jobs, generate role-tailored resumes, and prepare comprehensive interview guides.

## Features

| Phase | Capability | Description |
|-------|-----------|-------------|
| **1. Profile Build** | Resume Analysis & Optimization | Parse resume, extract skills matrix, identify strengths/gaps, generate optimized base resume |
| **2. Search & Match** | Job Discovery & Scoring | Multi-dimensional web search, JD parsing, 6-factor weighted fit scoring, tiered ranking |
| **3. Tailor Resume** | Per-Role Resume Generation | Persona-based reframing, section-by-section customization, internal info sanitization, MD-to-DOCX conversion |
| **4. Interview Prep** | Comprehensive Preparation | Company research, JD-experience mapping, STAR behavioral stories, technical Q&A, system design scenarios, weakness mitigation |

## Quick Start

### Installation

Copy the skill directory to your Devin CLI skills folder:

```bash
# Global (available in all projects)
# Linux/macOS:
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
| English | "find jobs", "optimize resume", "tailor resume for [company]", "prepare interview" |
| Chinese | "找工作", "优化简历", "定制简历", "面试准备" |

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    JOB HUNTER SKILL                       │
├──────────┬──────────┬───────────────┬────────────────────┤
│ Phase 1  │ Phase 2  │   Phase 3     │     Phase 4        │
│ PROFILE  │ SEARCH   │   TAILOR      │     INTERVIEW      │
│ BUILD    │ & MATCH  │   RESUME      │     PREP           │
├──────────┼──────────┼───────────────┼────────────────────┤
│ Read     │ Web      │ Per-role      │ Product research   │
│ resume   │ search   │ resume gen    │ JD gap analysis    │
│ Extract  │ JD fetch │ Sanitize      │ STAR stories       │
│ skills   │ & parse  │ internal info │ Tech Q&A           │
│ Build    │ Score    │ MD -> DOCX    │ System design      │
│ profile  │ & rank   │ conversion    │ Weakness plan      │
└──────────┴──────────┴───────────────┴────────────────────┘
```

Each phase can be invoked independently or as part of the full pipeline.

## Key Highlights

### Fit Scoring Model

Positions are scored with a 6-factor weighted model:

| Factor | Weight | Method |
|--------|--------|--------|
| Required skills | 35% | % of must-haves matched |
| Domain match | 25% | Depth of relevant experience |
| Seniority fit | 15% | Years + scope alignment |
| Preferred skills | 10% | % of nice-to-haves matched |
| Location match | 10% | City > country > remote |
| Education fit | 5% | Meets or exceeds requirements |

### Resume Reframing Strategy

The same candidate's experience is repositioned based on the target role's "persona":

| JD Persona | Reframing Focus |
|------------|----------------|
| Platform Engineer | Infrastructure, systems, scalability, API integration |
| QA / SDET | Automation, testing strategy, CI/CD, defect metrics |
| Domain Expert | Domain depth, architecture knowledge, SME role |
| Tech Lead / Manager | Team building, cross-team coordination, delivery |
| AI / ML Engineer | AI tools, LLM usage, agent systems, data pipelines |

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

## Requirements

- [Devin CLI](https://devin.ai), Windsurf, or Claude Code
- `python-docx` Python package (for MD-to-DOCX conversion)
- Web search capability (for job searching and company research)

## Bilingual Support

- **English resumes** for international/multinational companies
- **Chinese resumes (简历)** for domestic Chinese companies
- **Interview prep** generated in the language matching the JD

## License

MIT
