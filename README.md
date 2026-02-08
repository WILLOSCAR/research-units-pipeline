# research-units-pipeline-skills

> **一句话**：让 Pipeline 会"带人 / 带模型"做研究——不是给一堆脚本，而是给一套**语义化的 skills**，每个 skill 知道"该做什么、怎么做、做到什么程度、不能做什么"。

English version: [`README.en.md`](README.en.md).  
Skills index: [`SKILL_INDEX.md`](SKILL_INDEX.md).  
Skill/Pipeline standard: [`SKILLS_STANDARD.md`](SKILLS_STANDARD.md).


## 核心设计：Skills-First + 拆解链路 + 证据先行

这类工作最容易陷入两种极端：
- **只有脚本**：能跑，但失败时很难知道“该改哪里”。
- **只有文档**：看起来都对，但执行时仍靠经验，容易漂移。

本仓库的做法：把“写一篇 survey”拆成一串**可验收、可恢复**的小步，并把每一步的中间产物写到磁盘上。

1) **Skill：带验收的步骤说明书**
- 每个 skill 都写清楚 `inputs / outputs / acceptance / guardrail`：需要什么、产出什么、做到什么程度、哪些行为禁止（例如 C2–C4 **NO PROSE**）。

2) **Unit：一次运行里的一个小任务**
- `UNITS.csv` 一行一个 unit（依赖 + 输入/输出 + 验收）。
- 卡住时看报告定位到具体文件；修完从卡住的 unit 继续，不需要全重跑。

3) **证据先行：先准备“可写材料”，再写作**
- C1 找论文 → C2 定结构 → C3/C4 做证据与引用 → C5 写作/合并/审计/出 PDF。

一眼看懂（你想解决什么，就先看哪里）：

| 你想解决的问题 | 优先看哪里 | 常见修复动作 |
|---|---|---|
| 论文太少 / 覆盖不足 | `queries.md` + `papers/retrieval_report.md` | 扩关键词桶、提高 `max_results`、导入离线集合、做 snowball |
| 大纲不稳 / 小节没论文可写 | `outline/outline.yml` + `outline/mapping.tsv` | 合并/重排小节、提高 `per_subsection`、重跑 mapping |
| 证据薄导致写作空洞 | `papers/paper_notes.jsonl` + `outline/evidence_drafts.jsonl` | 补 notes / 补 evidence packs（先补证据，再写作） |
| 写作出现模板话/口癖/越写越冗余 | `output/WRITER_SELFLOOP_TODO.md` + `output/PARAGRAPH_CURATION_REPORT.md` + `sections/*` | 定点改写（并行候选→择优融合；去旁白/去导航/融合冗余段），再跑自检门 |
| 引用密度不够（unique 偏低） | `output/CITATION_BUDGET_REPORT.md` + `citations/ref.bib` | 按预算做 in-scope 注入（NO NEW FACTS） |

## codex 参考配置
配置可能会根据 codex 的更新有变化
```toml

[sandbox_workspace_write]
network_access = true

[features]
shell_snapshot = true
```


## 30 秒上手（从 0 到 PDF）

1) 在本仓库目录启动 Codex：

```bash
codex --sandbox workspace-write --ask-for-approval never
```

2) 在对话里说一句话（例子）：

```
帮我写一篇关于 LLM agents 的 LaTeX survey
```

3) 接下来会发生什么：
- 它会在 `workspaces/` 下新建一个带时间戳的文件夹，把所有结果都放进去。
- 它会先给你一份“大纲 + 每个小节要参考哪些论文”，然后停下来等你确认。
- 你回复“同意继续”，它才会开始写正文，并在最后生成 PDF。

4) 跑完后你最常看的 3 个文件：
- 草稿（Markdown）：`workspaces/<…>/output/DRAFT.md`
- PDF：`workspaces/<…>/latex/main.pdf`
- 质量报告：`workspaces/<…>/output/AUDIT_REPORT.md`

5) 如果卡住了，先看这两个文件：
- `workspaces/<…>/output/QUALITY_GATE.md`（为什么停、下一步该改什么）
- `workspaces/<…>/output/RUN_ERRORS.md`（脚本/缺文件等运行问题）

备注（可选，但更稳）：
- 你可以显式指定跑哪条流程：`pipelines/arxiv-survey-latex.pipeline.md`（需要 PDF 就用它）
- 想一次跑完（不在大纲处停）：请在那句话里补一句类似“跳过大纲确认 / 自动同意大纲 / 无需停在 outline 处确认，直接继续执行到成稿”的指令。

术语速查（只看这 3 个就够）：
- workspace：一次运行的输出目录（`workspaces/<name>/`）
- C2：大纲确认点；不确认就不会写正文
- strict：开启质量门；不达标会停下来，并在 `output/QUALITY_GATE.md` 写明原因与下一步

下面的“详细版”会解释每一步会产出哪些中间文件，以及写作阶段如何逐步润色与收敛。

