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
