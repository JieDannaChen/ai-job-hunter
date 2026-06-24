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
