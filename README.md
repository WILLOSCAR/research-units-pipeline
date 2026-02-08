# research-units-pipeline-skills

> **一句话**：让 Pipeline 会"带人 / 带模型"做研究——不是给一堆脚本，而是给一套**语义化的 skills**，每个 skill 知道"该做什么、怎么做、做到什么程度、不能做什么"。

---

## WIP
1. 在 Appendix 增加了表格
2. 持续打磨写作技巧，提升写作上下限（已经尝试了增加 role playing 的 soft 约束）
3. 去除模板话描述
## Todo
1. 加入多 cli 协作，multi-agent design （在合适的环节接入 API，替代或者分担 codex 执行过程中的压力）
2. 完善剩余的Pipeline，example 新增例子
3. 精简Pipeline中冗余的中间内容，遵循优雅的奥卡姆剃刀原则，如无必要，勿增实体。


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


English version: [`README.en.md`](README.en.md).


## codex 参考配置
配置可能会根据 codex 的更新有变化
```toml

[sandbox_workspace_write]
network_access = true

[features]
shell_snapshot = true
```


## 一句话启用（推荐：对话式跑一篇 survey）

1) 在本仓库目录启动 Codex：

```bash
codex --sandbox workspace-write --ask-for-approval never
```

2) 在对话里直接说目标（例子）：

> 给我写一篇关于 LLM agents 的 LaTeX survey

它会自动创建 `workspaces/<时间戳>/`，并按 C0→C5 逐步产出文件。默认会在 **C2（大纲确认）** 停下来；你确认后才会开始写正文并编译 PDF。

可选（用一句话说清即可）：
- 指定流程文件：`pipelines/arxiv-survey-latex.pipeline.md`（需要 PDF 就选它）
- 不想停在 C2：加 `C2 自动同意`（熟练后再用）

术语速查：
- workspace：一次运行的输出目录（`workspaces/<name>/`）
- C2：大纲确认点；不确认就不会写正文
- strict：开启质量门；失败会停并在 `output/` 写报告

## 你会得到什么（分层产物 + 自循环入口）

一次完整 run 的输出都在一个 workspace 里（`workspaces/<name>/`）。你主要会用到两类东西：
- **运行清单**：看进度 / 看卡点 / 从失败点继续跑
- **分阶段产物**：papers/outline/citations/sections/output/latex

默认参数（A150++，对齐 survey 交付）：
- 检索上限：`max_results=1800`（每个 query bucket）
- 核心论文：`core_size=300`（对应 `papers/core_set.csv` / `citations/ref.bib`）
- 每个小节论文池：`per_subsection=28`（对应 `outline/mapping.tsv`）
- 全局 unique citations：hard `>=150`，recommended `>=165`（默认会补齐到 recommended）

运行清单（最常看）：
- `UNITS.csv`：约 43–45 个 unit（不同 pipeline 略有差异；LaTeX/PDF 版会多几个）；卡住就看哪个 unit 是 `BLOCKED`
- `DECISIONS.md`：人类确认点（最重要的是 **C2：确认大纲后才写正文**）
- `STATUS.md`：运行日志（当前跑到哪一步）

分阶段产物（你真正关心的内容）：
```
C1（找论文）:
  papers/papers_raw.jsonl → papers/papers_dedup.jsonl → papers/core_set.csv
  + papers/retrieval_report.md   # 这次检索/筛选的说明

C2（搭骨架；不写正文）:
  outline/outline.yml + outline/mapping.tsv
  (+ outline/taxonomy.yml / outline/coverage_report.md)  # 可选：更结构化/更可审计

C3（做“可写”的证据底座；不写正文）:
  papers/paper_notes.jsonl + papers/evidence_bank.jsonl → outline/subsection_briefs.jsonl
  + papers/fulltext_index.jsonl  # 永远存在；abstract 模式只记录 skip，fulltext 模式才会下载/抽取

C4（把每小节写作包准备好；不写正文）:
  citations/ref.bib + citations/verified.jsonl
  + outline/evidence_bindings.jsonl / outline/evidence_drafts.jsonl / outline/anchor_sheet.jsonl
  → outline/writer_context_packs.jsonl
  + outline/tables_appendix.md  # 面向读者的 Appendix 表格（索引表只作为中间产物保留）

C5（写作与输出）:
  sections/*.md → output/DRAFT.md
  (+ latex/main.pdf)  # 只有 LaTeX pipeline 才会有
```

失败怎么定位（按优先级，按报告定点修）：
- 跑不动/脚本报错：`output/RUN_ERRORS.md`
- strict 模式被拦住：`output/QUALITY_GATE.md`（最后一条就是当前原因 + 下一步）
- 写作门（只修列出的文件）：`output/WRITER_SELFLOOP_TODO.md`
- 段落跳步/孤岛：`output/SECTION_LOGIC_REPORT.md`
- 论证链路 + 口径一致性：`output/ARGUMENT_SELFLOOP_TODO.md`（口径单一真源在 `output/ARGUMENT_SKELETON.md# Consistency Contract`）
- 去冗余/融合收敛：`output/PARAGRAPH_CURATION_REPORT.md`（选段→评价→多候选→择优融合）
- 引用增密：`output/CITATION_BUDGET_REPORT.md`
- 全局体检：`output/AUDIT_REPORT.md`（最终审计）

## 简单的对话式执行（从 0 到 PDF）

