# Pipeline Diagnosis & Improvement (skills-first)

Last updated: 2026-01-16

目标：把本仓库的 `skills + pipelines + units + quality gates` 做成一个 **Codex 能端到端跑完、过程可见、结果不空洞** 的闭环；并把写作质量尽量拉近 `ref/agent-surveys/` 的"论文感"。

本文档定位：**诊断与改进清单（偏契约/流程/skill 修改点）**，而不是写作长文；尽量用可观测指标与中间产物来定位问题。

---

## 0) 当前状态（事实指标）

已验证的"跑通且不空洞"样例（strict + auto-approve C2 的 smoke test）：

- Workspace：`workspaces/e2e-agent-survey-citeboost-20260114-015029`
  - Draft：`workspaces/e2e-agent-survey-citeboost-20260114-015029/output/DRAFT.md`
  - PDF：`workspaces/e2e-agent-survey-citeboost-20260114-015029/latex/main.pdf`（43 pages）
  - Audit：`workspaces/e2e-agent-survey-citeboost-20260114-015029/output/AUDIT_REPORT.md`（PASS；unique citations in draft=105；bib entries=220）
  - Global review：`workspaces/e2e-agent-survey-citeboost-20260114-015029/output/GLOBAL_REVIEW.md`（PASS；H3 median length ≈ 10705 chars sans cites）

历史对比与复现命令见：`question.md`（如果本文件缺失，说明工作区发生了误删，需要先 restore）。

---

## 1) 参考基准（ref/agent-surveys）"长什么样"

我们不试图复刻具体论文内容，而是对齐一些 **可观测的写作外形指标**：

- 顶层结构：6–8 个一级章节（H2），少而厚；Intro/Related Work + 3–4 个核心章节 + Discussion + Conclusion 是常见形态。
- Front matter（Introduction / Related Work）引用密度往往更高（比单个 H3 小节更像"综述入口"）。
- 段落张力：更接近 "问题/张力 → 方法/框架 → 直接对比 → 评测锚点 → 局限/边界" 的递进，而非平铺罗列。

证据：`ref/agent-surveys/STYLE_REPORT.md`（统计到的一级章节数量：min/median/max = 3/6/10；建议目标：6–8）。

---

## 2) 现行 Pipeline 是什么（一步步）

Pipeline 定义：`pipelines/arxiv-survey-latex.pipeline.md`（Stage C0–C5）

下面是"执行合约"视角的一步步（每步都要求有可检查的产物；写作只在 C2 之后）：

### C0 — Init

- 目标：创建 workspace 骨架 + 确认 pipeline 路由。
- 关键产物：`STATUS.md`, `UNITS.csv`, `CHECKPOINTS.md`, `DECISIONS.md`, `GOAL.md`, `queries.md`
- 关键 skills：`workspace-init`, `pipeline-router`

### C1 — Retrieval & core set

- 目标：拉一个足够大的候选集合（≥200 更稳），再去重与核心集收敛。
- 关键产物：`papers/papers_raw.jsonl`, `papers/papers_dedup.jsonl`, `papers/core_set.csv`, `papers/retrieval_report.md`
- 关键 skills：`literature-engineer`, `dedupe-rank`（可选：`keyword-expansion`, `survey-seed-harvest`）
- 常见失败：
  - 论文太少（后面 C2/C4 会被迫"薄写"）：优先扩 queries 与多路召回（不要在 writer 阶段硬写空话）。

### C2 — Structure（NO PROSE + HUMAN）

- 目标：生成"像论文"的章节骨架，**控制章节数量与粒度**，并把每个 H3 写成可验证的需求（不是模板 bullet）。
- 关键产物：`outline/taxonomy.yml`, `outline/outline.yml`, `outline/mapping.tsv`, `outline/coverage_report.md`
- 关键 skills：`taxonomy-builder`, `outline-builder`, `section-mapper`, `outline-refiner`
- Human checkpoint：`Approve C2`（scope + outline，写入 `DECISIONS.md`）
- 常见失败：
  - H3 太多、每节太薄：这是最常见的"最终 PDF 空洞"的根因之一，应在 C2 就合并/收敛。

### C3 — Evidence pack（NO PROSE）

- 目标：把每个 H3 变成"能写出来"的写作卡：明确 RQ、对比轴、段落计划、需要哪些证据类型。
- 关键产物：`papers/paper_notes.jsonl`, `papers/evidence_bank.jsonl`, `outline/subsection_briefs.jsonl`, `outline/chapter_briefs.jsonl`
- 关键 skills：`pdf-text-extractor`, `paper-notes`, `subsection-briefs`, `chapter-briefs`
- 常见失败：
  - `subsection_briefs` 里 paragraph_plan/axes 太空：C5 再强也会"空跑"。

### C4 — Citations + visuals（NO PROSE）

- 目标：把"可用引用范围 + 可用证据片段 + 数字锚点 + 图表 schema" 变成 writer 能直接消费的"确定性包"。
- 关键产物：
  - 引用：`citations/ref.bib`, `citations/verified.jsonl`
  - 绑定：`outline/evidence_bindings.jsonl`, `outline/evidence_binding_report.md`
  - 证据包：`outline/evidence_drafts.jsonl`, `outline/anchor_sheet.jsonl`, `outline/writer_context_packs.jsonl`
  - 结构 QA：`outline/claim_evidence_matrix.md`
  - 表格/图：`outline/table_schema.md`, `outline/tables.md`, `outline/timeline.md`, `outline/figures.md`
- 关键 skills：
  - `citation-verifier`, `evidence-binder`, `evidence-draft`, `anchor-sheet`, `writer-context-pack`,
  - `claim-matrix-rewriter`, `table-schema`, `table-filler`, `survey-visuals`
- 常见失败：
  - anchor facts / comparisons 产出了但 writer 不消费：C5 会变成"无数字、无对比"的泛写。

### C5 — Draft + PDF（PROSE after C2）

- 目标：按 H3 逐节写厚，合并成 paper-like draft，并通过审计/编译。
- 关键产物：`sections/*.md`, `output/DRAFT.md`, `output/GLOBAL_REVIEW.md`, `output/AUDIT_REPORT.md`, `latex/main.pdf`
- 关键 skills：`subsection-writer`, `transition-weaver`, `section-merger`, `draft-polisher`, `global-reviewer`, `pipeline-auditor`, `latex-*`
- 推荐工作方式：把 C5 当成"可控自循环"（只改失败节），而不是一次性大稿：
  - `subsection-writer` 写每个 H3 → quality gate 卡住就用 `writer-selfloop` 生成 per-file TODO → 只改失败文件 → 继续。

---

## 3) 质量差距主要来自哪里（按环节定位）

这部分只列 **最影响"空洞感/论文感"的根因**，并指向应该改哪个 skill（避免靠脚本"兜底"）。

### A) C2：章节预算（Section Budget）缺失 → H3 爆炸/变薄

现象：
- 生成的大纲容易"多小节"，每节只能写一点点，导致最终读起来像"目录展开"。

改进应落在：
- `taxonomy-builder`：把 taxonomy 设计成能自然收敛到 3–4 个核心章节（不要把所有细粒度能力都变成单独章节）。
- `outline-builder`：引入明确的 **章节预算契约**（默认目标：6–8 个 H2；核心章节 3–4；H3 总数建议 ≤8–12）。
- `outline-refiner`：把"过多/过薄"的风险写成可执行建议（合并哪些 H3、哪些轴可以在同一节比较）。

### B) C3：brief 里缺"论证段落计划" → writer 只能模板填充

现象：
- `subsection_briefs.jsonl` 如果只有主题/列点，没有对比轴与段落骨架，writer 会自然退化成"逐条描述"。

改进应落在：
- `subsection-briefs`：每个 H3 的 paragraph_plan 要显式包含：
  - 至少 2 个 A-vs-B 对比段（同段多引用）
  - 至少 1 个 evaluation anchor 段（benchmark/setting/metric）
  - 至少 1 个 limitation/edge-case 段（不要只是"未来工作"）
  - 至少 1 个 cross-paper synthesis 段（总结共性/差异，而非列举）
- `chapter-briefs`：给每个核心 H2 写 chapter lead 计划（连接各 H3 的比较轴），避免"章节孤岛"。

### C) C4：证据包/锚点产出没变成"必须消费的写作合同"

现象：
- `evidence_drafts` 和 `anchor_sheet` 即使很丰富，writer 仍可能选择性忽略，写成"无数字/无对比"的泛段落。

改进应落在：
- `writer-context-pack`：把"必须用"的清单提升为 pack 内的显式字段（例如 `must_use_anchor_facts_min`、`must_use_comparisons_min`），并在 skill 指南里要求 writer 对齐这些最小值。
- `anchor-sheet`：输出要面向"可落地到段落的锚点"（短句 + 数字 + 引用），并规定每节至少消费 N 个锚点。
- `evidence-binder`：默认允许"同一 H2 内有限复用"，降低过度严格导致的 brittle（但仍禁止跨 H2 漫游引用）。

已落地的 skill 合同补强（本次迭代）：
- `.codex/skills/anchor-sheet/SKILL.md`：新增 anchor 消费最小规则（eval/limitation/numeric 必须出现）。
- `.codex/skills/writer-context-pack/SKILL.md`：新增 writer contract（把 pack 当 checklist；anchors/comparisons must-use；引用优先 selected）。
- `.codex/skills/evidence-binder/SKILL.md`：补齐 bindings 输出格式 + "同 H2 内有限复用"策略说明（减少 brittle 且防 free-cite drift）。

### D) C5：段落微结构不稳定 → 像"总结"不像"论证"

