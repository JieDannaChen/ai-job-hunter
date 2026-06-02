---
name: job-hunter
description: >-
  End-to-end job hunting assistant — analyze resume & experience to build a
  candidate profile, search and match job postings, generate role-tailored
  resumes (Markdown + DOCX), and prepare comprehensive interview guides.
  TRIGGER when: user says "find jobs", "optimize resume", "match jobs",
  "prepare interview", "tailor resume for", "analyze JD", "job search",
  "找工作", "优化简历", "匹配岗位", "面试准备", "简历定制", or provides a JD
  and asks for fit analysis.
  DO NOT TRIGGER when: user asks about internal job transfers, HR policies,
  or salary negotiation specifics.
metadata:
  author: dannachen
  version: "1.0.0"
  category: career
  tags: [resume, job-search, interview-prep, career]
---

# Job Hunter — End-to-End Career Toolkit

Analyze resumes, search & match jobs, generate tailored resumes, and prepare
interview guides. Built from real job-hunting workflows producing production
resumes and 900+ line interview prep documents.

## When to Use

- User provides a resume and asks to optimize or review it
- User provides a JD (or URL) and asks for fit analysis
- User asks to find matching jobs based on their skills
- User asks to tailor a resume for a specific position
- User asks to prepare for an interview
- User says "找工作", "优化简历", "匹配岗位", "面试准备"
- User provides multiple JDs and wants a comparison

### Do Not Use When

- User asks about salary negotiation tactics (out of scope)
- User asks about internal transfer processes (company-specific)
- User asks about visa/immigration requirements (legal advice)

---

## Architecture Overview

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
│ Build    │ Score    │ MD → DOCX     │ System design      │
│ profile  │ & rank   │ conversion    │ Weakness plan      │
└──────────┴──────────┴───────────────┴────────────────────┘
```

Each phase can be invoked independently or as part of the full pipeline.

---

## Phase 1: Profile Build — Resume Analysis & Optimization

### Trigger

- "analyze my resume", "optimize resume", "review my experience"
- "优化简历", "分析我的经历"
- User provides a resume file (MD/PDF/DOCX)

### Workflow

```
1. READ RESUME
   → Read the user's resume file (Markdown preferred; PDF/DOCX also supported)
   → If no resume file exists, interview the user to collect experience data

2. EXTRACT STRUCTURED PROFILE
   → Parse into structured sections:
     ┌────────────────────────────────────────────────┐
     │ Identity    : Name, contact, location, langs   │
     │ Experience  : [Company, role, dates, bullets]   │
     │ Skills      : Technical + soft skills matrix    │
     │ Domain Depth: Years × depth per domain          │
     │ Education   : Degrees, certifications           │
     │ Projects    : Key projects with impact metrics  │
     │ Differentiators: Unique strengths               │
     └────────────────────────────────────────────────┘

3. SKILLS MATRIX GENERATION
   → Categorize skills into:
     - Primary skills (5+ years, daily use, deep expertise)
     - Secondary skills (2-5 years, working knowledge)
     - Exposure (< 2 years, familiarity)
   → Map skills to industry-standard job categories

4. STRENGTH & GAP ANALYSIS
   → Identify top 5 differentiators (what makes this candidate unique)
   → Identify potential gaps vs common market expectations
   → Suggest optimization directions

5. OUTPUT: Optimized base resume (Markdown)
   → Professional Summary rewritten for clarity and impact
   → Experience bullets follow STAR+metrics pattern
   → Quantified impact wherever possible (%, time saved, team size, scale)
   → Remove filler words, buzzwords without substance
