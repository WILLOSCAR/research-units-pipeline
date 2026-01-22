# research-units-pipeline-skills

> **一句话**：让 Pipeline 会"带人 / 带模型"做研究——不是给一堆脚本，而是给一套**语义化的 skills**，每个 skill 知道"该做什么、怎么做、做到什么程度、不能做什么"。

---

## Todo
1. 加入多 cli 协作，multi-agent design （在合适的环节接入 API，替代或者分担 codex 执行过程中的压力）
2. 持续打磨写作技巧，提升写作上下限（已经尝试了增加 role playing 的 soft 约束）
3. 完善剩余的Pipeline，example 新增例子
4. 精简Pipeline中冗余的中间内容，遵循优雅的奥卡姆剃刀原则，如无必要，勿增实体。


## 核心设计：Skills-First + 拆解链路 + 证据先行

**传统问题**：研究流水线要么是黑盒脚本（不知道怎么改），要么是松散文档（执行时靠人肉判断）。

**本设计的解法**：

1. **Skills 语义化**：每个 skill 不是函数，而是**带引导的执行单元**——
   - `inputs / outputs`：明确依赖和产物
   - `acceptance`：验收标准（如"每小节映射 >=8 篇论文"）
   - `notes`：怎么做、边界条件、常见错误
   - `guardrail`：不能做什么（如 C2-C4 阶段 **NO PROSE**）

2. **拆解链路**：6 个 checkpoint（C0→C5），36 个原子 units，依赖关系显式写在 `UNITS.csv`
3. **证据先行**：C2-C4 强制先建证据底座（taxonomy → mapping → evidence packs），C5 才写作

**设计目标**：
- **可复用**：同一个 skill（如 `subsection-writer`）可被多个 pipeline 复用，换个 pipeline 不用重写逻辑
- **可引导**：新手/模型按 skill 的 `acceptance` + `notes` 执行，不需要"猜"该做到什么程度
- **可约束**：`guardrail` 防止执行者（尤其是模型）越界（如在 C3 阶段偷偷写正文）
- **可定位**：失败时报告指向具体 skill + 中间产物，修复后从失败点继续

---

**为什么这样设计？**

| 特性 | 传统做法 | 本设计 |
|------|----------|--------|
| **可见** | 黑盒脚本 | 每个 unit 产出中间文件（`papers/`、`outline/`、`citations/`、`sections/`） |
| **可审计** | 日志散落 | `UNITS.csv` 记录执行历史与验收标准，`DECISIONS.md` 记录人类检查点 |
| **可自循环** | 失败全部重跑 | 质量门 FAIL → 报告告诉你改哪个中间产物 → 修复后从失败 unit 继续 |
| **可复用** | 每个项目重写 | skills 模块化，跨 pipeline 复用（如 `taxonomy-builder`、`evidence-binder`） |
| **可引导** | 靠人肉判断 | 每个 skill 带 `acceptance` + `notes`，执行者知道"做到什么程度" |


English version: [`README.en.md`](README.en.md).


## codex 参考配置

```toml

[sandbox_workspace_write]
network_access = true

[features]
unified_exec = true
shell_snapshot = true
steer = true
```


## 一句话启用（推荐：对话里跑 Pipeline）
启动 codex
> codex --sandbox workspace-write --ask-for-approval never 

把下面这句话丢给 Codex（或 Claude Code）即可：

> 给我写一个 agent 的 latex-survey

这句话会触发 repo 内的 skills 自动路由并执行 pipeline（按 `UNITS.csv` 合同落盘中间产物）。

（可选：指定 pipeline 文件：`pipelines/arxiv-survey-latex.pipeline.md`（或 `research-units-pipeline-skills/pipelines/arxiv-survey-latex.pipeline.md`）；不想自动同意 C2：把“C2 自动同意”删掉即可。C2 是一个 human in the loop 的介入点）

你也可以更明确一点（避免 router 选错）：

> 用 `pipelines/arxiv-survey-latex.pipeline.md` 给我写一个 agent 的 latex-survey（启用 strict 质量门；C2 自动同意）

## 你会得到什么（分层产物 + 自循环入口）