现象（对比 ref）：
- 句末堆 citations（像标签）
- 没有直接对比句（A 一段 B 一段）
- 没有 evaluation anchor（读者不知道怎么比）
- limitation 写成泛泛"未来工作"

改进应落在：
- `subsection-writer`：把"论文段落形态"写成硬性检查清单（由 writer 自检，而不是只靠脚本事后抓）：
  - 每节 8–12 段（或按 `draft_profile`），且至少 1 段是 cross-paper synthesis（同段 ≥2 citations）
  - 每节至少 2 个"contrast sentence"（显式出现对比连接词：in contrast / unlike / compared to / whereas）
  - 每节至少 1 段写 evaluation anchor（benchmark + metric + setting，保守陈述）
  - 每节至少 1 段写 limitation（具体限制条件/失败模式/不适用场景）
  - 引用策略：尽量在"提出结论/对比/数字"句子处就近引用，而非段末堆砌

已落地的 skill 合同补强（本次迭代）：
- `.codex/skills/subsection-writer/SKILL.md`：新增 "Citation embedding + Transitions" 规则 + `grad-paragraph` 作为默认段落积木（提升"张力/对比/评测锚点/限制"的显式度）。
- `.codex/skills/transition-weaver/SKILL.md`：新增 paper-like connector 指南（Building on this / However / In contrast / As a result），减少"段落孤岛"。

---

## 4) 改进优先级（按 skills 落地）

> 原则：能靠 SKILL.md 的"合同/检查清单/产物规范"解决的，不新增脚本；脚本只做 deterministic merge/audit/compile。

P0（直接影响"空洞感/章节数量"）：
- `outline-builder`：章节预算契约（6–8 H2；核心章节 3–4；H3 总数 ≤8–12）
- `subsection-briefs`：强制段落计划包含对比/评测锚点/局限/综合段
- `subsection-writer`：段落微结构 + 引用嵌入策略（写作自检清单）

P1（提升可控性与可 debug）：
- `writer-context-pack`：把 must-use 清单显式化（并写进 writer 的 DoD）
- `anchor-sheet`：锚点输出更"可直接粘贴到段落"的形态 + 最小消费规则
- `evidence-binder`：同 H2 内有限复用策略（减少 brittle）

P2（可选增强）：
- `transition-weaver`：更像论文的 chapter lead / transitions（不引入新事实）
- `survey-visuals`：让 tables/timeline/figures 变成 writer 的"结构提示"，而不是 PDF 里孤立附件

---

## 5) 推荐的 writer 自循环（不靠"兜底链路"）

最小闭环（strict）：

1. 跑到 C5：`scripts/pipeline.py run --strict --auto-approve C2`
2. 如果卡在质量门：
   - 用 `writer-selfloop` 生成 per-file TODO（只列失败节的"缺什么"）
   - 只改失败的 `sections/*.md`（按 `writer_context_packs.jsonl` 的 contract 写）
   - 反复直到 PASS，然后继续 merge/audit/latex

关键心法：
- C5 的写作质量不要靠"补一句免责声明"混过 gate；而是回到 C2/C3/C4 把 brief/evidence/anchors 补厚（否则全局会越来越像模板）。

---

## 6) 仍待回答的问题（写入 question.md 追踪）

- C2：是否要把"章节预算"变成 `outline-refiner` 的硬 gate（默认 warn 还是 fail）？
- C4：同一 H2 内的 citation reuse 的上限/策略应该如何表述，既不 brittle 又不放飞？
- C5：是否要把"contrast sentence / eval anchor / limitation"变成 `subsection-writer` 的显式产物字段（例如每段标注它属于哪类），以便自检更稳？
- Ref 对齐：是否要把 `ref/agent-surveys/STYLE_REPORT.md` 的统计结果作为 C2 的 sanity check（只告警，不 fail），避免大纲逐渐漂移到"多小节薄写"？

---

# 第二部分：详细问题诊断

---

## 7) 证据准备阶段问题 (`evidence-draft`)

### 7.1 `evidence-draft/scripts/run.py` 问题

#### 问题 1: `blocking_missing` 字段被生成但从未强制执行

**位置**: `run.py:193-230`

```python
blocking_missing: list[str] = []
if not cite_keys:
    blocking_missing.append("no usable citation keys...")
if (fulltext_n + abstract_n) == 0 and title_n > 0:
    blocking_missing.append("title-only evidence...")
```

**问题**:
- 脚本生成了 `blocking_missing` 警告
- 但下游 skills (`subsection-writer`, `writer-context-pack`) 不检查此字段
- 写作在证据不足时仍然继续

**修改建议**:
- 在 `quality_gate.py` 增加 `evidence_drafts_blocking_missing` 检查
- 如果 `blocking_missing` 非空，阻断 C5 阶段

#### 问题 2: Claim candidates 被截断到 240 字符

**位置**: `run.py:494-495`

```python
if len(claim) > 240:
    claim = claim[:240].rstrip()
```

**问题**:
- 重要的 claim 可能被截断
- 丢失关键信息

**修改建议**:
- 增加截断阈值到 400 字符
- 或者按句子边界截断

#### 问题 3-7: 各种硬编码限制

- 对比数量限制、锚点提取正则不完整等

---

## 8) 上下文打包问题 (`writer-context-pack`)

### 8.1 `writer-context-pack/scripts/run.py` 问题

#### 问题 8: 截断阈值不一致

**位置**: `run.py:17-21, 224`

```python
def _trim(text: str, *, max_len: int = 260) -> str:
    # 默认 260 字符

"excerpt": _trim(hl.get("excerpt") or "", max_len=220),
    # 但 excerpt 只有 220 字符
```

**问题**:
- 不同字段使用不同的截断阈值
- 260 vs 220 字符不一致
- 重要上下文可能丢失

**修改建议**:
```python
# 统一截断阈值
TRIM_THRESHOLD = 400  # 增加到 400

def _trim(text: str, *, max_len: int = TRIM_THRESHOLD) -> str:
    ...
```

#### 问题 9: 丢弃项目时没有警告

**位置**: `run.py:188-190, 217-218, 250-252`

```python
if not cites:
    continue  # 静默丢弃
```

**问题**:
- 如果引用不在 bibkeys 中，整个项目被丢弃
- 没有记录丢弃事件
- 可能导致空的 context packs

**修改建议**:
```python
dropped_items = []
if not cites:
    dropped_items.append({
        "type": "anchor_fact",
        "reason": "citation not in allowed_bibkeys",
        "original": item
    })
    continue

# 在输出中记录
record["dropped_items"] = dropped_items
record["drop_rate"] = len(dropped_items) / total_items
```

#### 问题 10-13: 完整性问题

- 即使大多数字段为空，record 仍然被创建
- 下游 skills 收到不完整的 packs
- 没有最小完整性检查

---

## 9) 过渡生成问题 (`transition-weaver`)

### 9.1 `transition-weaver/scripts/run.py` 问题

#### 问题 14: `_stable_choice` 使用 SHA1 哈希导致确定性选择

**位置**: `run.py:11-16`

```python
def _stable_choice(key: str, options: list[str]) -> str:
    if not options:
        return ""
    digest = hashlib.sha1((key or "").encode("utf-8", errors="ignore")).hexdigest()
    idx = int(digest[:8], 16) % len(options)
    return options[idx]
```

**问题**:
- 相同的 subsection 对**永远**得到相同的过渡模板
- 没有基于内容的变化 - 纯粹是结构性的
- 如果 `3.1→3.2` 总是映射到同一模板，所有 survey 对于相似结构都有相同的过渡
- 缺乏多样性

**修改建议**:
- 增加内容相关的 seed（如 subsection title hash）
- 或者使用 LLM 生成过渡而非模板选择

#### 问题 15-17: 过渡模板问题

- 模板变体太少（每类型只有 3-4 个）
- 没有使用 subsection 内容生成过渡
- 没有过渡质量验证

---

## 10) 写作阶段问题 (`subsection-writer`)

### 10.1 `subsection-writer/SKILL.md` 设计问题

#### 问题 18: 引用范围是"指导语"而非强制约束

**位置**: `SKILL.md:127`

```markdown
Citation scope: citations must be allowed by `outline/evidence_bindings.jsonl`
```

**问题**:
- LLM 可以直接访问完整引用库，而不是只能看到 `allowed_bibkeys`
- "must be allowed" 只是建议，不是物理限制

**修改建议**:
- 创建 `citation-injector` skill 生成子集 bib 文件
- 修改 UNITS.csv 让写作 skill 只能看到子集

#### 问题 19-24: 段落结构问题

- Workflow 描述过于抽象
- 引用规则不够具体
- 没有段落结构模板
- 只有数量要求，没有结构要求

---

## 11) Quality Gate 问题 (`tooling/quality_gate.py`)

### 11.1 检查机制问题

#### 问题 25: 所有问题被同等对待，没有严重性级别

**位置**: `quality_gate.py` 全局

**问题**:
- 所有 `QualityIssue` 都是同一类型
- 没有 `severity: error/warning/info` 区分
- 小问题和大问题一样阻断流程

**修改建议**:
- 增加 `severity` 字段（error/warning/info）
- error 阻断流程，warning 记录但不阻断

#### 问题 26: 缺少 Claim 覆盖检查

**问题**:
- `evidence_drafts.jsonl` 产出了 `claim_candidates`
- 但 quality gate **不检查**这些 claims 是否被写入
- 导致证据被忽略

**应该有的检查**:
```python
def sections_claim_coverage(ws: Path) -> list[QualityIssue]:
    # 检查 claim_candidates 是否被覆盖
    # 覆盖率 < 80% 则 FAIL
```