```

### Resume Quality Checklist

| Criterion | Check |
|-----------|-------|
| **Quantified impact** | Every role has at least 2 bullets with numbers (%, $, time, scale) |
| **Action verbs** | Bullets start with strong verbs: Architected, Led, Designed, Built, Reduced |
| **Recency bias** | Most recent role gets 60%+ of the space; older roles are condensed |
| **Keyword density** | Technical terms match industry standard terminology |
| **Consistency** | Uniform date format, capitalization, punctuation |
| **Length** | 2-3 pages for 10+ years experience; 1-2 pages for < 10 years |
| **No internal jargon** | Employer-internal product names / codenames / project names removed |

### Sanitization Rules

When optimizing a resume for external use, always sanitize employer-internal information:

| Category | Action | Example |
|----------|--------|---------|
| Internal product codenames | Replace with generic description | "Project Phoenix" → "cross-BU converged platform" |
| Internal service names | Use generic functional names | "datasvc-core" → "data service" |
| BU / division codenames | Use "multiple business units" | "Team-A, Team-B, Team-C" → "8 business units" |
| Internal tool names with org prefix | Remove prefix or genericize | "acme-toolkit" → "Enterprise AI Agent Platform" |
| Version-specific internal releases | Use "Release X.Y" | "ProductX 3.4" → "Release 3.4" |
| Keep | Employer name, public awards, public conferences | Employer name, industry conference talks, public awards |

---

## Phase 2: Search & Match — Job Discovery and Scoring

### Trigger

- "find jobs for me", "match my skills to jobs", "search for positions"
- "找工作", "匹配岗位", "帮我搜索职位"
- After Phase 1 profile is built

### Workflow

```
1. DEFINE SEARCH PARAMETERS
   → Ask or infer from profile:
     - Target roles (up to 5 role types)
     - Location preference (city onsite / remote / hybrid)
     - Seniority level (IC vs management, senior vs staff)
     - Industry preferences (if any)
     - Deal-breakers (if any)

2. MULTI-DIMENSIONAL JOB SEARCH
   → Construct 6-8 search queries covering different angles:
     ┌─────────────────────────────────────────────────┐
     │ Query 1: [Primary skill] + [Target role] + [City]│
     │ Query 2: [Domain expertise] + engineer + [City]  │
     │ Query 3: [Secondary skill] + [Alt role] + remote  │
     │ Query 4: [Industry] + [Seniority] + [City]       │
     │ Query 5: Chinese keywords for local platforms     │
     │ Query 6: [Niche skill combination] + hiring       │
     └─────────────────────────────────────────────────┘
   → Use web_search tool for each query
   → Fetch full JD from result URLs via webfetch

3. JD PARSING & NORMALIZATION
   → For each JD, extract:
     - Company, role title, location, remote policy
     - Required skills (must-have)
     - Preferred skills (nice-to-have)
     - Years of experience required
     - Education requirements
     - Key responsibilities
     - Team/product context

4. FIT SCORING
   → Score each position against the candidate profile:

   | Factor           | Weight | Scoring Method                           |
   |------------------|--------|------------------------------------------|
   | Required skills  | 35%    | % of must-haves the candidate has        |
   | Domain match     | 25%    | Depth of relevant domain experience      |
   | Seniority fit    | 15%    | Years + scope alignment                  |
   | Preferred skills | 10%    | % of nice-to-haves                       |
   | Location match   | 10%    | Exact city > same country > remote       |
   | Education fit    | 5%     | Meets or exceeds requirements            |

5. TIER & RANK
   → Classify results:
     - Tier 1 (80%+):  Highly matched — apply immediately
     - Tier 2 (65-79%): Well matched — apply with tailored resume
     - Tier 3 (50-64%): Stretch — apply if interested in growth
     - Below 50%: Skip unless special interest

6. OUTPUT: Ranked job list with analysis
```

### Match Report Format

For each recommended position, output:

```markdown
### [Company] — [Role Title]
**Match Score**: XX% (Tier N)
**Location**: City, Remote/Hybrid/Onsite
**Why It Matches**:
- [Strength 1 mapping to JD requirement]
- [Strength 2 mapping to JD requirement]
**Gaps to Address**:
- [Gap 1 — mitigation strategy]
**Resume Focus Points**:
- [What to emphasize for this role]
- [What to de-emphasize or reframe]
```

---

## Phase 3: Tailor Resume — Per-Role Resume Generation

### Trigger

- "tailor resume for [company/role]", "create resume for [JD]"
- "定制简历", "针对这个岗位优化简历"
- User selects target roles from Phase 2 results

### Workflow

```
1. ANALYZE TARGET JD
   → Deep-read the full JD
   → Extract: required skills, responsibilities, team context, tech stack
   → Identify the "persona" the JD is hiring for