**执行层**：
- `UNITS.csv`：39+（还在增加） 个原子 unit 的执行合约（依赖 → 输入 → 输出 → 验收标准）
- `DECISIONS.md`：人类检查点（**C2 必须审批大纲**后才进入写作）

**中间产物层**（按 checkpoint 分层）：
```
C1: papers/papers_raw.jsonl → papers/papers_dedup.jsonl → papers/core_set.csv (+ papers/retrieval_report.md)                  # 检索 + 去重/精选
C2: outline/taxonomy.yml → outline/outline.yml → outline/mapping.tsv (+ outline/coverage_report.md; outline/outline_state.jsonl) # 结构（NO PROSE）
C3: papers/fulltext_index.jsonl → papers/paper_notes.jsonl + papers/evidence_bank.jsonl → outline/subsection_briefs.jsonl (+ outline/chapter_briefs.jsonl) # 证据底座（NO PROSE）
C4: citations/ref.bib + citations/verified.jsonl → outline/evidence_bindings.jsonl → outline/evidence_drafts.jsonl → outline/anchor_sheet.jsonl → outline/writer_context_packs.jsonl (+ outline/claim_evidence_matrix.md) # 引用 + 证据包（NO PROSE）
C5: sections/*.md → output/DRAFT.md → latex/main.tex → latex/main.pdf                                                       # 写作 + 编译
```

**质量门 + 自循环入口**：
- `--strict` 模式才会持续写入质量门结论：unit 被 BLOCKED 时看 `output/QUALITY_GATE.md`（最新条目）定位需要修的中间产物；脚本/缺产物等运行问题看 `output/RUN_ERRORS.md`
- 非 `--strict` 跑法：不会做 unit-level 质量门拦截（`output/QUALITY_GATE.md` 可能只有模板/历史记录）；以 `output/AUDIT_REPORT.md`（全局审计）+ `output/RUN_ERRORS.md` 为主
- 写作层自循环（只修复失败小节）：
  - `output/WRITER_SELFLOOP_TODO.md`（写作门：PASS/FAIL + 需要修复的 sections 列表）
  - `output/SECTION_LOGIC_REPORT.md`（thesis + 连接词密度）
  - `output/CITATION_BUDGET_REPORT.md`（引用增密建议）

## 简单的对话式执行（从 0 到 PDF）

```
你：给我写一个 agent 的 latex-survey

↓ [C0-C1] 检索 800+ 篇论文 → 去重到 150+ 核心集 arxiv 会补全 meta 信息
↓ [C2] 构建 taxonomy + outline + mapping（NO PROSE）→ 停在 C2 等审批

你：C2 check 关键文件，看没有问题回复同意，继续

↓ [C3-C4] 构建证据底座（paper notes + evidence packs + citations）（NO PROSE）
↓ [C5] 基于 evidence 开始写作 → 质量门检查

【如果 PASS】→ output/DRAFT.md + latex/main.pdf ✓
【如果 FAIL】→ output/QUALITY_GATE.md 告诉你改哪个中间产物

你（如果 FAIL）：按报告修复对应文件（如 outline/evidence_drafts.jsonl），然后说"继续"
→ 从失败 unit 恢复执行，不需要全部重跑
```

**关键原则**：C2-C4 强制 NO PROSE，先建证据底座；C5 才写作，失败时可定点修复中间产物。