#### 问题 27: 缺少过渡词检查

**问题**:
- 没有检查是否使用了过渡词
- 没有检查段落连贯性

#### 问题 28: 缺少引用嵌入检查

**位置**: `quality_gate.py` 缺失

**问题**:
- 没有检测句末堆砌模式: `. [@cite1; @cite2; @cite3]`
- 没有鼓励引用嵌入句中

#### 问题 29: 数字锚点检查使用错误的正则

**位置**: `quality_gate.py:2640, 2755`

```python
if re.search(r"\\d", blob):
    numeric_available.add(sid)
```

**问题**:
- `\\d` 是字面的反斜杠+d，不是数字匹配
- 应该是 `\d`

---

## 12) 写作质量流程问题

> 本节基于对 `subsection_briefs.jsonl`、`evidence_bindings.jsonl`、`writer_context_packs.jsonl` 与 `subsection-writer/SKILL.md` 数据流的详细分析。

### 12.1 `subsection_briefs.jsonl` 结构化约束被忽略

#### 问题 41: `paragraph_plan` 有 10 个详细段落计划但没有强制执行

**位置**: `outline/subsection_briefs.jsonl`

**数据结构**（每个 subsection 有 10 个段落计划）:
```json
{
  "para": 1,
  "intent": "Define scope, setup, and the subsection thesis (no pipeline jargon).",
  "focus": ["scope boundary", "key definitions", "thesis vs neighboring subsections"],
  "use_clusters": ["Agent frameworks / architectures"],
  "rq": "Which design choices in Agent loop and action spaces drive the major trade-offs?"
}
```

**问题**:
- 每个段落有明确的 `intent`（如 "Explain cluster A: core mechanism/architecture"）
- 有具体的 `focus` 列表
- 但 quality gate 只检查段落数量（>=9），不检查段落内容是否符合 intent

### 12.2 `evidence_bindings.jsonl` 约束不验证

#### 问题 46-48: 三层 `allowed_bibkeys` 约束被绕过

**数据结构**:
```json
{
  "sub_id": "3.1",
  "allowed_bibkeys": ["Yao2022React", "Shinn2023Reflexion", ...]
}
```

**问题**:
- 每个 subsection 有明确的 allowed_bibkeys 列表
- 理论上应该限制 LLM 只能使用这些引用
- 但 LLM 可以访问完整 ref.bib
- Quality gate 检查不够严格

### 12.3 `writer_context_packs.jsonl` 丰富结构被忽略

#### 问题 49-53: 丰富的写作指导被忽略

- `paragraph_plan` 的 10 段结构完全依赖 LLM 理解
- `comparison_cards.write_prompt` 没有追踪
- `anchor_facts` 没有消费追踪
- `limitation_hooks` 没有消费追踪

### 12.4 数据流断点问题

#### 问题 59-64: 定义但不验证

- `rq` (研究问题) 定义但不验证回答
- `contrast_hook` 定义但不强制使用
- `bridge_terms` 定义但不验证出现
- `scope_rule` 定义但不验证遵守

---

## 13) 与参考论文的差距分析

### 13.1 段落结构对比

| 维度 | 参考论文 (ref/agent-surveys) | 当前产出 | 差距 |
|------|------------------------------|----------|------|
| 段落结构 | 有张力（问题→方法→对比→限制） | 平铺直叙 | 缺少论证递进 |
| 引用密度 | 每段 3-5 个，自然嵌入 | 每段 1-2 个，句末堆砌 | 引用像"标签"不像"论据" |
| 对比写法 | "In contrast to A, B achieves..." | 分别描述 A 和 B | 缺少直接对比句 |
| 数字锚点 | 频繁且自然（"improves by 8.34%"） | 偶尔，生硬 | anchor_sheet 没被消费 |
| 段落过渡 | 承上启下（"Building on this..."） | 各段独立 | 缺少连接词 |
| 表格/图 | 对比表、taxonomy 图 | 有但不融入正文 | visuals 是附属品 |

### 13.2 具体示例对比

**参考论文写法 (2508.17281 第 2 页)**:
```
LLMs as agents can observe their environment, make decisions, and take
actions. Within this paradigm, single-agent LLM systems have demonstrated
promising performance in decision-making tasks. Single-agent systems such
as Reflexion [@Shinn2023], Toolformer [@Schick2023], and ReAct [@Yao2022]
have shown emergent capabilities in complex reasoning. However, scaling
to real-world scenarios remains challenging. To address these limitations,
multi-agent frameworks have emerged...
```

**当前产出写法**:
```
Agent systems have various capabilities. These include planning, reasoning,
and action execution. Several systems have been proposed. [@cite1; @cite2;
@cite3] These approaches show promising results.
```

**关键差异**:
1. 参考论文有具体系统名（Reflexion, Toolformer, ReAct）
2. 参考论文有转折（However）
3. 参考论文有因果（To address these limitations）
4. 参考论文引用是论据支撑，不是句末标签

---

## 14) 问题总结与优先级

### 14.1 问题统计

| 类别 | 问题数量 | 严重程度 |
|------|----------|----------|
| 证据准备 (`evidence-draft`) | 7 | 中 |
| 上下文打包 (`writer-context-pack`) | 6 | 中 |
| 过渡生成 (`transition-weaver`) | 4 | 低 |
| 写作阶段 (`subsection-writer`) | 7 | **高** |
| 质量检查 (`quality_gate.py`) | 6 | **高** |
| 数据流与依赖 | 4 | 中 |
| 其他 Skills | 6 | 中 |
| **写作质量流程问题** | **24** | **高** |
| **总计** | **64** | - |

### 14.2 优先级排序（按影响范围）

#### P0 - 阻断性问题（必须立即修复）

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| 18 | 引用范围是"指导语"而非强制约束 | `subsection-writer/SKILL.md:127` | 导致幻觉引用 |
| 29 | 数字锚点检查使用错误的正则 `\\d` | `quality_gate.py:2640` | 检查失效 |
| 31 | U100 可以访问完整 ref.bib | `UNITS.csv` | 无法阻止跨章节引用 |

#### P1 - 高优先级（严重影响质量）

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| 1 | `blocking_missing` 字段从未强制执行 | `evidence-draft/run.py:193` | 证据不足时继续写作 |
| 19 | evidence_drafts 被当作可选材料 | `subsection-writer/SKILL.md` | 证据包被忽略 |
| 26 | 缺少 Claim 覆盖检查 | `quality_gate.py` | Claims 被忽略 |
| 41 | paragraph_plan 10段计划被忽略 | `subsection_briefs.jsonl` | 段落结构混乱 |
| 50 | comparison_cards.write_prompt 没有追踪 | `writer_context_packs` | 对比内容被忽略 |
| 53 | 三层 allowed_bibkeys 约束被绕过 | 多处 | 引用范围失控 |

#### P2 - 中优先级（影响质量但不阻断）

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| 2 | Claim candidates 被截断到 240 字符 | `evidence-draft/run.py:494` | 信息丢失 |
| 8 | `_trim` 函数截断到 260 字符 | `writer-context-pack/run.py:17` | 信息丢失 |
| 14 | `_stable_choice` 使用 SHA1 哈希 | `transition-weaver/run.py:11` | 过渡缺乏多样性 |
| 27 | 缺少过渡词检查 | `quality_gate.py` | 段落不连贯 |
| 28 | 缺少引用嵌入检查 | `quality_gate.py` | 引用堆砌 |

#### P3 - 低优先级（可改进但不紧急）

| # | 问题 | 位置 | 影响 |
|---|------|------|------|
| 3-7 | 各种硬编码限制 | `evidence-draft/run.py` | 灵活性不足 |
| 9-13 | 各种硬编码限制 | `writer-context-pack/run.py` | 灵活性不足 |
| 15-17 | 过渡模板问题 | `transition-weaver/run.py` | 过渡质量 |
| 35-40 | 其他 Skills 问题 | 各 Skills | 边缘情况 |

### 14.3 需要修改的关键文件

| 文件 | 问题数量 | 修改类型 |
|------|----------|----------|
| `.codex/skills/subsection-writer/SKILL.md` | 10+ | 重写写作规范、增加结构约束 |
| `tooling/quality_gate.py` | 15+ | 增加检查项、修复 bug、验证约束覆盖 |
| `.codex/skills/evidence-draft/scripts/run.py` | 7 | 修复截断、增加验证 |
| `.codex/skills/writer-context-pack/scripts/run.py` | 6 | 修复截断、增加验证 |
| `.codex/skills/transition-weaver/scripts/run.py` | 4 | 增加变体、改进生成 |
| `templates/UNITS.arxiv-survey-latex.csv` | 2 | 修改依赖和输入 |
| **新增数据验证逻辑** | 24 | 验证 paragraph_plan/comparison_cards/allowed_bibkeys 等约束 |

---

## 15) 根本原因分析

### 15.1 设计层面的根本问题

Pipeline 的核心设计缺陷可以归结为三个根本原因：

#### 1. "软约束"架构

```
当前设计:
evidence_bindings → [参考材料] → LLM → [可能忽略] → 输出

应该的设计:
evidence_bindings → [物理限制] → LLM → [只能看到允许的] → 输出
```

**问题**: 所有约束都是"建议"而非"强制"。LLM 可以完全忽略 `allowed_bibkeys`、`claim_candidates`、`anchor_facts` 等。

**解决方向**:
- 创建 `citation-injector` skill 生成子集 bib 文件
- 修改 UNITS.csv 让写作 skill 只能看到子集
- 在 quality_gate 中严格验证约束遵守情况

#### 2. "事后检查"而非"事前拦截"

