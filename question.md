# question.md — Pipeline 自循环问题清单 & 改进记录

目标：把本仓库的 `skills + pipelines + UNITS.csv + quality gates` 做成一个 **Codex 能端到端跑完、过程可见、结果不空洞** 的闭环（尤其补强 writer）。

本文档的写法：**只记录可复现事实 + 精确到环节/产物/脚本的改进点**；避免泛泛而谈。

---

## 0) 最新一次端到端结果（基线）

- Pipeline：`pipelines/arxiv-survey-latex.pipeline.md`（strict gates）
- Workspace：`workspaces/e2e-agent-survey-selfloop-20260113-034953`
- 运行方式：`--strict --auto-approve C2`（用于 smoke test，绕过人工签字）
- 结果：全链路 DONE（含 PDF）
  - Draft：`workspaces/e2e-agent-survey-selfloop-20260113-034953/output/DRAFT.md`
  - Global review：`workspaces/e2e-agent-survey-selfloop-20260113-034953/output/GLOBAL_REVIEW.md`（PASS）
  - Audit：`workspaces/e2e-agent-survey-selfloop-20260113-034953/output/AUDIT_REPORT.md`（PASS）
  - PDF：`workspaces/e2e-agent-survey-selfloop-20260113-034953/latex/main.pdf`（27 pages）
  - LaTeX build report：`workspaces/e2e-agent-survey-selfloop-20260113-034953/output/LATEX_BUILD_REPORT.md`

复现命令：

```bash
python scripts/pipeline.py kickoff \
  --topic "LLM agents survey (tool use, planning, memory, evaluation) with LaTeX PDF" \
  --pipeline arxiv-survey-latex \
  --workspace workspaces/e2e-agent-survey-selfloop-20260113-034953 \
  --run --strict --auto-approve C2
```

补充：最新 smoke test（用于验证新增 self-loop 工具链）

- Workspace：`workspaces/e2e-agent-survey-selfloop-20260113-writerloop`
- 结果：`C0–C4` 全部 DONE；`U100` 按预期 BLOCKED（缺少 `sections/*.md`，需要 LLM 写作）
- `writer-selfloop`：已可生成完整的 per-file TODO（避免 `QUALITY_GATE.md` 的 “... 截断”）

---

## 1) 当前“完整流程”是什么（一步步）

以 `arxiv-survey-latex` 为例，默认 checkpoints：`C0 → C1 → C2(HUMAN) → C3 → C4 → C5`。

### C0 Init（工件骨架）

- skills：`workspace-init`, `pipeline-router`
- 输出：`STATUS.md`, `UNITS.csv`, `CHECKPOINTS.md`, `DECISIONS.md`, `GOAL.md`, `queries.md`

### C1 Retrieval & core set（检索 → 去重/排序 → core set）

- skills：`literature-engineer` → `dedupe-rank`
- 输出：`papers/papers_raw.jsonl`, `papers/papers_dedup.jsonl`, `papers/core_set.csv`, `papers/retrieval_report.md`

### C2 Structure（NO PROSE + 单次签字点）

- skills：`taxonomy-builder` → `outline-builder` → `section-mapper` → `outline-refiner` → `pipeline-router(C2 review)`
- 输出：`outline/taxonomy.yml`, `outline/outline.yml`, `outline/mapping.tsv`, `outline/coverage_report.md`
- HUMAN：`DECISIONS.md` 勾选 `Approve C2`

### C3 Evidence pack（NO PROSE）

- skills：`pdf-text-extractor` → `paper-notes` → `subsection-briefs` → `chapter-briefs`
- 输出：`papers/paper_notes.jsonl`, `papers/evidence_bank.jsonl`, `outline/subsection_briefs.jsonl`, `outline/chapter_briefs.jsonl`

### C4 Citations + visuals（NO PROSE）

- skills：`citation-verifier` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `claim-matrix-rewriter` → `table-schema` → `table-filler` → `survey-visuals`
- 输出：`citations/ref.bib`, `citations/verified.jsonl`, `outline/evidence_bindings.jsonl`, `outline/evidence_drafts.jsonl`, `outline/anchor_sheet.jsonl`, `outline/tables.md`, `outline/timeline.md`, `outline/figures.md`

### C5 Writing + QA + LaTeX/PDF（PROSE after C2）

- skills：`subsection-writer` → `transition-weaver` → `section-merger` → `draft-polisher` → `global-reviewer` → `pipeline-auditor` → `latex-scaffold` → `latex-compile-qa`
- 输出：`sections/*.md` → `output/DRAFT.md` → `latex/main.pdf`

---

## 2) “每个 section 太空洞/分点太多”根因（以及当前怎么防退化）

### 根因（历史问题）

- **H3 过多 + 每节证据不足**：大纲碎片化会把证据摊薄，writer 更容易写成“每节 1–2 段泛泛而谈”。
- **writer 质量门槛太松**：没有硬阈值时，stub（短段落 + 泛化句）会一路流入 PDF。
- **缺少“可写锚点”**：即使 `evidence_drafts` 存在，writer 仍可能忽略数字/benchmark，导致“像论文但没信息量”。
- **引用绑定缺少显式约束**：writer 容易跨小节乱引用，破坏 claim→evidence 对齐。

