---
name: job-hunter
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
metadata:
  author: dannachen
  version: "2.0.0"
  category: career
  tags: [resume, job-search, interview-prep, cover-letter, career]
---

# Job Hunter — End-to-End Career Toolkit

Analyze resumes, search & match jobs, generate tailored resumes, write targeted
cover letters, and prepare interview guides. Built from real job-hunting
workflows producing production resumes, cover letters, and 900+ line interview
prep documents.

## When to Use

- User provides a resume and asks to optimize or review it
- User provides a JD (or URL) and asks for fit analysis
- User asks to find matching jobs based on their skills
- User asks to tailor a resume for a specific position
- User asks to write a cover letter for a specific role
- User asks to prepare for an interview
- User says "找工作", "优化简历", "匹配岗位", "面试准备", "写求职信"
- User provides multiple JDs and wants a comparison

### Do Not Use When

- User asks about salary negotiation tactics (out of scope)
- User asks about internal transfer processes (company-specific)
- User asks about visa/immigration requirements (legal advice)

---

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
   → Use webfetch tool for each query
   → Fetch full JD from result URLs

   SEARCH PLATFORM PRIORITY & FALLBACK STRATEGY:

   ┌──────────────────────────────────────────────────────────────┐
   │ Priority │ Platform            │ Notes                       │
   ├──────────┼─────────────────────┼─────────────────────────────┤
   │ 1        │ LinkedIn (public)   │ Best for English keywords;  │
   │          │                     │ guest access limited to ~25 │
   │          │                     │ results; use multiple query │
   │          │                     │ variations                  │
   ├──────────┼─────────────────────┼─────────────────────────────┤
   │ 2        │ Company career page │ Direct URL if company known;│
   │          │                     │ many are JS-rendered (blank)│
   ├──────────┼─────────────────────┼─────────────────────────────┤
   │ 3        │ Bing search         │ Works for English queries;  │
   │          │                     │ poor results for Chinese    │
   ├──────────┼─────────────────────┼─────────────────────────────┤
   │ 4        │ Google search       │ Often blocked by CAPTCHA /  │
   │          │                     │ JS redirect; try as backup  │
   └──────────┴─────────────────────┴─────────────────────────────┘

   KNOWN PLATFORM LIMITATIONS (China job market):

   │ Platform         │ Issue                        │ Workaround        │
   ├──────────────────┼──────────────────────────────┼───────────────────┤
   │ BOSS直聘 (Zhipin)│ Fully JS-rendered, webfetch  │ Cannot scrape;    │
   │                  │ returns blank                 │ provide user with │
   │                  │                               │ search keywords   │
   │ 拉勾 (Lagou)     │ JS-rendered                  │ Same as above     │
   │ 猎聘 (Liepin)    │ JS-rendered                  │ Same as above     │
   │ 脉脉 (Maimai)    │ Login-walled                 │ Same as above     │
   │ 字节跳动招聘      │ JS-rendered                  │ Same as above     │
   │ 阿里人才 (Alibaba)│ JS-rendered, API returns 404│ Same as above     │

   FALLBACK: When automated search fails, output a "Manual Search Guide":
   → List specific platforms + exact keyword combinations to try
   → List target companies with direct career page URLs
   → Suggest networking approaches (e.g., 脉脉 for Chinese companies)

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

   | Factor              | Weight | Scoring Method                                  |
   |---------------------|--------|-------------------------------------------------|
   | Required skills     | 30%    | % of must-haves the candidate has               |
   | Domain match        | 20%    | Depth of relevant domain experience              |
   | Career trajectory   | 15%    | Does the role advance the candidate's direction? |
   | Seniority fit       | 15%    | Years + scope alignment (penalize over/under)    |
   | Preferred skills    | 10%    | % of nice-to-haves                               |
   | Location match      | 5%     | Exact city > same country > remote               |
   | Education fit       | 5%     | Meets or exceeds requirements                    |

   CAREER TRAJECTORY SCORING (new dimension):
   → Evaluate whether the role builds on the candidate's recent growth direction
   → High score: Role uses candidate's newest/strongest skills as core requirements
   → Medium score: Role uses candidate's established skills, neutral for growth
   → Low score: Role ignores candidate's recent investments, pulls them backward
   → Zero/Negative: Role is in a fundamentally different career track

