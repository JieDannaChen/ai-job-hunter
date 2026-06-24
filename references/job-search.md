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