2. DETERMINE REFRAMING STRATEGY
   → Based on JD persona, decide how to reposition the candidate:

   ┌──────────────────────────────────────────────────────┐
   │ JD Persona          │ Reframing Strategy             │
   ├──────────────────────┼────────────────────────────────┤
   │ Platform Engineer    │ Emphasize infra, systems,      │
   │                      │ scalability, API integration    │
   ├──────────────────────┼────────────────────────────────┤
   │ QA / SDET            │ Emphasize automation, testing   │
   │                      │ strategy, CI/CD, defect metrics │
   ├──────────────────────┼────────────────────────────────┤
   │ Domain Expert        │ Emphasize domain depth,         │
   │                      │ architecture knowledge, SME     │
   ├──────────────────────┼────────────────────────────────┤
   │ Tech Lead / Manager  │ Emphasize team building, cross- │
   │                      │ team coordination, delivery     │
   ├──────────────────────┼────────────────────────────────┤
   │ AI / ML Engineer     │ Emphasize AI tools, LLM usage,  │
   │                      │ agent systems, data pipelines   │
   └──────────────────────┴────────────────────────────────┘

3. GENERATE TAILORED RESUME
   → Customize each section:

   TITLE:
   - Match the JD's role title or a close variant
   - Example: same person → "Senior Software Engineer / AI Agent Platform Builder"
     vs "Principal Engineer / Cloud Storage Architect"
     vs "Senior QA Automation Engineer"

   PROFESSIONAL SUMMARY (3-4 sentences):
   - Sentence 1: Years + primary positioning aligned to JD
   - Sentence 2: Strongest proof point (project/achievement matching JD)
   - Sentence 3: Secondary strengths relevant to role
   - Sentence 4: Soft differentiator (communication, global teams, etc.)

   CORE COMPETENCIES (6-8 bullets):
   - Each bullet maps to a JD requirement
   - Format: "**Competency Name** — evidence/proof"
   - Order: highest JD-relevance first

   PROFESSIONAL EXPERIENCE:
   - Most recent role: 60% of space, broken into sub-sections matching JD themes
   - Older roles: condensed to 2-4 bullets each
   - Rewrite bullets to use JD's terminology (not candidate's original words)
   - Every bullet follows: [Action verb] + [What you did] + [Impact/metric]

   KEY PROJECTS (2-3):
   - Select projects most relevant to target role
   - Use table format for scanability
   - Include: Problem, What You Built, Impact, Tech Stack

   TECHNICAL SKILLS:
   - Reorder to put JD-relevant skills first
   - Group into categories matching JD's tech stack
   - Remove irrelevant skills that dilute focus

4. APPLY SANITIZATION RULES (see Phase 1)
   → Remove all employer-internal product names, codenames, service names
   → Keep employer name, public awards, public conferences

5. CONVERT TO DOCX
   → Use python-docx for Markdown → DOCX conversion
   → Professional formatting: Calibri font, proper heading hierarchy
   → Section dividers, table styling, consistent spacing
   → Page margins: 1.5cm top/bottom, 2.0cm left/right

6. OUTPUT:
   → Markdown file: Resume_[Company]_[Role].md
   → DOCX file: Resume_[Company]_[Role].docx
   → Both saved to user's resume directory