5. TIER & RANK
   → Classify results:
     - Tier 1 (80%+):  Highly matched — apply immediately
     - Tier 2 (65-79%): Well matched — apply with tailored resume
     - Tier 3 (50-64%): Stretch — apply if interested in growth
     - Below 50%: Evaluate with NOT-RECOMMENDED check (see below)

6. NOT-RECOMMENDED CHECK
   → Before suggesting "skip", evaluate these disqualification patterns:

   | Pattern                    | Signal                                          | Recommendation         |
   |----------------------------|-------------------------------------------------|------------------------|
   | Role type mismatch         | JD is fundamentally different track              | Do not apply           |
   |                            | (e.g., QA applying for fullstack dev role)       |                        |
   | Severe seniority downgrade | JD requires 3-5 yrs, candidate has 15 yrs;      | Do not apply unless    |
   |                            | daily work would be tasks done 8+ yrs ago        | strategic reason       |
   | Core skill direction drift | Role ignores candidate's last 3 years of         | Do not apply —         |
   |                            | specialized investment (e.g., AI Agent work)      | wastes career capital  |
   | Career trajectory reversal | Moving from specialized/senior track to           | Do not apply           |
   |                            | generalist/junior scope                          |                        |
   | Overqualified with no      | Candidate far exceeds requirements, but role     | Apply only if company  |
   | upside                     | offers no growth, title, or compensation match   | / mission is special   |

   → For not-recommended positions, output:
     - Clear "NOT RECOMMENDED" label with reason category
     - One-paragraph explanation of why it's a poor fit
     - What the candidate would lose by taking this role
     - What type of role they should look for instead

7. OUTPUT: Ranked job list with analysis
```

### Match Report Format

For each recommended position, output:

```markdown
### [Company] — [Role Title]
**Match Score**: XX% (Tier N)
**Location**: City, Remote/Hybrid/Onsite
**Career Direction**: Advances / Neutral / Regresses candidate's trajectory
**Why It Matches**:
- [Strength 1 mapping to JD requirement]
- [Strength 2 mapping to JD requirement]
**Gaps to Address**:
- [Gap 1 — mitigation strategy]
**Resume Focus Points**:
- [What to emphasize for this role]
- [What to de-emphasize or reframe]
```

For not-recommended positions:

```markdown
### [Company] — [Role Title]
**Match Score**: XX% | NOT RECOMMENDED
**Reason**: [Role type mismatch / Seniority downgrade / Direction drift / ...]
**Analysis**: [1-2 sentence explanation]
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

   ┌──────────────────────────────────────────────────────────────┐
   │ JD Persona              │ Reframing Strategy                 │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Platform Engineer       │ Emphasize infra, systems,          │
   │                         │ scalability, API integration        │
   ├─────────────────────────┼────────────────────────────────────┤
   │ QA / SDET               │ Emphasize automation, testing      │
   │                         │ strategy, CI/CD, defect metrics     │
   ├─────────────────────────┼────────────────────────────────────┤
   │ AI + QA Hybrid          │ Emphasize BOTH agent architecture  │
   │                         │ AND quality methodology; show how   │
   │                         │ AI skills enhance testing practice  │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Test Infra Builder      │ Emphasize from-zero framework      │
   │                         │ construction, tooling development,  │
   │                         │ CI/CD platform, coverage systems    │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Domain Expert           │ Emphasize domain depth,            │
   │                         │ architecture knowledge, SME role    │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Tech Lead / Manager     │ Emphasize team building, cross-    │
   │                         │ team coordination, delivery scope   │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Engineering Manager     │ Emphasize org building (0→N),      │
   │                         │ hiring, process design, delivery    │
   │                         │ metrics, cross-org influence        │
   ├─────────────────────────┼────────────────────────────────────┤
   │ AI / ML Engineer        │ Emphasize AI tools, LLM usage,     │
   │                         │ agent systems, data pipelines       │
   └─────────────────────────┴────────────────────────────────────┘