## 示例产物（v0.1，包含完整中间产物）
该版本由 codex 中的 gpt-5.2-xhigh 运行约 2 小时 生成，过程中仅进行过 一次 human-in-the-loop（C2 阶段） 介入。
路径：`example/e2e-agent-survey-latex-verify-****时间戳/`（pipeline：`pipelines/arxiv-survey-latex.pipeline.md`）。
配置摘要（示例 run）：`draft_profile: lite` / `evidence_mode: abstract` / `core_size: 220`（详见 `queries.md`）。
推荐默认（对齐最终交付）：`draft_profile: survey`（默认）或 `draft_profile: deep`（更严格）。

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
  classDef file fill:#ffffff,stroke:#d0d7de,color:#24292f;
  classDef report fill:#e7f3ff,stroke:#0969da,color:#24292f;
  classDef gate fill:#fff8c5,stroke:#bf8700,color:#24292f;
  classDef step fill:#ffffff,stroke:#6e7781,stroke-dasharray: 4 2,color:#24292f;

  subgraph C0["C0 / workspace root"]
    GOAL["GOAL.md"]:::file
    STATUS["STATUS.md"]:::file
    UNITS["UNITS.csv"]:::file
    DEC["DECISIONS.md"]:::file
    LOCK["PIPELINE.lock.md"]:::file
    QUERIES["queries.md"]:::file
  end

  subgraph PAPERS["papers/"]
    RAW["papers/papers_raw.jsonl"]:::file
    RETREP["papers/retrieval_report.md"]:::report
    DEDUP["papers/papers_dedup.jsonl"]:::file
    CORE["papers/core_set.csv"]:::file
    FULLIDX["papers/fulltext_index.jsonl"]:::file
    NOTES["papers/paper_notes.jsonl"]:::file
    BANK["papers/evidence_bank.jsonl"]:::file
  end

  subgraph OUTLINE["outline/"]
    TAX["outline/taxonomy.yml"]:::file
    OL["outline/outline.yml"]:::file
    MAP["outline/mapping.tsv"]:::file
    COV["outline/coverage_report.md"]:::report
    OSTATE["outline/outline_state.jsonl"]:::file
    SUBBR["outline/subsection_briefs.jsonl"]:::file
    CHBR["outline/chapter_briefs.jsonl"]:::file
    TRANS["outline/transitions.md"]:::file
    BIND["outline/evidence_bindings.jsonl"]:::file
    BINDREP["outline/evidence_binding_report.md"]:::report
    EDRAFT["outline/evidence_drafts.jsonl"]:::file
    ANCH["outline/anchor_sheet.jsonl"]:::file
    WCP["outline/writer_context_packs.jsonl"]:::file
    CEM["outline/claim_evidence_matrix.md"]:::file
  end

  subgraph CITE["citations/"]
    BIB["citations/ref.bib"]:::file
    VER["citations/verified.jsonl"]:::file
  end

  subgraph SECT["sections/"]
    MAN["sections/sections_manifest.jsonl"]:::file
    SFILES["sections/S*.md (H3 bodies + leads)"]:::file
    ABSTRACT["sections/abstract.md"]:::file
    DISC["sections/discussion.md"]:::file
    CONC["sections/conclusion.md"]:::file
  end

  subgraph OUT["output/"]
    DRAFT["output/DRAFT.md"]:::file
    FRONTREP["output/FRONT_MATTER_REPORT.md"]:::report
    MERGEREP["output/MERGE_REPORT.md"]:::report
    WTODO["output/WRITER_SELFLOOP_TODO.md"]:::report
    SLOG["output/SECTION_LOGIC_REPORT.md"]:::report
    CITEBUD["output/CITATION_BUDGET_REPORT.md"]:::report
    CITEINJ["output/CITATION_INJECTION_REPORT.md"]:::report
    POSTVOICE["output/POST_MERGE_VOICE_REPORT.md"]:::report
    GLOBALREV["output/GLOBAL_REVIEW.md"]:::report
    AUDIT["output/AUDIT_REPORT.md"]:::report
    SCHEMA["output/SCHEMA_NORMALIZATION_REPORT.md"]:::report
    ESELF["output/EVIDENCE_SELFLOOP_TODO.md"]:::report
    GATE["output/QUALITY_GATE.md (strict sink)"]:::gate
    ERR["output/RUN_ERRORS.md"]:::report
    LATEXREP["output/LATEX_BUILD_REPORT.md"]:::report
  end

  subgraph LATEX["latex/"]
    TEX["latex/main.tex"]:::file
    PDF["latex/main.pdf"]:::file
  end

  FM["front-matter-writer"]:::step
  SW["subsection-writer"]:::step
  MG["section-merger"]:::step

  %% C1: retrieval -> core set
  QUERIES --> RAW --> DEDUP --> CORE
  RAW --> RETREP

  %% C2: structure
  CORE --> TAX --> OL --> MAP --> COV
  MAP --> OSTATE

  %% C3: notes + evidence bank (uses mapping to prioritize)
  CORE --> FULLIDX --> NOTES
  MAP --> NOTES
  NOTES --> BANK
  OL --> SUBBR
  MAP --> SUBBR
  NOTES --> SUBBR
  OL --> CHBR
  SUBBR --> CHBR

  %% C4: citations + bindings + packs + context packs
  NOTES --> BIB --> VER
  BANK --> BIND
  SUBBR --> BIND
  MAP --> BIND
  BIB --> BIND
  BIND --> BINDREP

  SUBBR --> EDRAFT
  NOTES --> EDRAFT
  BANK --> EDRAFT
  BIND --> EDRAFT
  BIB --> EDRAFT

  EDRAFT --> ANCH
  BIB --> ANCH

  OL --> WCP
  SUBBR --> WCP
  CHBR --> WCP
  BIND --> WCP
  EDRAFT --> WCP
  ANCH --> WCP
  BIB --> WCP

  SUBBR --> CEM
  EDRAFT --> CEM
  BIB --> CEM

  SUBBR --> ESELF
  BIND --> ESELF
  EDRAFT --> ESELF
  ANCH --> ESELF

  OL --> SCHEMA
  BIB --> SCHEMA
  SUBBR --> SCHEMA
  CHBR --> SCHEMA
  BIND --> SCHEMA
  EDRAFT --> SCHEMA
  ANCH --> SCHEMA

  %% C5: writing -> merge -> audit -> LaTeX
  OL --> TRANS
  SUBBR --> TRANS

  %% front-matter (C5)
  DEC --> FM
  OL --> FM
  MAP --> FM
  RETREP --> FM
  CORE --> FM
  QUERIES --> FM
  BIB --> FM
  FM --> ABSTRACT
  FM --> DISC
  FM --> CONC
  FM --> FRONTREP

  %% per-H3 writing units (C5)
  OL --> SW
  CHBR --> SW
  SUBBR --> SW
  ANCH --> SW
  WCP --> SW
  EDRAFT --> SW
  BIND --> SW
  BIB --> SW
  DEC --> SW
  SW --> MAN --> SFILES

  %% merge (C5)
  GOAL --> MG
  OL --> MG
  TRANS --> MG
  MAN --> MG
  MG --> DRAFT
  MG --> MERGEREP

  %% writing self-loops / reports
  MAN --> WTODO
  SUBBR --> WTODO
  CHBR --> WTODO
  WCP --> WTODO
  BIND --> WTODO
  BIB --> WTODO
  QUERIES --> WTODO

  MAN --> SLOG
  SUBBR --> SLOG
  WCP --> SLOG
  QUERIES --> SLOG

  %% post-merge voice + citation loop + global review + audit
  DRAFT --> POSTVOICE
  TRANS --> POSTVOICE

  DRAFT --> CITEBUD
  OL --> CITEBUD
  WCP --> CITEBUD
  BIB --> CITEBUD

  DRAFT -.-> CITEINJ
  CITEBUD --> CITEINJ
  OL --> CITEINJ
  BIB --> CITEINJ
  CITEINJ -.-> DRAFT

  DRAFT --> GLOBALREV
  DRAFT --> AUDIT
  OL --> AUDIT
  BIND --> AUDIT
  BIB --> AUDIT

  %% LaTeX scaffold + compile
  DRAFT --> TEX --> PDF
  BIB --> TEX
  TEX --> LATEXREP
  PDF --> LATEXREP
```

最终交付只关注最新版本，测试完成后如有改进直接纳入示例路径中，默认以最新时间戳标记的文件夹即表示最新版本，视情况保留 2-3 个版本：

- Markdown 草稿：
example/e2e-agent-survey-latex-verify-<最新时间戳>/output/DRAFT.md

- PDF 输出：
example/e2e-agent-survey-latex-verify-<最新时间戳>/latex/main.pdf

- QA 审计报告：
example/e2e-agent-survey-latex-verify-<最新时间戳>/output/AUDIT_REPORT.md


## 欢迎提出各类 issue，一起改进写作流程

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