```
当前流程:
写作 → 检查 → 发现问题 → 修复 → 可能引入新问题

应该的流程:
规划 → 检查规划 → 写作 → 检查写作
```

**问题**: Quality Gate 在写作完成后才运行，此时错误已经发生。修复可能引入新错误，形成循环。

**解决方向**:
- 创建 `subsection-planner` skill 先生成段落计划
- 在写作前验证计划是否符合约束
- 让 LLM 分两步：先规划后写作

#### 3. 信息在传递中丢失

```
数据流:
原始证据 (完整)
  → evidence_drafts (截断到 240 字符)
    → writer_context_packs (截断到 260 字符)
      → LLM (只看到截断后的)
        → 输出 (信息丢失)
```

**问题**: 每一层都有截断和过滤，累积信息丢失严重。

### 15.2 写作质量问题的根源

写作质量差的根本原因不是 LLM 能力不足，而是：

1. **没有给 LLM 足够的写作规范**
   - 缺少段落结构模板
   - 缺少句式示例
   - 缺少过渡词要求

2. **没有强制消费证据**
   - `claim_candidates` 是可选的
   - `anchor_facts` 是可选的
   - `concrete_comparisons` 是可选的

3. **检查项不完整**
   - 只检查数量（段落数、引用数）
   - 不检查质量（结构、对比、锚点使用）

---

# 第三部分：改进方案

---

## 16) 改进策略概述

### 16.1 改进原则

1. **硬约束优先**: 将"软约束"转换为"硬约束"，物理限制 LLM 的访问范围
2. **事前拦截**: 在写作前验证计划，而非写作后修复
3. **信息保留**: 减少截断，保留关键信息
4. **检查完整**: 增加缺失的检查项，验证约束覆盖

### 16.2 改进优先级

| 优先级 | 改进项 | 影响范围 |
|--------|--------|----------|
| P0 | 修复 quality_gate.py 中的 bug | 立即生效 |
| P0 | 创建 citation-injector skill | 阻止幻觉引用 |
| P1 | 增强 quality_gate 检查项 | 提高写作质量 |
| P1 | 重写 subsection-writer/SKILL.md | 改善段落结构 |
| P2 | 修复截断问题 | 减少信息丢失 |
| P3 | 改进过渡生成 | 提高连贯性 |

---

## 17) 新增 Skills

### 17.1 `citation-injector` Skill

**目的**: 为每个 subsection 生成子集 bib 文件，物理限制 LLM 的引用范围

**输入**:
- `outline/evidence_bindings.jsonl`
- `citations/ref.bib`

**输出**:
- `sections/.allowed_cites/<sub_id>.bib` (每个 subsection 一个)

**实现逻辑**:
```python
def generate_allowed_bib(sub_id: str, bindings: dict, full_bib: Path) -> str:
    allowed_keys = set(bindings.get(sub_id, {}).get("allowed_bibkeys", []))
    full_entries = parse_bib(full_bib)

    subset = [e for e in full_entries if e.key in allowed_keys]
    return format_bib(subset)
```

### 17.2 `subsection-planner` Skill

**目的**: 在写作前生成段落计划，先验证计划再写作

**输入**:
- `outline/writer_context_packs.jsonl`
- `outline/subsection_briefs.jsonl`

**输出**:
- `sections/.plans/<sub_id>.plan.md`

---

## 18) 修改现有 Skills

### 18.1 `subsection-writer/SKILL.md` 重写

#### 18.1.1 增加段落结构模板

**新增内容**:
```markdown
### Paragraph Structure Templates

**Type A: Claim-Evidence Paragraph**
```
[Opening claim with system name] Systems such as X [@cite1] and Y [@cite2]
demonstrate [specific capability]. [Evidence sentence with numbers]
X achieves [metric] on [benchmark], while Y reports [metric].
[Synthesis sentence] Collectively, these results suggest [insight].
```

**Type B: Comparison Paragraph**
```
[Setup] A key design axis is [dimension]. [Contrast] In contrast to
[approach A] [@cite1], which [description], [approach B] [@cite2]
[alternative description]. [Trade-off] This trade-off manifests as
[concrete consequence]. [Implication] For practitioners, this means [guidance].
```
```

#### 18.1.2 增加引用嵌入规则

```markdown
### Citation Embedding Rules

**REQUIRED**: Citations must be embedded with system names
- GOOD: "ReAct [@Yao2022React] demonstrates..."
- BAD: "This is important. [@Yao2022React]"

**FORBIDDEN**: Citation piling at sentence end
- BAD: "...action validity. [@cite1; @cite2; @cite3]"
```

---

## 19) Quality Gate 增强

### 19.1 Bug 修复

#### 19.1.1 修复数字锚点检查正则

**位置**: `quality_gate.py:2640, 2755`

```python
# 原来（错误）
if re.search(r"\\d", blob):
    numeric_available.add(sid)

# 修改后（正确）
if re.search(r"\d", blob):
    numeric_available.add(sid)
```

### 19.2 新增检查函数

#### 19.2.1 `sections_claim_coverage` - Claim 覆盖检查

```python
def sections_claim_coverage(ws: Path) -> list[QualityIssue]:
    """检查 claim_candidates 是否被覆盖"""
    issues = []

    # 读取 evidence_drafts
    drafts = load_jsonl(ws / "outline" / "evidence_drafts.jsonl")

    for draft in drafts:
        sub_id = draft.get("sub_id")
        claims = draft.get("claim_candidates", [])
        section_file = ws / "sections" / f"S{sub_id.replace('.', '_')}.md"

        if not section_file.exists():
            continue

        text = section_file.read_text().lower()
        covered = sum(1 for c in claims if any(kw in text for kw in c.get("keywords", [])))
        coverage = covered / len(claims) if claims else 1.0

        if coverage < 0.8:
            issues.append(QualityIssue(
                f"Section {sub_id} has low claim coverage: {coverage:.0%}",
                severity="error"
            ))

    return issues
```

#### 19.2.2 `sections_citation_embedding` - 引用嵌入检查

```python
def sections_citation_embedding(ws: Path) -> list[QualityIssue]:
    """检测引用堆砌模式"""
    issues = []
    pile_pattern = re.compile(r"\.\s*\[@[^\]]+;\s*@[^\]]+;\s*@[^\]]+\]")

    for section_file in (ws / "sections").glob("S*.md"):
        text = section_file.read_text()
        matches = pile_pattern.findall(text)

        if len(matches) >= 3:
            issues.append(QualityIssue(
                f"{section_file.name} has {len(matches)} citation piles",
                severity="warning"
            ))

    return issues
```

---

## 20) 实施计划

### 20.1 Phase 1: Bug 修复（立即）

| 任务 | 文件 | 预期效果 |
|------|------|----------|
| 修复正则 `\\d` → `\d` | `quality_gate.py:2640, 2755` | 数字锚点检查生效 |

### 20.2 Phase 2: 硬约束实现

| 任务 | 文件 | 预期效果 |
|------|------|----------|
| 创建 `citation-injector` skill | 新建 `.codex/skills/citation-injector/` | 物理限制引用范围 |
| 修改 UNITS.csv | `templates/UNITS.*.csv` | U100 只能看到子集 bib |
| 增加引用范围检查 | `quality_gate.py` | 严格验证引用在 allowed_bibkeys 内 |

### 20.3 Phase 3: Quality Gate 增强

| 任务 | 文件 | 预期效果 |
|------|------|----------|
| 增加 `sections_claim_coverage` | `quality_gate.py` | 验证 claim 覆盖率 >=80% |
| 增加 `sections_transition_words` | `quality_gate.py` | 验证过渡词使用 |
| 增加 `sections_citation_embedding` | `quality_gate.py` | 检测引用堆砌 |
| 增加 `sections_anchor_usage` | `quality_gate.py` | 验证数字锚点使用 |

### 20.4 Phase 4: SKILL.md 重写

| 任务 | 文件 | 预期效果 |
|------|------|----------|
| 增加段落结构模板 | `subsection-writer/SKILL.md` | 改善段落结构 |
| 增加引用嵌入规则 | `subsection-writer/SKILL.md` | 减少引用堆砌 |
| 增加强制消费规则 | `subsection-writer/SKILL.md` | 确保证据被使用 |

---

## 21) 结论

### 21.1 核心发现

本报告详细记录了 Pipeline 中的 **64 个问题**，分布在 8 个主要类别中。

**核心发现**：
1. Pipeline 的"软约束"设计是根本问题
2. Quality Gate 是"事后检查"而非"事前拦截"
3. 信息在多层传递中严重丢失
4. 写作规范不够具体，导致段落质量差
5. **新发现**：丰富的结构化数据（paragraph_plan、comparison_cards、allowed_bibkeys 等）被完全忽略

### 21.2 最紧急的问题

**P0 级别（必须立即修复）**：
1. 问题 #18: 引用范围是"指导语"而非强制约束
2. 问题 #29: 数字锚点检查使用错误的正则 `\\d`
3. 问题 #31: U100 可以访问完整 ref.bib

**写作质量流程的核心问题**：
1. 问题 #41: `paragraph_plan` 10段计划被忽略
2. 问题 #50: `comparison_cards.write_prompt` 没有追踪
3. 问题 #53: 三层 `allowed_bibkeys` 约束被绕过

### 21.3 需要修改的核心文件

| 文件 | 修改类型 |
|------|----------|
| `subsection-writer/SKILL.md` | 重写写作规范、增加结构约束 |
| `quality_gate.py` | 增加检查项、修复 bug、验证约束覆盖 |
| `UNITS.csv` | 修改依赖和输入、限制 ref.bib 访问 |

### 21.4 问题分布可视化

