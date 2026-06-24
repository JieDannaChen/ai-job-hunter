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