## 详细版：对话式执行（从 0 到 PDF）

你在对话里通常会这样说（例子）：

> 帮我写一篇关于 LLM agents 的 LaTeX survey

然后会按阶段推进（每一步都会把结果写到 workspace 里；默认会在 C2 停下来等你确认）：

### [C0] 初始化一次 run（只做“建目录 + 写配置”，不写正文）

- 会在 `workspaces/` 下新建一个时间戳目录，把后续所有产物都放进去。
- 同时写入基础清单（比如 `UNITS.csv` / `DECISIONS.md` / `queries.md`），让这次 run 可追踪、可恢复。

### [C1] 找论文（先把“论文池子”做扎实）

- 目标：先拿到一个够大的候选池（`max_results=1800`/桶；去重后目标 `>=1200`），再选出 core set（默认 `300` 篇，写入 `papers/core_set.csv`）。
- 做法（简述）：把主题拆成多条 query bucket（同义词/缩写/子方向）分别检索 → 合并 → 去重。
  - 结果太少：补 bucket（例如“agent / tool use / planning / memory / reflection / evaluation”），或提高 `max_results`。
  - 结果太吵：改写关键词 + 加排除词（例如排除无关领域），再跑一次。
- 产物：`papers/core_set.csv` + `papers/retrieval_report.md`

### [C2] 给你看大纲（不写正文；默认会停在这里等你确认）

- 你主要看：
  - `outline/outline.yml`
  - `outline/mapping.tsv`（每个小节默认映射 `28` 篇）
  - （可选）`outline/coverage_report.md`（覆盖率/重复引用预警）
- 你确认后回复：`同意继续`
  - 如果你想一次跑完：也可以在第一句话里说“自动同意大纲 / 跳过大纲确认”。
- 你看大纲时，通常只抓两件事就够了：
  1) 结构是否“少而厚”（不要为了覆盖而把小节拆得太碎）
  2) 每个小节是否真的“有论文可写”（mapping 不是摆设：它决定后面写作允许用哪些引用）

### [C3-C4] 整理成“可写材料”（不写正文）

- 这一段的目标很简单：把“读论文”变成“能直接写进正文的材料”，但仍然 **不写正文段落**。
- `papers/paper_notes.jsonl`：每篇论文的要点/结果/局限（写作会反复用到）
- `citations/ref.bib`：参考文献表（正文里能引用的 key）
- `outline/writer_context_packs.jsonl`：每个小节的写作包（该写哪些对比点 + 能用哪些引用）
- （表格）`outline/tables_index.md` 是内部索引；`outline/tables_appendix.md` 是面向读者的 Appendix 表格

### [C5] 写作与输出（都在 C5 内反复迭代）

1) 先写分小节文件：`sections/*.md`
   - 先写主体，再写开头：先把各小节内容铺开，最后统一回头重写开头，减少“模板开头牵着全文走”。
   - 一般包含：摘要/引言/相关工作 + 章节导语 + 各小节正文

2) 再做“自检 + 收敛”（只修失败项，逐步润色）：
   - 写作门：`output/WRITER_SELFLOOP_TODO.md`（补结论句/对比/评测锚点/局限；去模板开头）
   - 段落逻辑门：`output/SECTION_LOGIC_REPORT.md`（补桥接、重排段落，消灭“段落孤岛”）
   - 论证与口径门：`output/ARGUMENT_SELFLOOP_TODO.md`（口径单一真源：`output/ARGUMENT_SKELETON.md`）
   - 选段融合收敛：`output/PARAGRAPH_CURATION_REPORT.md`（多候选→择优/融合，防止“越写越长”）

3) 去口癖/去模板化（收敛后再做）：`style-harmonizer` + `opener-variator`（best-of-N）

4) 合并成草稿并做终稿检查：`output/DRAFT.md`
   - 如果引用不够：`output/CITATION_BUDGET_REPORT.md` → `output/CITATION_INJECTION_REPORT.md`
   - 最终审计：`output/AUDIT_REPORT.md`
   - LaTeX pipeline 还会生成：`latex/main.pdf`

目标：
- 全局 unique citations 推荐 `>=165`（不足会触发“引用预算/注入”补齐）

如果卡住了：
- strict 拦住：看 `output/QUALITY_GATE.md`（最后一条就是原因 + 下一步）
- 运行问题：看 `output/RUN_ERRORS.md`

恢复执行：
- 按报告修复对应文件后说「继续」→ 从卡住的那一步继续跑，不需要全部重跑

**关键原则**：C2-C4 强制 NO PROSE，先建证据底座；C5 才写作，失败时可定点修复中间产物。

## 示例产物（v0.1：一整条链路的对照样例）
这是一个“完整跑通”的示例目录：从找论文 → 出大纲 → 整理证据与引用 → 分小节写作 → 合并成稿 → 编译 PDF。  
你可以把它当成“对照答案”：当你自己的 run 卡住时，直接去对照同名文件（或同一个文件夹）通常最快。