```
证据准备阶段:     █████████████ (13)
上下文打包:       ██████ (6)
过渡生成:         ████ (4)
写作阶段:         ███████ (7)
质量检查:         ██████ (6)
数据流:           ████ (4)
其他 Skills:      ██████ (6)
写作质量流程:     ████████████████████████ (24)
─────────────────────────────
总计:             64 个问题
```

---

## 22) Skills 详细问题分析

### 22.1 `subsection-writer` Skill 深度分析

**Skill 路径**: `.codex/skills/subsection-writer/`

#### A. SKILL.md 设计问题

**问题 A1: Workflow 描述过于抽象**

**位置**: `SKILL.md:60-90`

```markdown
## Workflow
1. Load context from writer_context_packs or fall back to subsection_briefs
2. Draft paragraphs following the paragraph_plan
3. Embed citations naturally
4. Run skeptic pass
```

**问题**:
- "Draft paragraphs following the paragraph_plan" 没有具体说明如何 follow
- "Embed citations naturally" 没有定义什么是 "naturally"
- 没有提供具体的段落写作步骤
- LLM 可以自由解释这些指令

**修改建议**:
```markdown
## Workflow (修改后)
1. Load context from writer_context_packs
2. For each paragraph in paragraph_plan:
   a. Read the intent and focus fields
   b. Identify citations from use_clusters
   c. Write opening sentence with system name + citation
   d. Add evidence sentence with numbers from anchor_facts
   e. Add synthesis sentence connecting multiple papers
3. Verify each paragraph has:
   - At least 1 citation embedded with system name
   - At least 1 concrete noun (benchmark/dataset/tool)
   - Connection to previous paragraph (if not first)
```

**问题 A2: 引用规则不够具体**

**位置**: `SKILL.md:125-130`

```markdown
Citation scope: citations must be allowed by `outline/evidence_bindings.jsonl`
Evidence-first: cite density depends on `draft_profile`
```

**问题**:
- 没有说明引用应该放在句子的什么位置
- 没有禁止句末堆砌
- 没有要求引用与系统名关联

**修改建议**:
```markdown
### Citation Rules (新增)

**位置规则**:
- REQUIRED: 引用必须与系统/方法名关联
  - GOOD: "ReAct [@Yao2022React] demonstrates..."
  - BAD: "This is important. [@Yao2022React]"

**禁止模式**:
- FORBIDDEN: 句末堆砌 (>=2 citations at sentence end)
  - BAD: "...action validity. [@cite1; @cite2; @cite3]"

**密度规则**:
- 每段至少 2 个引用
- 每个引用必须有对应的具体描述
```

### 22.2 `writer-context-pack` Skill 深度分析

**Skill 路径**: `.codex/skills/writer-context-pack/`

#### A. 数据打包问题

**问题 A1: 截断阈值不一致**

**位置**: `run.py:17-21, 224`

```python
def _trim(text: str, *, max_len: int = 260) -> str:
    # 默认 260 字符

"excerpt": _trim(hl.get("excerpt") or "", max_len=220),
    # 但 excerpt 只有 220 字符
```

**问题**:
- 不同字段使用不同的截断阈值
- 260 vs 220 字符不一致
- 重要上下文可能丢失

**修改建议**:
```python
# 统一截断阈值
TRIM_THRESHOLD = 400  # 增加到 400

def _trim(text: str, *, max_len: int = TRIM_THRESHOLD) -> str:
    ...
```

#### B. 完整性问题

**问题 B1: 没有最小完整性检查**

**位置**: `run.py:273-294`

**问题**:
- 即使大多数字段为空，record 仍然被创建
- 下游 skills 收到不完整的 packs
- 没有警告机制

**修改建议**:
```python
def check_completeness(record):
    score = 0
    if len(record.get("anchor_facts", [])) >= 2:
        score += 1
    if len(record.get("comparison_cards", [])) >= 1:
        score += 1
    if len(record.get("limitation_hooks", [])) >= 1:
        score += 1

    record["completeness_score"] = score
    record["is_complete"] = score >= 2

    if not record["is_complete"]:
        record["completeness_warning"] = "Pack may be insufficient for quality writing"

    return record
```

### 22.3 `transition-weaver` Skill 深度分析

**Skill 路径**: `.codex/skills/transition-weaver/`

#### A. 模板问题

**问题 A1: 模板变体太少**

**位置**: `run.py:114-163`

```python
# 每种过渡类型只有 3-4 个变体
SAME_CHAPTER_VARIANTS = [
    f"Next, we move from {a_title} to {b_title}...",
    f"Building on {a_title}, we turn to {b_title}...",
    f"After {a_title}, {b_title} shifts...",
    f"To keep the thread continuous...",
]
```

**问题**:
- 每类型只有 3-4 个变体
- 相同结构的 survey 会有相同的过渡
- 读起来像机械生成

**修改建议**:
```python
# 增加到每类型 10+ 个变体
SAME_CHAPTER_VARIANTS = [
    # 原有
    f"Next, we move from {a_title} to {b_title}...",
    f"Building on {a_title}, we turn to {b_title}...",
    # 新增
    f"Having established {a_title}, we now examine {b_title}...",
    f"The discussion of {a_title} naturally leads to {b_title}...",
    f"Complementing {a_title}, {b_title} addresses...",
    f"While {a_title} covered [aspect], {b_title} explores...",
    f"With {a_title} as foundation, {b_title} extends...",
    f"From {a_title}, we transition to {b_title}...",
    f"{b_title} builds directly on {a_title} by...",
    f"The insights from {a_title} inform our discussion of {b_title}...",
]
```

### 22.4 `anchor-sheet` Skill 深度分析

**Skill 路径**: `.codex/skills/anchor-sheet/`

#### A. 锚点提取问题

**问题 A1: 数字锚点提取不完整**

**问题**:
- 只提取明显的百分比和数字
- 遗漏复杂格式的数字（如 "1.5B parameters"）
- 遗漏比较性数字（如 "2x faster"）

**修改建议**:
```python
# 增强数字提取正则
NUMBER_PATTERNS = [
    r"\d+\.?\d*%",           # 百分比: 8.34%
    r"\d+\.?\d*x",           # 倍数: 2.3x
    r"\d+\.?\d*[KMB]",       # 缩写: 1.5B, 119K
    r"\d+\.?\d*\s*(times|fold)",  # 倍数文字
    r"(up to|over|about)\s*\d+",  # 约数
]
```

### 22.5 `section-merger` Skill 深度分析

**Skill 路径**: `.codex/skills/section-merger/`

#### A. 合并逻辑问题

**问题 A1: 不验证 manifest 约束**

**问题**:
- 只检查文件是否存在
- 不验证 `sections_manifest.jsonl` 中的约束
- 不检查 `allowed_bibkeys` 是否被遵守

**修改建议**:
```python
def validate_before_merge(sections_dir, manifest):
    """合并前验证"""
    issues = []

    for entry in manifest:
        section_file = sections_dir / entry["filename"]
        allowed_keys = set(entry.get("allowed_bibkeys", []))

        # 提取实际使用的引用
        text = section_file.read_text()
        used_keys = extract_citations(text)

        # 检查越界引用
        out_of_scope = used_keys - allowed_keys
        if out_of_scope:
            issues.append({
                "file": entry["filename"],
                "issue": "out_of_scope_citations",
                "citations": list(out_of_scope)
            })

    return issues
```

---

## 23) 实例分析

> 本部分基于 `e2e-agent-survey-citeboost` workspace 中的实际生成输出进行分析。

### 23.1 S3_1.md 实例分析

**文件**: `sections/S3_1.md` (Agent loop and action spaces)
**段落数**: 16 段
**字符数**: ~11,000 字符
**引用数**: 18 个唯一引用

### 23.2 问题实例

#### 问题实例 1: 引用堆砌在句末

**当前写法**:
```markdown
These representations are not cosmetic: they constrain what the agent can
plan over, what can be validated, and what can be logged for debugging.
[@Yao2022React; @Kim2025Bridging]
```

**问题分析**:
- 引用放在段落末尾，像"标签"
- 没有与具体系统名关联
- 读者无法知道哪个观点来自哪篇论文

**应该的写法**:
```markdown
These representations are not cosmetic. ReAct [@Yao2022React] demonstrates
that the action format constrains what the agent can plan over, while
SCL [@Kim2025Bridging] shows how it affects what can be validated and
logged for debugging.
```

#### 问题实例 2: 缺少直接对比

**当前写法**:
```markdown
Some systems use structured actions. Other systems use natural language.
Both approaches have trade-offs.
```

**应该的写法**:
```markdown
A key design axis is the action representation format. In contrast to
ReAct [@Yao2022React], which uses structured thought-action-observation
tuples, Toolformer [@Schick2023] embeds tool calls directly in natural
language. This trade-off manifests in debuggability versus flexibility:
structured formats enable systematic error analysis, while natural
language allows more expressive tool composition.
```

---

# 第四部分：Workspace 实例锐评

---

## 24) `e2e-agent-survey-skillcontracts-20260114-2332` 锐评

> 本节对 `workspaces/e2e-agent-survey-skillcontracts-20260114-2332` 进行深度分析，对比 citeboost workspace 的产出质量，识别改进效果与残留问题。

### 24.1 基本信息

| 维度 | 数据 |
|------|------|
| Pipeline | `arxiv-survey-latex` |
| 最终状态 | **BLOCKED at U100** (subsection-writer script failed) |
| 论文收集 | 800 papers raw, 220 paper notes, 2202 BibTeX lines |
| 大纲结构 | 6 H2 sections, 8 H3 subsections |
| 已完成章节 | S1.md, S3_1.md, S3_2.md, S4_1.md, abstract.md, discussion.md, conclusion.md |
| 缺失章节 | S4_2.md, S5_1.md, S5_2.md, S6_1.md, S6_2.md |