3. GENERATE TAILORED RESUME
   → Customize each section:

   TITLE:
   - Match the JD's role title or a close variant
   - Example: same person →
     "Senior Software Engineer / AI Agent Platform Builder"
     vs "Principal Engineer / Cloud Storage Architect"
     vs "Senior QA Automation Engineer"
     vs "质量工程专家 — AI 测试智能体 / 测试平台架构"

   PROFESSIONAL SUMMARY (3-4 sentences):
   - Sentence 1: Years + primary positioning aligned to JD
   - Sentence 2: Strongest proof point (project/achievement matching JD)
   - Sentence 3: Secondary strengths relevant to role
   - Sentence 4: Soft differentiator (communication, global teams, etc.)

   JD ALIGNMENT TABLE (for Chinese resumes / JDs with many requirements):
   - Create a "核心能力 — JD对标" table mapping each JD requirement to
     the candidate's matching experience
   - This is especially effective for Chinese tech company applications
     where HR scans for keyword alignment

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
   → Use scripts/md_to_docx.py or inline python-docx for conversion
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

## Phase 4: Cover Letter — Targeted Narrative Generation

### Trigger

- "write cover letter for [company/role]", "cover letter for [JD]"
- "写求职信", "帮我写求职信给[公司]"
- After Phase 3 resume is generated (or independently with a JD)

### Workflow

```
1. DETERMINE NARRATIVE ANCHOR
   → The SAME candidate must tell a DIFFERENT story for each role.
   → Read the JD and identify the single most important theme:

   ┌──────────────────────────────────────────────────────────────┐
   │ JD Theme                │ Narrative Anchor                   │
   ├─────────────────────────┼────────────────────────────────────┤
   │ AI / Agent systems      │ "I've already built what you're    │
   │                         │ looking to build"                   │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Test infra / tooling    │ "I've built test infrastructure    │
   │                         │ from zero — multiple times"         │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Scale / distributed     │ "I've ensured quality at massive   │
   │                         │ scale (N users, M services)"        │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Team building           │ "I've built teams and processes    │
   │                         │ from zero during hyper-growth"      │
   ├─────────────────────────┼────────────────────────────────────┤
   │ Product / consumer      │ "I've shipped consumer products    │
   │                         │ where quality = user delight"       │
   ├─────────────────────────┼────────────────────────────────────┤
   │ 中文 — AI智能体         │ "用AI大模型打造测试智能体，正是我    │
   │                         │ 过去3年一直在做的事"                 │
   ├─────────────────────────┼────────────────────────────────────┤
   │ 中文 — 质量/测试平台     │ "多次从零搭建自动化框架与CI/CD      │
   │                         │ 平台，覆盖全球工程团队"              │
   └─────────────────────────┴────────────────────────────────────┘

2. SELECT STORIES (2-3 max)
   → Pick the 2-3 experiences that most directly prove the narrative anchor
   → Each story must include: what you built + quantified impact
   → DO NOT repeat resume content verbatim — provide depth and context
     that a resume cannot convey

3. STRUCTURE

   ENGLISH COVER LETTER:
   ┌─────────────────────────────────────────────────────────┐
   │ Header: Name, contact, date                             │
   │                                                         │
   │ Opening (2-3 sentences):                                │
   │   Hook — state your anchor narrative                    │
   │   Briefly connect your background to their need         │
   │                                                         │
   │ Body — "What I bring" (2-3 paragraphs):                 │
   │   Story 1: Most relevant achievement (with metrics)     │
   │   Story 2: Second proof point (different dimension)     │
   │   Optional Story 3: If JD has 3+ distinct requirements  │
   │                                                         │
   │ "Why this role / company" (1 paragraph):                │
   │   What specifically draws you — must be genuine, not    │
   │   generic. Reference specific product, team, mission.   │
   │   Connect to your own motivations.                      │
   │                                                         │
   │ Closing (2-3 sentences):                                │
   │   Summarize value proposition in one line               │
   │   Express interest, invite discussion                   │
   └─────────────────────────────────────────────────────────┘

   中文求职信:
   ┌─────────────────────────────────────────────────────────┐
   │ 称呼: [公司名] 招聘团队/[具体部门]                        │
   │                                                         │
   │ 开头 (2-3句):                                           │
   │   直接点题 — 你和这个岗位的核心连接点                      │
   │                                                         │
   │ 主体 — "我的匹配优势" (2-3段):                           │
   │   故事1: 最相关的项目/成果（含数据）                       │
   │   故事2: 第二维度的证明                                   │
   │                                                         │
   │ "为什么选择贵司" (1段):                                   │
   │   具体提到产品/技术/团队，不要泛泛而谈                     │
   │                                                         │
   │ 结尾 (1-2句):                                           │
   │   一句话总结价值主张，表达期待                             │
   └─────────────────────────────────────────────────────────┘

4. TONE CALIBRATION
   → Match cover letter tone to company culture:

   | Company Type             | Tone                                        |
   |--------------------------|---------------------------------------------|
   | Big tech (Google, MSFT)  | Direct, data-driven, no fluff               |
   | AI startup               | Builder mindset, 0-to-1, move fast          |
   | Enterprise (Dell, SAP)   | Professional, structured, process-aware      |
   | Education (EF, Crimson)  | Mission-driven, user empathy + technical     |
   | 中国大厂 (阿里/字节/美团) | 结果导向、数据说话、突出业务理解              |
   | 中国AI创业公司            | 强调动手能力、从零到一、技术深度              |

5. ANTI-PATTERNS

   | Anti-Pattern                       | Why It Fails                           |
   |------------------------------------|----------------------------------------|
   | Repeating resume bullets verbatim  | Adds no value; reader already has CV   |
   | Generic "I'm passionate about..."  | Every applicant says this              |
   | Listing all skills/technologies    | Cover letter is narrative, not a list  |
   | > 1 page                           | Nobody reads a 2-page cover letter     |
   | Not mentioning the company by name | Shows you're mass-sending              |
   | 中文求职信直译英文模板              | 语气不自然，不符合中文商务写作习惯       |

6. OUTPUT:
   → CoverLetter_[Company]_[Role].md
   → Saved to user's resume directory
   → Target length: 350-500 words (EN) / 400-600字 (CN)
```

