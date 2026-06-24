---
name: ai-job-hunter
description: >-
  End-to-end job hunting assistant — analyze resume & experience to build a
  candidate profile, search and match job postings, generate role-tailored
  resumes (Markdown + DOCX), write targeted cover letters, and prepare
  comprehensive interview guides.
  TRIGGER when: user says "find jobs", "optimize resume", "match jobs",
  "prepare interview", "tailor resume for", "analyze JD", "job search",
  "write cover letter", "cover letter for",
  "找工作", "优化简历", "匹配岗位", "面试准备", "简历定制", "写求职信",
  or provides a JD and asks for fit analysis.
  DO NOT TRIGGER when: user asks about internal job transfers, HR policies,
  or salary negotiation specifics.
---

# Job Hunter — End-to-End Career Toolkit

Analyze resumes, search & match jobs, generate tailored resumes, write targeted
cover letters, and prepare interview guides. Built from real job-hunting
workflows producing production resumes, cover letters, and 900+ line interview
prep documents.

## Architecture Overview

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
│ Build    │ Score    │ MD → DOCX    │ Tone match   │ System design     │
│ profile  │ & rank   │ conversion   │ EN / CN      │ Weakness plan     │
└──────────┴──────────┴──────────────┴──────────────┴───────────────────┘
```

Each phase can be invoked independently or as part of the full pipeline.

---

## Phase 1: Profile Build — Resume Analysis & Optimization

### Trigger
- "analyze my resume", "optimize resume", "review my experience"
- "优化简历", "分析我的经历"
- User provides a resume file (MD/PDF/DOCX)

### Workflow
1. READ RESUME → Read the user's resume file
2. EXTRACT STRUCTURED PROFILE → Parse into identity, experience, skills, etc.
3. SKILLS MATRIX GENERATION → Categorize skills by proficiency
4. STRENGTH & GAP ANALYSIS → Identify differentiators and improvement areas
5. OUTPUT: Optimized base resume (Markdown)

**详细规则见**: [references/resume-optimization.md](references/resume-optimization.md)

---

## Phase 2: Search & Match — Job Discovery and Scoring

### Trigger
- "find jobs for me", "match my skills to jobs", "search for positions"
- "找工作", "匹配岗位", "帮我搜索职位"
- After Phase 1 profile is built

### Workflow
1. DEFINE SEARCH PARAMETERS → Infer or ask for role, location, seniority, etc.
2. MULTI-DIMENSIONAL JOB SEARCH → 6-8 queries across platforms, fetch JDs
3. JD PARSING & NORMALIZATION → Extract requirements, context, responsibilities
4. FIT SCORING → 7-factor weighted scoring against candidate profile
5. TIER & RANK → Classify into Tier 1/2/3 or Not Recommended
6. OUTPUT: Ranked job list with match analysis

**详细规则见**: [references/job-search.md](references/job-search.md)

---

## Phase 3: Tailor Resume — Per-Role Resume Generation

### Trigger
- "tailor resume for [company/role]", "create resume for [JD]"
- "定制简历", "针对这个岗位优化简历"
- User selects target roles from Phase 2 results

### Workflow
1. ANALYZE TARGET JD → Deep-read to identify hiring persona
2. DETERMINE REFRAMING STRATEGY → Align experience to JD requirements
3. RESTRUCTURE EXPERIENCE → Reorder, reframe, and prioritize relevant content
4. SANITIZE INTERNAL INFO → Remove company-specific codenames and jargon
5. CONVERT TO DOCX → Generate professionally formatted DOCX file
6. OUTPUT: Tailored resume (MD + DOCX)

**详细规则见**: [references/resume-tailoring.md](references/resume-tailoring.md)

---

## Phase 4: Cover Letter — Targeted Narrative Generation

### Trigger
- "write cover letter for [company/role]", "cover letter for [JD]"
- "写求职信", "帮我写求职信给[公司]"
- After Phase 3 resume is generated (or independently with a JD)

### Workflow
1. DETERMINE NARRATIVE ANCHOR → Identify core connection to the role
2. SELECT STORIES → 2-3 most relevant achievements to prove the anchor
3. STRUCTURE NARRATIVE → Follow EN/CN format conventions
4. CALIBRATE TONE → Match company culture and industry norms
5. OUTPUT: Targeted cover letter (Markdown)

**详细规则见**: [references/cover-letter.md](references/cover-letter.md)

---

## Phase 5: Interview Prep — Comprehensive Preparation Guide

### Trigger
- "prepare for interview at [company]", "interview prep for [role]"
- "面试准备", "帮我准备面试", "帮我准备[公司]的面试"
- User has a confirmed interview or target role

### Workflow
1. PRODUCT & COMPANY RESEARCH → Gather context on company, culture, product
2. JD-TO-EXPERIENCE MAPPING → Create talking points for each requirement
3. STAR BEHAVIORAL STORIES → 8-10 prepared stories across key categories
4. TECHNICAL QUESTIONS & ANSWERS → 20-30 role-specific Q&A
5. SYSTEM DESIGN SCENARIOS → Structured approaches for relevant design questions
6. STRENGTHS & WEAKNESSES STRATEGY → Prepare showcase and mitigation points
7. QUESTIONS TO ASK INTERVIEWER → Curated list of thoughtful questions
8. OUTPUT: Comprehensive interview preparation guide

**详细规则见**: [references/interview-prep.md](references/interview-prep.md)

---

## Parallel Execution Strategy

When the user provides multiple target roles, use subagents for parallelism:
```
User selects 3 roles → Launch 3 background subagents in parallel:
  ├── Subagent 1: Tailor resume for Role A
  ├── Subagent 2: Tailor resume for Role B
  └── Subagent 3: Tailor resume for Role C
```

---

## Additional Resources

- **Formatting & Naming Conventions**: [references/formatting.md](references/formatting.md)
- **Usage Examples**: [references/examples.md](references/examples.md)
- **Scripts**: `scripts/md_to_docx.py` for Markdown to DOCX conversion
