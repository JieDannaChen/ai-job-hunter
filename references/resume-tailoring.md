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