### 24.2 写作质量分析（对比 citeboost）

#### 显著进步（契约补强生效）

**1. 引用嵌入方式彻底改进**

citeboost 写法（问题写法）:
```markdown
These representations are not cosmetic: they constrain what the agent can
plan over, what can be validated, and what can be logged for debugging.
[@Yao2022React; @Kim2025Bridging]
```

skillcontracts 写法（正确写法）:
```markdown
ReAct [@Yao2022React] illustrates the free-form end of the spectrum, where
reasoning traces and actions are intertwined in text; by contrast, the
Structured Cognitive Loop explicitly separates phases to make control
decisions auditable [@Kim2025Bridging].
```

**分析**: 引用不再是句末堆砌的"标签"，而是与具体系统名绑定的"论据"。读者能清楚知道哪个观点来自哪篇论文。

**2. 对比句式显著增加**

S3_1.md 实例:
```markdown
In contrast, structured loops and schema-backed actions constrain the
agent's output space so that states and transitions are easier to
attribute to components [@Kim2025Bridging].
```

S4_1.md 实例:
```markdown
In contrast to free-form chain-of-thought, these approaches treat planning
as a structured policy over states and transitions.
```

**分析**: "In contrast to..."、"by contrast"、"whereas" 等对比连接词频繁出现，段落不再是"A 一段 B 一段"的平铺罗列。

**3. 评测锚点有具体数字**

S3_1.md:
```markdown
AgentSwift reports an average gain of 8.34% across seven benchmarks
spanning embodied, math, web, tool, and game domains [@Li2025Agentswift].
```

```markdown
...collecting 1,170 trajectories for fine-tuning and achieving stronger
performance than baselines trained with 119k samples...
```

S4_1.md:
```markdown
...a 1.5B parameter model trained with single-turn GRPO is reported to
outperform larger baselines up to 14B parameters [@Hu2025Training].
```

```markdown
...a self-guided reasoning baseline completes only 13.5%, 16.5%, and 75.7%
of subtasks while requiring 86.2%, 118.7%, and 205.9% more model queries...
```

**分析**: 数字锚点不再是可有可无的装饰，而是支撑论点的核心证据。`anchor-sheet` 的契约补强明显生效。

**4. 跨论文综合段落**

S3_1.md 结尾:
```markdown
Taken together, we can view current work as spanning two clusters:
(i) **architectural loop design** that makes actions structured and
optimizable (e.g., Structured Cognitive Loop, AgentSwift, EvoRoute)
[@Kim2025Bridging; @Li2025Agentswift; @Zhang2026Evoroute], and
(ii) **environment- and domain-grounded action spaces** that tie actions
to external systems and their constraints...
```

**分析**: 不再是逐篇描述，而是提炼共性/差异，形成 cross-paper synthesis。

**5. 局限写法具体化**

S3_1.md:
```markdown
First, many comparisons are only weakly controlled: performance changes
can reflect differences in environment difficulty, tool availability, or
logging fidelity rather than the action representation itself...
```

```markdown
Second, action validity is still a major bottleneck in real-world
interfaces; even when feasibility is demonstrated, lack of unified APIs
and ambiguity in requests can make actions unreliable...
```

**分析**: 局限不再是泛泛的"未来工作"，而是指出具体的失败模式和边界条件。

### 24.3 残留问题

#### 问题 1: Pipeline 在 U100 崩溃

**现象**: STATUS.md 显示 `U100 (subsection-writer): script failed`

**时间线分析**:
- 00:01:02 - U030 (paper-notes) 完成
- 00:01:59 - U100 (subsection-writer) 失败
- 但 S3_1.md 等文件在 00:09-00:14 被创建

**推测**: 可能是手动重试或 selfloop 修复后产出了高质量章节，但 pipeline 状态没有更新。

**改进建议**:
- U100 的 script 需要更好的错误处理和恢复机制
- 应该记录具体的失败原因（而非泛泛的"script failed"）

#### 问题 2: 5/8 章节缺失

**缺失文件**: S4_2.md, S5_1.md, S5_2.md, S6_1.md, S6_2.md

**影响**: 只有 37.5% 的 H3 章节被写完，导致最终 draft 无法合并。

**可能原因**:
1. Pipeline 崩溃后没有继续
2. writer_context_packs 为这些章节的 completeness 不足
3. quality gate 在某些检查上 block 了后续章节

**改进建议**:
- 增加 "partial progress" 保存机制，避免一个章节失败导致全部丢失
- 为每个 H3 生成独立的 completeness report，提前识别"不可写"的章节

#### 问题 3: 部分段落仍偏"百科式"

S4_1.md 部分写法:
```markdown
Memory and retrieval can change what planning loops need to do. MemR$^3$
frames memory retrieval as an agent system with a router that selects
among retrieve, reflect, and answer actions...
```

**问题**: 虽然引用嵌入正确，但这段更像"功能描述"而非"论证分析"。缺少：
- 与前文的张力连接（为什么提 memory？解决什么问题？）
- 评价性语句（这个设计的优劣是什么？）

**对比参考论文写法**:
```
To address the limitation that planning cannot access historical context,
MemR³ introduces a router-based memory system. However, this design
introduces new trade-offs: the router itself becomes a potential failure
point, and memory access patterns can leak information about the agent's
reasoning strategy...
```

**改进建议**:
- `subsection-writer` 的 paragraph_plan 需要更明确的"intent 类型"标注
- 每段需要 self-check: "这段的论证目的是什么？是描述还是分析？"

#### 问题 4: 段落之间缺乏逻辑连接（核心问题）

**现象分析**：虽然单个段落质量不错，但段落之间的逻辑关系很弱。

**S3_1.md 段落结构**：
```
Para 1: 定义 action（引入）
Para 2: Axis 1 - granularity and structure
Para 3: Axis 2 - loop as optimization object  ← 为什么从 Axis 1 跳到这里？
Para 4: Axis 3 - environment affordances     ← 和 Axis 2 什么关系？
Para 5: Domain-specific settings             ← 突然换话题
Para 6: Evaluation                           ← 又换话题
Para 7: Training signals                     ← 再换话题
Para 8: Clusters synthesis                   ← 强行总结
Para 9: Limitations
Para 10: Transition to next section
```

**问题**：
- 每段都在介绍一个"新轴"或"新话题"，但缺乏**为什么这个轴跟在上一个轴后面**的解释
- 段落之间的连接词很少（缺少 "This naturally leads to..."、"However, this raises..."、"Building on this insight..."）
- 读起来像"论文清单"而非"论证链"

**对比参考论文写法**：
```markdown
[Para 1] Action granularity determines what can be verified...

[Para 2] However, granularity alone does not determine quality—the loop
itself can be treated as an optimization target. AgentSwift shows that
searching over loop configurations yields 8.34% gains, suggesting that
the meta-level design choice matters as much as the action representation.

[Para 3] This optimization perspective naturally raises a question: what
happens when the environment itself provides structure? ToolGym and
EnvScaler show that "better loops" can sometimes reflect "better environments"...
```

**当前写法**：
```markdown
[Para 1] One common axis is **granularity and structure**...

[Para 2] A second axis is whether the loop is treated as an **object of
optimization**...  ← 没有解释为什么引入这个"第二轴"

[Para 3] Optimization choices interact with the **environment's action
affordances**...  ← "interact" 太弱，没有说清楚什么交互
```

**根本原因**：
- `paragraph_plan` 只规定了每段的 topic，没有规定段落之间的 **logical connector**
- writer 按 topic 列表逐段写，没有思考"这段为什么要跟在上段后面"
- 缺少 **running example**（好的 survey 会用一个具体例子串联全节）

#### 问题 5: "Clusters synthesis" 模板化

**S3_1.md 结尾**：
```markdown
Taken together, we can view current work as spanning two clusters:
(i) **architectural loop design**... and
(ii) **environment- and domain-grounded action spaces**...
```

**S3_2.md 结尾**：
```markdown
Taken together, we can contrast two orchestration philosophies.
One treats orchestration primarily as **efficient tool retrieval**...
The other treats orchestration as a **safety- and attack-surface problem**...
```

**S4_1.md 结尾**：
```markdown
Taken together, current planning loops can be grouped into three clusters.
RL-trained planners...
Hybrid symbolic-control approaches...
Domain-structured planners...
```

**问题**：
- 每节结尾都是 "Taken together, we can view/contrast/group... into N clusters"
- 这是好的 synthesis 模式，但**每节都用**就变成了模板
- 更严重的是：clusters 划分感觉是**事后强加**的，而非从论证中自然涌现

**改进建议**：
- Clusters 应该在节的**开头**作为组织框架预告，而非结尾强行总结
- 或者：不同的节使用不同的 synthesis 方式（有些用 clusters，有些用 timeline，有些用 trade-off matrix）

#### 问题 6: 章节末尾的保守声明过于模板化

S3_1.md 结尾:
```markdown
...security-oriented action spaces make explicit that autonomy must be
balanced with governance, because the same "expressive" actions that
enable penetration testing can also enable misuse [@Abdulzada2025Vulnerability].
```

S4_1.md 结尾:
```markdown
Despite progress, evidence remains heterogeneous and often abstract-level,
so broad claims about general planning superiority should be treated as
provisional.
```

**问题**: 每节都有类似的"证据还不够充分，claims 需要谨慎"的声明，形成模板感。

**改进建议**:
- 保守性声明应该针对该节的具体 claims，而非泛泛的"evidence is heterogeneous"
- 可以用具体例子说明哪些 claims 有强证据、哪些是 provisional