### 当前已落地的防退化机制（可复现）

- `tooling/quality_gate.py`：
  - 限制 `outline`：survey profile 下 H3 总数 `<= 12`
  - 强制 writer 深度：H3 正文（去 citations）`>= ~5000 chars` 且 `>=6 段`
  - 若 evidence pack 含数字：强制至少 1 个 **带引用的数字锚点**
  - 要求每个含 H3 的 H2 有 `sections/S<sec_id>_lead.md`（不新增目录层级）
- 新增 NO-PROSE 中间产物，减少“自由发挥”：
  - `.codex/skills/chapter-briefs/` → `outline/chapter_briefs.jsonl`（H2 贯穿线 + lead 计划）
  - `.codex/skills/anchor-sheet/` → `outline/anchor_sheet.jsonl`（每个 H3 的数字/benchmark/limitation 锚点）

---

## 3) 本次 smoke test 暴露的“真实问题”（精确到环节/脚本）

### (C1) `literature-engineer` 在线扩充失效（已修复）

- 现象：严格模式在 `U010` 直接 BLOCKED，`papers_raw.jsonl` 只剩 pinned 的少量论文（<200）
- 根因：`r.jina.ai` 返回格式变更（JSON envelope + `data.content`），导致 Semantic Scholar fallback 解析失败 → 0 结果，但脚本不报错，只是静默退出
- 修复：`workspaces/e2e-agent-survey-selfloop-20260113-034953` 跑通后已验证 OK（`papers_raw.jsonl=800`）
- 需要继续改进：
  - `retrieval_report.md` 应明确记录 semantic scholar “结构化错误/空结果”原因（否则误以为在线 OK）
  - 对 arXiv API 的不稳定（RemoteDisconnected）要有更明确的降级路径与提示

涉及文件：
- `.codex/skills/literature-engineer/scripts/run.py`（已修复 r.jina.ai envelope 解析）

### (C5) writer 仍然是“必须人工/LLM”的环节（这是设计选择，但需要更好自举）

- 现象：`U100` 必然 BLOCKED（`sections_missing_files`）直到 `sections/*.md` 被写出
- 当前策略：让脚本只做确定性工作（生成 manifest + gate），语义写作由 LLM 按 `subsection-writer` skill 执行
- 需要继续改进：
  - 让 `sections/sections_manifest.jsonl` 明确包含每个 H3 的 `allowed_bibkeys`（从 `evidence_bindings.jsonl` 复制一份），减少“跨小节乱引用”反复失败
  - 增加一个“writer self-loop” skill：读 `output/QUALITY_GATE.md`，只扩写失败小节（避免全量重写）

---

## 4) Pipeline 结构是否“像论文”（减少章节碎片）

本次基线 run 的 Draft 结构：

- H2：`Introduction` / `Related Work` / `Foundations & Interfaces` / `Core Components` / `Learning...` / `Evaluation & Risks` / `Open Problems` / `Conclusion`
- H3：8 个（每个 H3 深度被 gates 强制）

这基本符合你提到的“6–8 个左右、3–4 个核心章 + discussion/open problems”的论文结构；同时避免把 tables/figures/timeline 等“意图产物”塞进目录，减少 TOC 噪声。

---

## 5) 下一轮要做的改进（建议按收益排序）

1) **writer 自循环 skill（已落地）**
   - Skill：`.codex/skills/writer-selfloop/`
   - 用法：读 `output/QUALITY_GATE.md`，只改失败的 `sections/*.md`，反复 rerun `subsection-writer` script 直到 PASS（避免全量重写）

2) **global-reviewer 的 evidence_mode 识别（已修复）**
   - 修复点：`.codex/skills/global-reviewer/scripts/run.py` 现在优先读 `queries.md`，避免因为 `papers/fulltext_index.jsonl` 在 abstract 模式下也存在而误报 fulltext

3) **把 “allowed citations” 下沉到 writer 入口**
   - 让 `sections_manifest.jsonl` 或单独 `outline/allowed_cites.jsonl` 给每个 sub_id 明确 bibkeys 列表

4) **模板/脚本简化（skills 优先）**
   - 原则：脚本只做 scaffold/validate/compile/report；语义工作写在 skill workflow 里
   - 把“脚本生成但需要 LLM 填充”的产物在 skill 里标记为 bootstrap，避免误把 scaffold 当 DONE

---

## 6) 你接下来希望我优先做什么？

可选路线：

1) 继续把 writer self-loop 做成“更自动”的收敛：让脚本能产出更强的 per-file TODO/context pack，并把 loop 结果写成可审计的日志（但不自动改 prose）。
2) 全量“Anthropic skills 风格”升级：统一 `Decision Tree / Inputs / Outputs / Workflow / Troubleshooting`，并跑 `python scripts/validate_repo.py --strict` + 生成技能依赖图更新 docs。
3) 把 C2 的 outline-builder 再做一次“论文风格”强化（默认 6–8 个 H2、<=12 H3、每个 H3 有明确比较轴与 expected-cites），进一步减少碎片化风险。