- 示例路径：`example/e2e-agent-survey-latex-verify-<时间戳>/`（对应流程：`pipelines/arxiv-survey-latex.pipeline.md`）
- 过程中会在 **C2（大纲）** 停下来等你确认；确认后才会写正文
- 默认配置（A150++）：核心论文 300 篇、每个小节映射 28 篇、证据模式用 abstract（摘要级）；目标是全局引用足够密（全局 unique citations 默认收敛到推荐值）
- 一般建议：`draft_profile: survey`（默认交付）；想更严格再用 `draft_profile: deep`

建议从这里开始看示例（按顺序打开）：
- `example/e2e-agent-survey-latex-verify-<最新时间戳>/output/AUDIT_REPORT.md`：是否 PASS + 关键指标（引用数、模板话、缺小节等）
- `example/e2e-agent-survey-latex-verify-<最新时间戳>/latex/main.pdf`：最终 PDF 效果（如果你用的是 LaTeX pipeline）
- `example/e2e-agent-survey-latex-verify-<最新时间戳>/output/DRAFT.md`：合并后的正文（和 PDF 内容对应）

如果你想看“写作是怎么逐步变好”的：
- 正文原始素材在 `sections/`（按小节拆分，便于逐个修）
- 每轮自检/收敛的报告在 `output/`（例如 `WRITER_SELFLOOP_TODO.md` / `SECTION_LOGIC_REPORT.md` / `ARGUMENT_SELFLOOP_TODO.md` / `PARAGRAPH_CURATION_REPORT.md`）

目录速览（每个文件夹干嘛用）：

```text
example/e2e-agent-survey-latex-verify-<最新时间戳>/
  STATUS.md           # 进度与执行日志（当前 checkpoint）
  UNITS.csv           # 执行合约（一行一个 unit：依赖/验收/产物）
  DECISIONS.md        # 人类检查点（最关键：C2 大纲审批）
  CHECKPOINTS.md      # checkpoint 规则
  PIPELINE.lock.md    # 选中的 pipeline（单一真相源）
  GOAL.md             # 目标/范围 seed
  queries.md          # 检索与写作档位配置（例如 core_size / per_subsection）
  papers/             # 检索结果 + 论文“底座”（core set / paper notes / evidence bank）
  outline/            # 结构与写作素材（outline/mapping + briefs + evidence packs + tables）
  citations/          # BibTeX 与 verification 记录
  sections/           # 分小节草稿（便于按 unit 定点修）
  output/             # 合并后的草稿 + QA 报告（质量门/审计/引用预算…）
  latex/              # LaTeX scaffold + 编译产物（main.pdf；只有 LaTeX pipeline 才有）
```

注：`outline/tables_index.md` 是内部索引表（中间产物）；`outline/tables_appendix.md` 是面向读者的 Appendix 表格。

文件夹之间的“流水线关系”：

```mermaid
flowchart LR
  WS["workspaces/{run}/"]
  WS --> RAW["papers/papers_raw.jsonl"]
  RAW --> DEDUP["papers/papers_dedup.jsonl"]
  DEDUP --> CORE["papers/core_set.csv"]
  CORE --> STRUCT["outline/outline.yml + outline/mapping.tsv"]
  STRUCT -->|Approve C2| EVID["C3-C4：paper_notes + evidence packs"]
  EVID --> PACKS["C4：writer_context_packs.jsonl + citations/ref.bib"]
  PACKS --> SECS["sections/（分小节草稿）"]
  SECS --> G["C5 自检门（writer/logic/argument/style）"]
  G --> DRAFT["output/DRAFT.md"]
  DRAFT --> AUDIT["output/AUDIT_REPORT.md"]
  AUDIT --> PDF["latex/main.pdf（可选）"]

  G -.->|"没通过 → 回到 sections/"| SECS
  AUDIT -.->|"没通过 → 回到 sections/"| SECS
```

交付时只关注**最新时间戳**的示例目录（默认保留 2–3 个历史目录用于回归对比）：

- Markdown 草稿：`example/e2e-agent-survey-latex-verify-<最新时间戳>/output/DRAFT.md`
- PDF 输出：`example/e2e-agent-survey-latex-verify-<最新时间戳>/latex/main.pdf`
- QA 审计报告：`example/e2e-agent-survey-latex-verify-<最新时间戳>/output/AUDIT_REPORT.md`


## 欢迎提出各类 issue，一起改进写作流程

### WIP
1. best of N 写作
### Todo
1. 加入多 cli 协作，multi-agent design （在合适的环节接入 API，替代或者分担 codex 执行过程中的压力）
2. 完善剩余的Pipeline，example 新增例子
3. 精简Pipeline中冗余的中间内容，遵循优雅的奥卡姆剃刀原则，如无必要，勿增实体。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