#### 问题 7: 缺少节内的"论证主线"

**参考论文的写法**（有论证主线）：
```
本节论证：action representation 决定了 agent 的 verifiability ceiling

Para 1: 引入问题 - 为什么 action rep 重要
Para 2: 证据 1 - free-form 的问题（ReAct 的 debugging 困难）
Para 3: 证据 2 - structured 的优势（SCL 的 attribution）
Para 4: 反驳/复杂化 - 但 structured 也有代价（flexibility loss）
Para 5: 综合 - 因此选择取决于 verifiability vs flexibility 的权衡
```

**当前写法**（无论证主线，只有话题列表）：
```
本节介绍：action space design 的各种 axes

Para 1: 引入 - action space 很重要
Para 2: Axis 1 - granularity
Para 3: Axis 2 - optimization
Para 4: Axis 3 - environment
Para 5: Domain examples（列举）
Para 6: Evaluation（列举）
Para 7: Training（列举）
Para 8: Clusters（强行总结）
```

**问题**：
- 没有一个贯穿全节的**thesis**（核心论点）
- 每段都在"介绍一个方面"，而非"推进一个论证"
- 缺少 **tension → resolution** 的叙事弧

#### 问题 8: 句子层面的逻辑连接词不足

**统计**：

| 连接词类型 | S3_1.md 出现次数 | 参考论文（同长度）预期 |
|-----------|------------------|----------------------|
| However / But | 1 | 5-8 |
| Therefore / Thus / Hence | 1 | 4-6 |
| In contrast / Unlike | 3 | 3-5 ✓ |
| Building on / Following | 0 | 2-4 |
| This raises / This suggests | 1 | 3-5 |

**问题**：
- "In contrast" 用得还可以，但 **因果连接词** (Therefore, Thus) 严重不足
- **承上启下连接词** (Building on, Following, This raises) 几乎没有
- 导致段落像"孤岛"而非"链条"

### 24.4 是否需要润色遍（Polishing Pass）？

**答案：需要，但需要结构化的润色，而非自由润色**

#### 当前问题：writer 写完即结束

现有流程：
```
subsection-writer → sections/*.md → section-merger → DRAFT.md → global-reviewer
```

问题：
- `global-reviewer` 只检查 terminology consistency 和 citation hygiene
- **不检查逻辑连贯性**
- 写完的章节直接进入 merge，没有"论证润色"步骤

#### 建议增加：Logic Polishing Pass

**新增 skill**: `section-logic-polisher`

**输入**: 单个 `sections/S*.md` + 该节的 `subsection_briefs`

**检查清单**:
1. **Thesis check**: 该节是否有一个可识别的 central argument？
2. **Flow check**: 每两段之间是否有 logical connector？
3. **Evidence-to-claim ratio**: 每个 claim 是否有 ≥1 evidence sentence？
4. **Tension-resolution**: 是否存在 "problem → solution" 或 "limitation → workaround" 结构？

**输出**: 带标注的 `sections/S*.md.polished` 或 `sections/S*.logic_issues.json`

**执行时机**: 在 `section-merger` 之前，对每个完成的章节运行

#### Polishing 应该做什么

| 阶段 | 当前 | 建议 |
|------|------|------|
| 写作后立即 | 无检查 | **Logic scan**: 检测孤立段落、缺少连接词 |
| Merge 前 | 无检查 | **Coherence pass**: 确保节内有 thesis 和 flow |
| Global review | 只检查术语 | **增加**: Cross-section flow 检查 |

#### Polishing 不应该做什么

- ❌ 大幅重写段落内容（应在 writer 阶段解决）
- ❌ 添加新的引用或证据（应在 evidence-draft 阶段解决）
- ❌ 改变节的 scope 或 clusters 划分（应在 outline 阶段解决）

**核心原则**: Polishing 只做**连接**（加 connectors、调整段落顺序、补 thesis statement），不做**内容**。

### 24.5 问题→Skills/Pipeline 改进映射

> 以下将上述 badcase 抽象为可落地的 skill 合同改进。

#### 映射 1: 段落逻辑连接缺失 → `subsection-briefs` + `subsection-writer` 改进

| Badcase | 根因分析 | Skill 改进 |
|---------|----------|-----------|
| 段落之间缺少 "However/Therefore/Building on this" | `paragraph_plan` 只规定 topic，不规定 **inter-paragraph connector** | `subsection-briefs`: 每个 para 增加 `connector_to_prev` 字段（如 "contrast", "consequence", "extension"） |
| 读起来像"论文清单"而非"论证链" | writer 按列表逐段写，无全局 thesis 意识 | `subsection-writer`: 开头必须写 **thesis statement**（明确该节要论证什么） |

**`subsection-briefs/SKILL.md` 具体修改**:
```yaml
# paragraph_plan 新增字段
- para: 3
  intent: "Compare optimization-centric vs environment-centric views"
  connector_to_prev: "consequence"  # 新增：说明这段为什么跟在上段后面
  connector_phrase: "This optimization perspective naturally raises..."  # 新增：建议连接句
```

**`subsection-writer/SKILL.md` 具体修改**:
```markdown
### Thesis Statement Requirement (新增)
每节的**第一段最后一句**必须是 thesis statement，格式：
"This subsection argues/shows/surveys that [central claim]."

示例：
- "This subsection argues that action representation determines the ceiling of verifiability."
- "This subsection surveys how tool orchestration creates both efficiency gains and security risks."

Quality gate 检查：第一段是否包含 "argues/shows/surveys that" 句式。
```

#### 映射 2: Clusters 模板化 → `outline-builder` + `chapter-briefs` 改进

| Badcase | 根因分析 | Skill 改进 |
|---------|----------|-----------|
| 每节结尾都是 "Taken together... N clusters" | `chapter-briefs` 没有规定 synthesis 方式的**多样性** | `chapter-briefs`: 为每个 H2 指定 synthesis_mode（clusters / timeline / trade-off matrix / case-study） |
| Clusters 是事后强加而非自然涌现 | Clusters 在写作阶段才出现，outline 阶段没有预告 | `outline-builder`: H3 级别就预告 "这节属于哪个 cluster"，写作时只需呼应 |

**`chapter-briefs/SKILL.md` 具体修改**:
```yaml
# 每个 H2 的 brief 新增字段
chapter_id: "3"
synthesis_mode: "clusters"  # 可选: clusters, timeline, trade-off_matrix, case_study, tension_resolution
synthesis_preview: "Will contrast 'architectural loop design' vs 'domain-grounded action spaces'"
```

**`outline-builder/SKILL.md` 具体修改**:
```yaml
# outline.yml 新增 cluster_tag 字段
sections:
  - id: "3.1"
    title: "Agent loop and action spaces"
    cluster_tag: "architectural"  # 预告这节属于哪个 cluster
  - id: "3.2"
    title: "Tool interfaces and orchestration"
    cluster_tag: "interface"
```

#### 映射 3: 节内论证主线缺失 → `subsection-briefs` 改进

| Badcase | 根因分析 | Skill 改进 |
|---------|----------|-----------|
| 没有贯穿全节的 thesis | `subsection_briefs` 只有 topic 和 axes，没有 **central_argument** | `subsection-briefs`: 新增 `thesis` 字段，明确该节要论证什么 |
| 段落是"介绍"而非"论证" | `paragraph_plan.intent` 太宽泛（如 "Compare approaches"） | `subsection-briefs`: `intent` 改为 argument_role（introduce_tension / provide_evidence / counter_argument / synthesize） |

**`subsection-briefs/SKILL.md` 具体修改**:
```yaml
# subsection_briefs.jsonl 新增字段
{
  "sub_id": "3.1",
  "title": "Agent loop and action spaces",
  "thesis": "Action representation determines verifiability ceiling; structured > free-form for debugging but sacrifices flexibility",  # 新增
  "paragraph_plan": [
    {
      "para": 1,
      "argument_role": "introduce_tension",  # 新增：替代原来的 intent
      "content_focus": "Why action representation matters for verifiability"
    },
    {
      "para": 2,
      "argument_role": "provide_evidence",
      "content_focus": "Free-form (ReAct) creates debugging difficulty"
    },
    {
      "para": 3,
      "argument_role": "provide_evidence",
      "content_focus": "Structured (SCL) enables attribution"
    },
    {
      "para": 4,
      "argument_role": "counter_argument",
      "content_focus": "But structured loses flexibility"
    },
    {
      "para": 5,
      "argument_role": "synthesize",
      "content_focus": "Therefore choice depends on verifiability vs flexibility trade-off"
    }
  ]
}
```

#### 映射 4: 逻辑连接词不足 → `subsection-writer` + `quality_gate` 改进

| Badcase | 根因分析 | Skill 改进 |
|---------|----------|-----------|
| However/Therefore 太少 | writer 没有被要求使用这些词 | `subsection-writer`: 增加 **connector density** 最低要求 |
| 因果关系隐含而非显式 | 没有检查机制 | `quality_gate`: 新增 `sections_connector_density` 检查 |

**`subsection-writer/SKILL.md` 具体修改**:
```markdown
### Logical Connector Requirements (新增)

每节必须包含以下连接词的**最低数量**：

| 连接词类型 | 最低要求 | 示例 |
|-----------|---------|------|
| 因果 | ≥3 | Therefore, Thus, Hence, As a result, Consequently |
| 转折 | ≥2 | However, But, Yet, Nevertheless, In contrast |
| 递进 | ≥2 | Building on this, Following, Moreover, Furthermore |
| 提问 | ≥1 | This raises the question, This suggests that |

Self-check: 写完后统计连接词数量，不足则补充。
```

