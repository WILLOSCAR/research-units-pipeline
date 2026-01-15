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

*End of document*