---

## Phase 5: Interview Prep — Comprehensive Preparation Guide

### Trigger

- "prepare for interview at [company]", "interview prep for [role]"
- "面试准备", "帮我准备面试", "帮我准备[公司]的面试"
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

### Example 1: Full Pipeline

```
User: "I want to find a new job. Here's my resume: [file path]"

→ Phase 1: Read resume, build profile, identify strengths
→ Phase 2: Search 6-8 queries, fetch JDs, score & rank
→ Present: Tier 1/2/3 matches with analysis
→ User selects: "Tailor for Company A, Company B, Company C"
→ Phase 3: Generate 3 tailored resumes (parallel subagents)
→ Output: 3 × (MD + DOCX) files
→ User: "Write cover letter for Company A"
→ Phase 4: Generate targeted cover letter
→ Output: CoverLetter_CompanyA_Role.md
→ User: "Prepare me for Company A interview"
→ Phase 5: Generate interview prep guide
→ Output: Interview_Prep_CompanyA_Role.md
```

### Example 2: JD Fit Analysis Only

```
User: "Analyze this JD against my resume: [JD URL or text]"

→ Fetch JD → Parse requirements
→ Score fit (7-factor model) → Show match table
→ Evaluate career trajectory alignment
→ Identify gaps → Suggest mitigation
→ Recommend: apply / stretch / NOT RECOMMENDED (with reason)
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

### Example 4: 中文全流程

```
User: "帮我分析这个千问的测试智能体岗位是否匹配，并定制简历"

→ 解析JD → 提取技能要求、职责、团队背景
→ 7因子评分 → 匹配度80-85% (Tier 1)
→ 职业方向评估: 高度一致（AI测试智能体正是候选人核心方向）
→ 生成定制中文简历:
   - 标题: "质量工程专家 — AI测试智能体 / 测试平台架构"
   - 新增 "核心能力—JD对标" 表格
   - 按JD主题重组工作经历
→ 输出: Resume_Qwen_Test_Agent_Engineer.md + .docx

User: "帮我写一封求职信"
→ 叙事锚点: "用AI大模型打造测试智能体，正是我过去3年一直在做的事"
→ 选择故事: AI测试平台(87技能) + Coverage-to-Robot(效率95%)
→ 输出: 求职信_千问_测试智能体.md
```

### Example 5: Not-Recommended Analysis

```
User: "帮我分析这个岗位是否匹配: [Fullstack Developer JD]"

→ 解析JD → 核心要求: React/Node.js全栈开发, 4+年产品开发经验
→ 7因子评分 → 15-20%
→ NOT RECOMMENDED 判定:
   - 原因: 岗位类型错配
   - 分析: "这是一个全栈开发岗，不是测试/质量岗。即使你技术上能做，
     投这个岗位等于放弃15年质量工程积累。"
   - 建议: "继续聚焦AI测试智能体/LLM评测方向的岗位"
```