**`quality_gate.py` 新增检查**:
```python
def sections_connector_density(ws: Path) -> list[QualityIssue]:
    """检查逻辑连接词密度"""
    issues = []

    CAUSAL = r"\b(therefore|thus|hence|as a result|consequently)\b"
    CONTRAST = r"\b(however|but|yet|nevertheless|in contrast|unlike)\b"
    EXTENSION = r"\b(building on|following|moreover|furthermore)\b"

    for section_file in (ws / "sections").glob("S*.md"):
        text = section_file.read_text().lower()

        causal_count = len(re.findall(CAUSAL, text))
        contrast_count = len(re.findall(CONTRAST, text))
        extension_count = len(re.findall(EXTENSION, text))

        if causal_count < 3:
            issues.append(QualityIssue(
                f"{section_file.name}: causal connectors={causal_count}, need ≥3",
                severity="warning"
            ))
        if contrast_count < 2:
            issues.append(QualityIssue(
                f"{section_file.name}: contrast connectors={contrast_count}, need ≥2",
                severity="warning"
            ))

    return issues
```

#### 映射 5: 润色缺失 → Pipeline 新增 `section-logic-polisher` skill

| Badcase | 根因分析 | Skill 改进 |
|---------|----------|-----------|
| 写完即 merge，无逻辑检查 | Pipeline 中没有润色步骤 | 新增 `section-logic-polisher` skill，在 `section-merger` 之前运行 |
| global-reviewer 只检查术语 | Reviewer 的 scope 太窄 | `global-reviewer`: 增加 cross-section flow 检查 |

**新增 skill: `section-logic-polisher`**

```markdown
# .codex/skills/section-logic-polisher/SKILL.md

## Purpose
对已写完的 section 进行逻辑润色（不改内容，只加连接）。

## Input
- `sections/S*.md`: 待润色的章节
- `outline/subsection_briefs.jsonl`: 该节的 paragraph_plan

## Output
- `sections/S*.md`: 润色后的章节（原地更新）
- `sections/.polish_log/S*.polish.json`: 润色记录

## Workflow
1. **Thesis check**: 第一段最后一句是否是 thesis statement？
   - 如果不是，插入 "This subsection argues/shows that [thesis from briefs]."
2. **Flow check**: 每两段之间是否有 logical connector？
   - 如果缺少，在段首插入 connector phrase（参考 briefs 的 connector_to_prev）
3. **Connector density**: 统计连接词数量
   - 如果不足，在合适位置补充（优先在 claim 句之后）

## Constraints
- ❌ 不改变段落内容（只加连接句）
- ❌ 不添加新引用
- ❌ 不改变 clusters/scope
- ✅ 可以调整段落顺序（如果 flow 需要）
- ✅ 可以补充 thesis statement
- ✅ 可以插入 connector phrase
```

**Pipeline 修改**:
```yaml
# arxiv-survey-latex.pipeline.md Stage C5 修改

## C5 — Draft + PDF

Skills (顺序执行):
1. subsection-writer      # 写各节
2. section-logic-polisher # 新增：逻辑润色
3. transition-weaver      # 生成过渡
4. section-merger         # 合并
5. draft-polisher         # 去模板化
6. global-reviewer        # 全局审查
```

### 24.6 质量对比矩阵

| 维度 | citeboost | skillcontracts | 改进幅度 | 下一步改进 |
|------|-----------|----------------|----------|-----------|
| 引用嵌入 | 句末堆砌 | 系统名+引用 | **显著** | ✅ 已解决 |
| 对比句式 | 很少 | 每节 2-3 处 | **显著** | ✅ 已解决 |
| 数字锚点 | 偶尔 | 频繁且具体 | **显著** | ✅ 已解决 |
| 跨论文综合 | 无 | 每节结尾有 | **显著** | ⚠️ 需去模板化 |
| 局限具体性 | 泛泛 | 指向具体失败模式 | **中等** | ⚠️ 需去模板化 |
| **段落逻辑连接** | N/A | **弱** | N/A | 🔴 需改进 briefs + writer |
| **节内论证主线** | N/A | **缺失** | N/A | 🔴 需增加 thesis 要求 |
| **连接词密度** | N/A | **不足** | N/A | 🔴 需增加 quality gate |
| **润色机制** | 无 | 无 | 无变化 | 🔴 需新增 polisher skill |
| 完成度 | 100% | 37.5% | **退步** | 🔴 需修复 pipeline 稳定性 |

### 24.7 关键发现

**成功验证的契约补强**:

1. `anchor-sheet/SKILL.md` 的"锚点消费最小规则"生效 → 数字锚点使用率大幅提升
2. `writer-context-pack/SKILL.md` 的"must-use 清单"生效 → 对比和评测锚点不再被忽略
3. `subsection-writer/SKILL.md` 的"Citation embedding + Transitions"规则生效 → 引用嵌入方式正确

**新发现的写作逻辑问题**:

1. **段落逻辑连接弱**: paragraph_plan 只规定 topic，不规定 inter-paragraph connector
2. **节内论证主线缺失**: 没有 thesis statement，段落是"介绍"而非"论证"
3. **连接词密度不足**: However/Therefore 等因果连接词太少
4. **Synthesis 模板化**: 每节结尾都是 "Taken together... N clusters"
5. **润色机制缺失**: 写完即 merge，无逻辑检查步骤

**需要进一步加强的契约**:

1. **`subsection-briefs`**: 增加 thesis、argument_role、connector_to_prev 字段
2. **`subsection-writer`**: 增加 thesis statement 要求、connector density 要求
3. **`chapter-briefs`**: 增加 synthesis_mode 多样性要求
4. **`quality_gate`**: 增加 sections_connector_density 检查
5. **Pipeline**: 新增 `section-logic-polisher` skill

### 24.8 改进优先级更新

基于本次分析，调整优先级：

**P0（写作逻辑问题 - 新增）**:
- `subsection-briefs`: 增加 `thesis`、`argument_role`、`connector_to_prev` 字段
- `subsection-writer`: 增加 thesis statement 要求（第一段末尾）
- `quality_gate`: 新增 `sections_connector_density` 检查

**P0（Pipeline 稳定性）**:
- Pipeline 错误恢复机制（单个章节失败不应阻断全部）
- U100 script 错误日志完整化（记录具体失败原因）

**P1（写作质量细节）**:
- `chapter-briefs`: synthesis_mode 多样性要求
- 新增 `section-logic-polisher` skill
- `global-reviewer`: 增加 cross-section flow 检查

**降级为 P2**（已被契约补强解决）:
- 引用嵌入规则 → 已生效
- 数字锚点消费 → 已生效
- 对比句式要求 → 已生效

---

## 25) 总结与下一步

### 25.1 契约补强效果验证

本次 `e2e-agent-survey-skillcontracts` workspace 分析证明：
- **SKILL.md 的契约补强是有效的**：引用嵌入、数字锚点、对比句式等问题显著改善
- **写作问题的根因确实在 C2-C4**：当 brief/evidence/anchors 准备充分且有明确消费规则时，C5 的写作质量自然改善
- **"软约束"问题部分解决**：通过 must-use 清单和 writer contract，LLM 更倾向于遵守约束

### 25.2 新发现：写作逻辑问题

但本次分析也发现了**新的质量瓶颈**：

| 问题类型 | 表现 | 根因 |
|---------|------|------|
| 段落逻辑连接弱 | 每段像"孤岛" | paragraph_plan 只规定 topic，不规定 connector |
| 节内论证主线缺失 | 没有 thesis statement | subsection_briefs 没有 central_argument 字段 |
| 连接词密度不足 | However/Therefore 太少 | 没有最低数量要求 |
| Synthesis 模板化 | 每节都是 "Taken together... N clusters" | 没有 synthesis_mode 多样性规定 |
| 润色机制缺失 | 写完即 merge | Pipeline 没有 logic polishing 步骤 |

**核心洞察**：上一轮契约补强解决了**内容**问题（引用、锚点、对比），但没有解决**逻辑**问题（连接、论证、主线）。

### 25.3 残留风险

1. **Pipeline 稳定性**: 契约补强提高了质量但可能增加了脆性（更多检查 = 更多失败点）
2. **完成度**: 写得好但写不完，比写完但写不好更糟糕（因为无法交付）
3. **逻辑润色成本**: 新增 polisher 会增加 pipeline 时间，需要权衡

### 25.4 建议的下一步迭代

**Sprint 目标**: 解决写作逻辑问题，同时保持 Pipeline 稳定性

**具体任务**:

1. **修改 `subsection-briefs/SKILL.md`**:
   - 新增 `thesis` 字段（每节的核心论点）
   - `paragraph_plan` 新增 `argument_role`（introduce_tension / provide_evidence / counter_argument / synthesize）
   - `paragraph_plan` 新增 `connector_to_prev`（contrast / consequence / extension）

2. **修改 `subsection-writer/SKILL.md`**:
   - 增加 Thesis Statement Requirement（第一段末尾必须是 thesis statement）
   - 增加 Logical Connector Requirements（因果 ≥3，转折 ≥2，递进 ≥2）

3. **修改 `quality_gate.py`**:
   - 新增 `sections_connector_density` 检查
   - 新增 `sections_thesis_statement` 检查

4. **新增 `section-logic-polisher` skill**:
   - 在 `section-merger` 之前运行
   - 只做连接（加 connectors、补 thesis），不改内容

5. **修改 `chapter-briefs/SKILL.md`**:
   - 新增 `synthesis_mode` 字段（clusters / timeline / trade-off_matrix / case_study）
   - 避免每节都用同一种 synthesis 方式

---

*End of document*