```

### Anti-Patterns

| Anti-Pattern | Why It's Bad | Correct Approach |
|-------------|-------------|-----------------|
| Copy-paste same resume for all roles | Fails ATS screening, shows no effort | Tailor title, summary, competencies per role |
| Keep QA/Test title when applying for SWE | Instant rejection bias | Reframe as "Software Engineer" with engineering achievements |
| Include irrelevant domain jargon | Confuses non-domain recruiters | Translate domain terms to generic equivalents |
| List every technology ever used | Dilutes signal | Curate 15-20 most relevant skills per role |
| Lengthy paragraphs | Recruiters scan, not read | Bullet points with bold key phrases |

---

## Phase 4: Interview Prep — Comprehensive Preparation Guide

### Trigger

- "prepare for interview at [company]", "interview prep for [role]"
- "面试准备", "帮我准备面试"
- User has a confirmed interview or target role

### Workflow

```
1. PRODUCT & COMPANY RESEARCH
   → Web search for:
     - Company overview, funding, headcount, culture
     - Product architecture (if public)
     - Tech blog posts, engineering culture articles
     - Recent news, funding rounds, product launches
     - Glassdoor / LinkedIn insights (interview style)
   → Generate a "Company & Product Knowledge" section

2. JD-TO-EXPERIENCE MAPPING
   → Create a detailed mapping table:

   | JD Requirement | Your Experience | Talking Point (30-sec version) |
   |----------------|----------------|-------------------------------|
   | [requirement]  | [experience]   | "At [company], I [action]..." |

   → Classify each requirement:
     - DIRECT MATCH: Strong experience, lead with this
     - TRANSFERABLE: Related experience, draw parallels
     - GAP: No direct experience, show learning ability

3. STAR BEHAVIORAL STORIES (8-10 prepared)
   → Select stories covering these categories:
     ┌──────────────────────────────────────────────┐
     │ Category              │ # Stories             │
     ├───────────────────────┼───────────────────────┤
     │ Technical leadership  │ 2                     │
     │ Cross-team delivery   │ 2                     │
     │ Problem solving       │ 2                     │
     │ Failure & recovery    │ 1                     │
     │ Innovation            │ 1                     │
     │ Conflict resolution   │ 1                     │
     │ Mentoring / growth    │ 1                     │
     └───────────────────────┴───────────────────────┘

   → Each story follows STAR format:
     - Situation: 2-3 sentences of context
     - Task: What was your specific responsibility
     - Action: Step-by-step what YOU did (use "I", not "we")
     - Result: Quantified outcome + what you learned

4. TECHNICAL QUESTIONS & ANSWERS (20-30)
   → Generate questions based on:
     - JD required skills (10-15 questions)
     - JD preferred skills (5-8 questions)
     - System design scenarios (3-5 questions)
     - Candidate's claimed expertise deep-dive (5+ questions)
   → Each answer includes:
     - Concise answer (30 seconds)
     - Extended answer with examples from experience
     - "Bridge" to your strengths

5. SYSTEM DESIGN / WHITEBOARD SCENARIOS (2-3)
   → Design questions relevant to the role:
     - "Design a [system from JD]"
     - "How would you test [product feature]"
     - "Architect a [infrastructure component]"
   → Provide structured approach:
     - Requirements clarification questions to ask
     - High-level architecture diagram (ASCII/Mermaid)
     - Component breakdown
     - Scalability considerations
     - Trade-off discussions

6. STRENGTHS & WEAKNESSES STRATEGY
   → STRENGTHS (3-5):
     - Each strength tied to a JD requirement
     - Backed by a concrete example
     - Format: "[Strength] — proven by [evidence]"

   → WEAKNESSES / GAPS (2-3):
     - Honest gap acknowledgment
     - Mitigation strategy (transferable skill, learning plan, parallel experience)
     - Format: "[Gap] — mitigated by [strategy], already doing [action]"

   → RED FLAG PREPARATION:
     - Anticipate concerns the interviewer might have
     - Prepare proactive responses
     - Example: "You might wonder about my [gap]. Let me address that..."

7. QUESTIONS TO ASK THE INTERVIEWER (8-10)
   → Categories:
     - Team & culture (2-3)
     - Technical depth (2-3)
     - Growth & impact (2-3)
     - Product direction (1-2)
   → Avoid: questions easily answered by website, salary in round 1

8. INTERVIEW DAY CHECKLIST
   → Logistics (time, location, interviewer names)
   → Materials (resume copies, portfolio, notebook)
   → Key talking points (top 3 stories to tell no matter what)
   → Confidence boosters (your 3 strongest differentiators)