```
你：写一篇关于 LLM agents 的 LaTeX survey

↓ [C0-C1] 找论文：检索候选（`max_results=1800`/桶；去重后目标 >=1200）→ core set（默认 300 篇：`papers/core_set.csv`）
↓ [C2] 生成“大纲 + 每小节论文池”（不写正文）：`outline/outline.yml` + `outline/mapping.tsv`（默认每个小节映射 28 篇）
   → 默认停在 C2 等你确认（如果你明确说 `C2 自动同意` 才会继续）

你：看过没问题，回复「同意继续」

↓ [C3-C4] 把论文整理成“可写材料”（不写正文）：
   - `papers/paper_notes.jsonl`：每篇论文的要点/结果/局限
   - `citations/ref.bib`：参考文献表（可引用的 key 集合）
   - `outline/writer_context_packs.jsonl`：每个小节的写作包（允许引用哪些论文 + 该写哪些对比点）
↓ [C5] 写作与输出：
   - 先写分小节文件：`sections/*.md`
   - 再做“自检 + 收敛”：写作门 / 段落逻辑门 / 论证门 / 选段融合（都在 C5 反复迭代）
   - 再合并成草稿：`output/DRAFT.md`
   - LaTeX pipeline 会额外生成：`latex/main.pdf`
   - 目标：全局 unique citations 推荐 `>=165`（不足会触发“引用预算/注入”步骤补齐）

【如果卡住】按报告定点修：
- 开了 strict：看 `output/QUALITY_GATE.md`（最后一条就是当前原因 + 下一步）
- 最终总审计：看 `output/AUDIT_REPORT.md`

你：按报告修复对应文件后说「继续」
→ 从卡住的那一步继续跑，不需要全部重跑
```

**关键原则**：C2-C4 强制 NO PROSE，先建证据底座；C5 才写作，失败时可定点修复中间产物。

## 示例产物（v0.1，包含完整中间产物）
这是一个“完整跑通”的示例 workspace：从找论文 → 出大纲 → 整理证据 → 写草稿 → 编译 PDF，所有中间产物都在里面，方便你对照理解整条链路。

- 示例路径：`example/e2e-agent-survey-latex-verify-<时间戳>/`（对应流程：`pipelines/arxiv-survey-latex.pipeline.md`）
- 过程中会在 **C2（大纲）** 停下来等你确认；确认后才会写正文
- 默认配置（A150++）：核心论文 300 篇、每个小节映射 28 篇、证据模式用 abstract（摘要级）；目标是全局引用足够密（全局 unique citations 默认收敛到推荐值）
- 一般建议：`draft_profile: survey`（默认交付）；想更严格再用 `draft_profile: deep`

目录速览（每个文件夹干嘛用）：

```text
example/e2e-agent-survey-latex-verify-<最新时间戳>/
  STATUS.md            # 进度与执行日志（当前 checkpoint）
  UNITS.csv            # 执行合约：一行一个 unit（依赖/验收/产物）
  DECISIONS.md         # 人类检查点（Approve C*）
  CHECKPOINTS.md       # checkpoint 规则
  PIPELINE.lock.md     # 选中的 pipeline（单一真相源）
  GOAL.md              # 目标/范围 seed
  queries.md            # 检索与写作档位配置（draft_profile/evidence_mode/core_size...）
  papers/              # C1/C3：检索结果与论文“底座”
  outline/             # C2/C3/C4：taxonomy/outline/mapping + briefs + evidence packs + tables/figures 规格
  citations/           # C4：BibTeX 与 verification 记录
  sections/            # C5：按 H2/H3 拆分的可 QA 小文件（含 chapter lead）
  output/              # C5：合并后的 DRAFT + 报告（audit/merge/citation budget...）
  latex/               # C5：LaTeX scaffold + 编译产物（main.pdf）
```

文件夹之间的“流水线关系”：

```mermaid
flowchart LR
  C0["C0 Workspace<br/>STATUS/UNITS/DECISIONS/queries"] --> C1["C1 papers/<br/>papers_raw → papers_dedup → core_set<br/>(+ retrieval_report)"]
  C1 --> C2["C2 outline/ (NO PROSE)<br/>taxonomy → outline → mapping<br/>(+ coverage_report)"]
  C2 --> C3["C3 evidence substrate (NO PROSE)<br/>paper_notes + evidence_bank<br/>subsection_briefs / chapter_briefs"]
  C3 --> C4["C4 evidence packs + citations (NO PROSE)<br/>ref.bib + verified<br/>evidence_bindings / evidence_drafts<br/>anchor_sheet / writer_context_packs"]
  C4 --> C5["C5 sections/<br/>front matter + per-H3 writing units<br/>(+ transitions)"]
  C5 --> OUT["output/<br/>DRAFT + QA reports"]
  OUT --> TEX["latex/<br/>main.tex → main.pdf"]
```

交付时只关注**最新时间戳**的示例目录（默认保留 2–3 个历史目录用于回归对比）：

- Markdown 草稿：`example/e2e-agent-survey-latex-verify-<最新时间戳>/output/DRAFT.md`
- PDF 输出：`example/e2e-agent-survey-latex-verify-<最新时间戳>/latex/main.pdf`
- QA 审计报告：`example/e2e-agent-survey-latex-verify-<最新时间戳>/output/AUDIT_REPORT.md`


## 欢迎提出各类 issue，一起改进写作流程

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