```

### Output Format

Generate a comprehensive Interview Preparation Guide as a Markdown file:

```
Interview_Prep_[Company]_[Role].md

Structure:
1. Company & Product Knowledge (with architecture diagram if applicable)
2. JD-to-Experience Mapping Table (with talking points)
3. Behavioral STAR Stories (8-10 prepared answers)
4. Technical Q&A (20-30 questions with answers)
5. System Design Scenarios (2-3 with structured approaches)
6. Strengths Showcase & Weakness Mitigation
7. Questions to Ask Interviewer
8. Interview Day Checklist
```

Target length: 800-1200 lines for a thorough preparation guide.

---

## Parallel Execution Strategy

When the user provides multiple target roles, use subagents for parallelism:

```
User selects 3 roles → Launch 3 background subagents in parallel:
  ├── Subagent 1: Tailor resume for Role A
  ├── Subagent 2: Tailor resume for Role B
  └── Subagent 3: Tailor resume for Role C

Each subagent receives:
  - Full candidate profile (from Phase 1)
  - Full JD text (from Phase 2)
  - Reframing strategy instructions
  - Sanitization rules
  - Output path
```

---

## File Conventions

| Artifact | Naming | Location |
|----------|--------|----------|
| Base resume (EN) | `Resume_Optimized_EN.md` | User's resume directory |
| Base resume (CN) | `简历-优化版.md` | User's resume directory |
| Tailored resume | `Resume_[Company]_[Role_Short].md/.docx` | User's resume directory |
| Interview prep | `Interview_Prep_[Company]_[Role_Short].md` | User's resume directory |
| JD analysis | `JD_Analysis.md` | User's resume directory |

---

## Markdown to DOCX Conversion

Use `python-docx` library (pre-installed) for conversion. Key formatting rules:

| Element | Format |
|---------|--------|
| Page margins | 1.5cm top/bottom, 2.0cm left/right |
| Body font | Calibri 10.5pt |
| H1 (Name) | Calibri 18pt, centered, dark blue (#2C3E50) |
| H2 (Sections) | Calibri 12pt, bold, uppercase, dark blue, bottom border |
| H3 (Roles) | Calibri 11pt, bold, dark blue |
| Bullets | Calibri 10.5pt, 0.25" indent, dark blue dot |
| Tables | Alternating row shading (#F8F9FA), dark header (#2C3E50) |
| Contact line | Calibri 9.5pt, centered, gray (#505050) |

---

## Language Support

This skill supports bilingual operation:

- **English resumes**: Default for international/multinational companies
- **Chinese resumes (简历)**: For domestic Chinese companies or Chinese-language JDs
- **Interview prep**: Generated in the language matching the JD
- **Mixed**: Chinese companies with English JDs get English resume + bilingual interview prep

---

## Examples

### Example 1: Full Pipeline

```
User: "I want to find a new job. Here's my resume: [file path]"

→ Phase 1: Read resume, build profile, identify strengths
→ Phase 2: Search 6-8 queries, fetch JDs, score & rank
→ Present: Tier 1/2/3 matches with analysis
→ User selects: "Tailor for Company A, Company B, Company C"
→ Phase 3: Generate 3 tailored resumes (parallel subagents)
→ Output: 3 × (MD + DOCX) files
→ User: "Prepare me for Company A interview"
→ Phase 4: Generate interview prep guide
→ Output: Interview_Prep_CompanyA_Role.md
```

### Example 2: JD Fit Analysis Only

```
User: "Analyze this JD against my resume: [JD URL or text]"

→ Fetch JD → Parse requirements
→ Score fit (%) → Show match table
→ Identify gaps → Suggest mitigation
→ Recommend: apply / skip / stretch
```

### Example 3: Interview Prep Only

```
User: "I have an interview at NVIDIA for Senior SDET. Help me prepare."

→ Research NVIDIA + product (DGX Cloud, GPU testing, etc.)
→ Map JD requirements to user experience
→ Generate 10 STAR stories + 25 technical Q&A
→ Create system design scenarios
→ Output: 900+ line interview prep document
```
