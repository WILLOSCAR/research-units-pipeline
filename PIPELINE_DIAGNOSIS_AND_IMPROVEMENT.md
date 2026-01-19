# Pipeline Diagnosis & Improvement (skills-first LaTeX survey)

Last updated: 2026-01-19

本诊断聚焦：**skills 驱动的 LaTeX survey 生成 Pipeline**（不是某次草稿内容打磨）。

- Pipeline 定义：`pipelines/arxiv-survey-latex.pipeline.md`
- 对标材料（风格/结构基准）：`ref/agent-surveys/`（尤其 `ref/agent-surveys/STYLE_REPORT.md` + `ref/agent-surveys/text/`）
- 实证 workspace（用作回归基线，不是交付物）：`workspaces/e2e-agent-survey-latex-verify-20260118-182656/`

核心目标（你要的“会带人/带模型做事”）：
- 语义化：skill 的命名/描述/合同足够清晰、可组合、可解释（像 Anthropic skills 那样“读 SKILL.md 就知道怎么做且不会跑偏”）。
- 可审计：任何一次 run 的过程与失败原因都能从 workspace 里读出来（无需重跑）。
- 写作不空洞：不是靠硬 gate 堵住，而是通过 **中间态合同**（brief/evidence/pack/transition）把 writer 引导到“论文写法”。

---

## 0b) Current status (implemented vs remaining)

Implemented (2026-01-19):
- Contract closure: report-class skills always write outputs; `artifact-contract-auditor` writes `output/CONTRACT_REPORT.md`.
- Failure sinks: `output/QUALITY_GATE.md` is append-only; runner appends `output/RUN_ERRORS.md`.
- Paper voice guardrails (non-hardcode first): transition outputs are paper-voice (no planner talk), writer packs include a positive `paper_voice_palette`.
- Writing-stage playbooks: key C5 skills now encode explicit argument-move contracts + rewrite recipes + good/bad examples (so quality is guided before/during drafting, not only audited after).
- Schema normalization (P2-2): `schema-normalizer` makes C3/C4 JSONL join keys + citation formats consistent, writing `output/SCHEMA_NORMALIZATION_REPORT.md`.
- Two self-loops are now explicit in the pipeline:
  - Evidence self-loop (prewrite routing): `evidence-selfloop` → `output/EVIDENCE_SELFLOOP_TODO.md` (blocks on `blocking_missing`).
  - Writing self-loop: `writer-selfloop` → `output/WRITER_SELFLOOP_TODO.md` (blocks until PASS; fix only failing `sections/*.md`).
- Visuals default strategy: optional by default (tables/timeline/figures skills remain available but are not required for arxiv-survey(-latex)).

Remaining: optional visuals insertion into LaTeX if you want closed-loop figures/tables (make visuals a first-class deliverable instead of intermediate-only).

## 0) 对标：成熟 survey 的“外形”和“写法”是什么

基于 `ref/agent-surveys/STYLE_REPORT.md`（11 篇 agent survey 的 best-effort 统计）和 `ref/agent-surveys/text/*.txt` 的结构观察：

### 0.1 结构外形（paper-like）

- 顶层章节（H2/Section）数量：min/median/max = 3/6/10
- 常见章节骨架（不要求完全一致，但“气质”一致）：
  - Introduction
  - Related Work / Related Surveys（有些会有）
  - Methodology / Survey methodology（不少 survey 会明确写“怎么收集/筛选/分类”）
  - Taxonomy / Techniques / Capabilities（通常 2–4 个核心章，少而厚）
  - Evaluation / Benchmarks
  - Challenges / Future Directions / Risks
  - Conclusion

结论：成熟 survey 很少把“章节数量堆满”；更常见的是 **少而厚** + **每章内部有明确对比轴**。

### 0.2 论证写法（段落结构）

成熟 survey 的段落通常隐含一个稳定的“论证骨架”（不是模板句，而是信息组织方式）：

- 张力/问题（为什么这件事难、难在哪里）
- 典型路线对比（A vs B 的机制差异，不是“列论文”）
- 评测锚点（benchmark/protocol/metric/budget/tool availability，至少交代其中 2–3 个）
- 局限与可迁移性（“结论在什么条件下成立”）

### 0.3 语言风格（paper voice）

- 少“旁白导航”：不写“Now we move to … / This subsection surveys …”，而写“内容论证句”。
- 少“生产线口吻”：不会出现“this run / pipeline / stage”这样的词；方法学声明会像论文 Method note。
- 引用更“嵌入”：引用跟着主张走，不在段尾“甩一串 cite dump”。

对 pipeline 的启示：
- 你要解决的不是“段落数/字数不够”，而是 **中间态没有把 writer 限定在上述骨架里**，导致写出来像“合理但空”的自动化综述。

---

## 1) 实证对齐：当前 workspace vs 成熟 survey 的差距（先看产物外形）

基于 `workspaces/e2e-agent-survey-latex-verify-20260118-182656/` 的可观测信息：

### 1.1 结构/覆盖（总体不差，但细节会放大缺陷）

- Draft 顶层 H2（含 Abstract）：9（Abstract/Intro/Related + 4 核心章 + Discussion + Conclusion）
  - 排除 Abstract 后为 8，落在对标 survey 的常见范围内。
- H3 数：8（每个核心章 2 个 H3）
  - 对 `draft_profile: lite` 来说，这个“少而厚”是正确方向。
- 引用：
  - `output/AUDIT_REPORT.md`：unique cites=101；`citations/ref.bib` entries=220
  - 引用规模不算少，问题更多在“引用如何服务论证”。

### 1.2 写作观感差距（主要来自“中间态泄漏”和“元指导口吻”）

从 `output/AUDIT_REPORT.md` 的非阻断告警可见：
- “Taken together, …” 6×（综合开头重复）
- “survey … should …” 4×（元指导口吻）
- “this run” 1×（pipeline voice 进入正文）

更致命的是：**transition 产物本身像“规划注释”**，被 merge 后直接进入正文：

- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/outline/transitions.md` 的 Within-section / Section openers 里，出现大量：
  - `After X, Y makes the bridge explicit via ...; ...; ...`
  - `Y follows naturally by turning X’s framing into ... anchored evaluation questions.`

这些句子在最终稿中可定位为：
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/output/DRAFT.md:59`
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/output/DRAFT.md:111`
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/output/DRAFT.md:165`
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/output/DRAFT.md:221`

这类“规划注释句”会让读者第一眼判断“自动生成”。

### 1.3 可复用性/可审计性差距（这是 pipeline 层面 P0）

pipeline 声称的 `target_artifacts`（`arxiv-survey-latex` 当前 40 个）在 baseline workspace 缺失 2 个关键 QA 报告：
- 缺失 `output/SECTION_LOGIC_REPORT.md`
- 缺失 `output/GLOBAL_REVIEW.md`

这不是“内容问题”，而是 **Units 合同失效**：
- pipeline/units 把它们当作必产物，但 run 结果没有。
- 这会直接削弱“自循环”：你想定位写作问题时，最关键的 QA 证据没落盘。

另一个审计性 canary：
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/DECISIONS.md` 的 C0 kickoff block 中 workspace 路径是旧的（与当前 workspace 名不一致）。
  - 这意味着 checkpoint scaffolding 不完全可信，会影响后续 HITL 审批与复现。

---

## 2) 共性核心问题（Root causes）— 为什么这类 pipeline 容易“写得空 / 不像论文”

下面每条都包含：症状 → 根因 → 有问题的中间态 → 如何被放大/掩盖 → 改进建议（含收益/风险/验证）。

### RC1) 执行合同不闭环：DONE ≠ 产物存在（可审计性崩塌）

症状（可证）：
- baseline workspace 缺 `output/SECTION_LOGIC_REPORT.md`、`output/GLOBAL_REVIEW.md`。

根因（设计）：
- pipeline/units 把“报告”当必产物，但执行链路没有强制“产物落盘”。
- 一旦报告缺失，后续只能靠主观读稿，无法稳定自循环。

中间态问题：
- QA 报告类 artifact（logic/global review）没有被当作“交付合同的一等公民”。

放大/掩盖方式：
- 写作质量问题会被掩盖为“感觉不对”，而不是可定位问题（哪一小节缺 thesis？哪一类重复口吻？）。

改进建议（P0，偏合同/流程，不依赖硬编码风格 gate）：
- 把“报告类技能”的 SKILL.md 合同写死：
  - “无论 PASS/FAIL 都必须写出 report 文件；PASS 也要写（便于回归）。”
- 引入一个 **artifact contract auditor**（可以是新 skill，也可以合并进 pipeline-auditor）：
  - 输入：PIPELINE.lock + pipeline target_artifacts
  - 输出：`output/CONTRACT_REPORT.md`（列缺失项；PASS/FAIL）

预期收益：
- 每个 workspace 都能独立作为回归样本；自循环有据可依。

潜在风险：
- 更严格会让一些“以前看似跑通”的 run 变成 FAIL（但这是好事：暴露合同问题）。

验证：
- 任意一次 e2e 结束后：40/40 `target_artifacts` 存在；缺失会被 `CONTRACT_REPORT` 明确列出。

---

### RC2) 失败信息不落盘：BLOCKED 只能靠重跑（自举能力弱）

症状（可证）：
- `STATUS.md` 里出现 `BLOCKED (script failed)` / `BLOCKED (quality gate: output/QUALITY_GATE.md)` 记录。
- 但 baseline workspace 的 `output/` 下并不存在 `output/QUALITY_GATE.md` 或一个集中错误日志（无法回放失败上下文）。

根因（协作链路）：
- pipeline 缺少统一的“失败沉淀”机制：stderr/trace 没写入 workspace。

中间态问题：
- 缺少标准错误 sink：`output/RUN_ERRORS.md` / `output/QUALITY_GATE.md`。

放大/掩盖方式：
- 同样的问题每次都要靠重跑触发，成本高，且容易在不同环境下表现不同（“偶发”）。

改进建议（P0）：
- 为所有 pipeline 定义两类标准失败沉淀：
  - `output/QUALITY_GATE.md`：append-only，记录 gate code + 路由建议（回到 C2/C3/C4/C5 哪个 skill）。
  - `output/RUN_ERRORS.md`：append-only，记录 unit_id + timestamp + 关键 stderr 摘要。

验证：
- 故意制造一个失败（例如删 input），run 结束后 workspace 必然包含上述两个文件，且可定位到具体 unit。

---

### RC3) “NO PROSE”边界不清，规划语言泄漏到正文（最影响论文感）

症状（可证）：
- `outline/transitions.md` 写的不是“论证桥”，而是“构建注释”（分号列表、turning framing into…）。
- merge 后直接进入 `output/DRAFT.md`。

根因（语义表达 + 引导能力）：
- 多个技能标注 NO PROSE，但没有形式化定义“禁止什么”。
- transition-weaver 的产物位于 C5 前的 NO NEW FACTS 区域，**更容易被当作“模板可直接用”**，从而泄漏。

中间态问题（明确指出）：
- `outline/transitions.md` 本身不合格：内容是“planner talk”，不是“paper voice”。

放大机制：
- `section-merger` 会把 transitions 当“可直接注入正文的句子”，因此任何 planner talk 会被放大为全篇的 generator voice。

改进建议（P0，优先改 skill 合同与默认写法）：
- 形式化“NO PROSE / NO NEW FACTS”的语义边界（写进 `SKILLS_STANDARD.md`，并被 NO PROSE skills 引用）：
  - 允许：短语、短句、bullets、字段化 JSONL
  - 禁止：分号列举式“构建说明”、章节导航旁白、“turning X into Y”这种结构化注释
- transition-weaver 必须输出“内容论证句”（1 句即可）：
  - 只写：上一节结论/局限 → 下一节为什么重要
  - 不写：工具链路/构建过程/“setting up a cleaner A-vs-B comparison”

验证：
- `outline/transitions.md` 中不再出现：
  - `After .* makes the bridge explicit via`
  - `follows naturally by turning .* framing into`
  - `;` 形式的枚举规划句
- 这些模式在 `output/DRAFT.md` 中为 0。

---

### RC4) briefs 的 thesis/contrast 太泛，writer 容易写成“正确但空”的综述

症状（可证，抽样）：
- `outline/subsection_briefs.jsonl`（以 3.1 为例）的 thesis：
  - “... highlights a tension around mechanism / architecture and data / training setup ...”
- `contrast_hook`：`evaluation`（过泛）

根因（C3 语义合同弱）：
- thesis/contrast 没有落到“具体张力”（例如“表达能力 vs 可验证性”“free-form vs schema-constrained”等）。
- paragraph_plan 的 connector_phrase 是完整句，容易被 writer 复用成重复口吻。

中间态问题：
- `subsection_briefs.jsonl` 的字段足够多，但“信息密度不够”（具体张力与评价锚点不够具象）。

放大机制：
- writer 写作时，为了填满段落，会自然落到 meta-guidance 句式（Taken together / survey should）而不是“具体对比”。

改进建议（P1，语义化增强，不靠硬 gate）：
- 扩展 subsection-briefs 的合同：
  - `tension_statement`（必须是具体张力句，不是泛轴名）
  - `evaluation_anchor_minimal`（每节至少 1 个：task + metric + constraint 的三元组；abstract-first 可允许“部分未知”但要标 unknown slot）
  - `anti_voice_rules`（避免写“survey should”，鼓励写“we observe ... under protocol ...”）
- connector_phrase 改成“短语级提示”（clause-level），禁止成句，以减少 copy-paste。

验证：
- brief 里每个 H3 的 tension_statement 可直接作为段落 1 的核心句（无需模板词）。
- draft 中 “survey should” 下降到 <=1。

---

### RC5) evidence-binder 过于均匀/机械，容易掩盖“证据结构差异”

症状（可证）：
- `outline/evidence_binding_report.md` 显示每个 H3 都是同样的 mix：`limitation=1, method=1, result=10`，且 evidence_level 全是 abstract。

根因（C4 规划不够“差异化”）：
- binder 像在填一个固定配方，而不是根据 subsection 的 `required_evidence_fields` / `axes` 去挑“更像这节的证据”。

中间态问题：
- `outline/evidence_bindings.jsonl` 的选择策略过“规则化”，缺少 subsection-specific 的解释与缺口标注。

放大/掩盖方式：
- writer 拿到的 evidence_ids 看似齐全，但可能不够“贴题”。写出来就会变成泛泛对比。

改进建议（P1）：
- binder 输出要带两个字段：
  - `binding_rationale`：为什么这些证据匹配本节 axes（短 bullet，不是 prose）
  - `binding_gaps`：哪些 required_evidence_fields 没覆盖（用于回退到 C3 paper-notes 或 C1 扩文献）

验证：
- binding report 不再每节完全同构；能看到不同小节的 evidence_type/anchors 分布差异。

---

### RC6) writer-context-pack 已经是“上帝对象”，但仍缺少“正向写法引导”

症状（可证）：
- pack 里已有 `do_not_repeat_phrases` / `opener_hint` / `must_use`。
- 但最终 draft 仍出现：Taken together（6×）、survey should（4×）、以及 transitions 的 planner talk。

根因（引导能力）：
- “禁止什么”写得不错，但“该怎么写得像论文”还不够具体（缺少正向 palette/例句）。

中间态问题：
- `writer_context_packs.jsonl` 里缺少“替代表达库”和“微结构模板（非套话）”。

放大机制：
- writer 会用最省力的学术口吻填充（Taken together / therefore survey should），形成 generator voice。

改进建议（P1）：
- 在 writer-context-pack 中加入 `paper_voice_palette`（结构化字段，不是长 prose）：
  - opener archetypes（decision-first / tension-first / evidence-first）各 2–3 个例句
  - synthesis sentence alternatives（替代 Taken together）
  - rewrite rules：把 “survey should …” 变成 “Across protocols, we observe …” 的映射

验证：
- audit report 的 phrase family 复发明显下降。

---

### RC7) 视觉/表格类中间态产出未进入最终 LaTeX（工作流不闭环）

症状（可证）：
- workspace 有 `outline/tables.md`、`outline/timeline.md`、`outline/figures.md`。
- 但 `latex/main.tex` 不包含这些内容（LaTeX 输出只来自 `output/DRAFT.md`）。

根因（设计合理性）：
- pipeline 把 visuals 作为必做（C4 required），但没有“注入到正文/LaTeX”的后续动作。

中间态问题：
- 这些中间态变成“孤岛产物”，既不影响 draft，也不影响 PDF。

放大/掩盖方式：
- 你会感觉 pipeline 做了很多，但最终交付（PDF）没有体现，导致“流程看起来强但产出不强”。

改进建议（P2，两种路线二选一，需产品决策）：

Current repo default (2026-01-19): choose route (1) optional — visuals skills remain available, but they are not required/contracted in the default arxiv-survey(-latex) run.

1) 简化路线：把 `table-schema/table-filler/survey-visuals` 改为 optional（默认不跑）。
2) 闭环路线：新增 `visuals-inserter`（C5）：
   - 把 tables/timeline/figure specs 以“论文可接受”的方式插入 DRAFT（或 LaTeX），并保持 citations 不引入新 key。

验证：
- 如果走闭环路线：PDF 中至少包含 1–2 张表（或 timeline figure placeholder），且引用可编译。

---

### RC8) schema/字段命名缺少统一规范，导致手工 heuristics 变多

症状（可证）：
- `subsection_briefs.jsonl` 有 `section_id`，`evidence_drafts.jsonl` 没有。
- evidence snippets 使用 `citations: ["@Key"]`（带 @），而 Markdown 正文是 `[@Key]`。

根因（语义表达）：
- 没有一个“统一 schema 规范”作为技能间的接口合同。

中间态问题：
- 下游脚本/skill 只能 best-effort 解析，长期会积累 drift 与隐式兼容逻辑。

改进建议（P2）：
- 在 `SKILLS_STANDARD.md` 增加一个小节：
  - JSONL interface schema（必填字段：sub_id/section_id/title/schema_version；citations 统一用 bibkey，不带 @）
- 可选：增加 `schema-normalizer` skill（NO PROSE，deterministic）：
  - 统一字段/引用格式，降低后续技能复杂度。

验证：
- briefs → evidence packs → writer packs 可以无 heuristics join。

---

## 3) Pipeline 分阶段诊断（逐步定位“中间态哪里坏了，怎么被放大”）

下面按 C0–C5 列出：该阶段目标、现状问题、典型放大路径、改进点（技能层）。

### C0 — Init（workspace + 决策路由）

现状问题（baseline 证据）：
- `DECISIONS.md` 的 C0 block workspace 路径与当前 workspace 名不一致（审计性问题）。

放大路径：
- HITL 审批变得不可信（签字页不知道对应哪个 run）。

改进点：
- pipeline-router 的 checkpoint block 必须“每次刷新 workspace/pipeline 信息”，避免 stale。
- checkpoint block 增加一个 self-check 行：当前文件所在目录名（让 drift 可见）。

### C1 — Retrieval & core set（文献池）

现状：
- core_set 与 bib entries 规模足够（bib=220）；不是当前瓶颈。

潜在共性风险（与写作空洞相关）：
- 如果 evidence_mode=abstract，很多定量细节只能写成“泛比较”，容易触发 disclaimer/元指导口吻。

改进点（偏语义引导）：
- 在 queries.md/briefs 中把“abstract-first 的限制”收敛成 **单段 method note**（而不是让 writer 在每节重复）。

### C2 — Structure（NO PROSE + 人工确认）

现状：
- 结构形态已接近对标（8 个 H3，4 个核心章，Intro/Related/Discussion/Conclusion 具备）。

共性风险：
- 大纲 bullets 的“比较轴”仍偏通用（mechanism/data/eval/efficiency/limitations），如果 C3 不能把它落到具体张力，会在 C5 变空。

改进点：
- C2 输出增加“章节预算/粒度”解释（为什么只有这 8 个 H3，避免未来回退到 H3 爆炸）。
- 让 outline-refiner 的 coverage report 更有用：至少报告每个 H3 的“可写性提示”（例如：是否包含 evaluation anchors bullets）。

### C3 — Evidence pack（NO PROSE）

现状问题（抽样）：
- thesis/contrast_hook 仍偏泛；connector_phrase 是完整句（容易模板化）。

放大路径：
- writer 为了填充段落会使用 meta synthesis 句式（Taken together / survey should）。

改进点：
- subsection-briefs：强制输出 `tension_statement` + `evaluation_anchor_minimal`（三元组）。
- chapter-briefs：把 H2 lead 的写法变成“比较轴预告”，避免 generic glue。

### C4 — Citations + visuals（NO PROSE）

现状问题：
- evidence binding mix 过于同构（每节 10 result + 1 method + 1 limitation）。
- visuals 产物未闭环进入 LaTeX。
- schema 有 drift（section_id 缺失、citations 表达不一）。

放大路径：
- binder 同构会掩盖“证据贴题性不足”；writer 写出来就泛。
- visuals 不进入正文会让“投入感”和“交付感”断裂。

改进点：
- evidence-binder：输出 rationale + gaps。
- 明确 visuals 的产品策略：optional 还是闭环注入。
- schema 标准化（字段/引用格式）。

### C5 — Draft + PDF（PROSE）

现状问题（baseline 证据）：
- transition-weaver 的 `outline/transitions.md` 直接把 planner talk 注入正文（最伤论文感）。
- QA 报告文件缺失（SECTION_LOGIC / GLOBAL_REVIEW），削弱自循环。
- 仍存在 meta synthesis / survey-guidance 句式重复。

放大路径：
- transitions 是“全篇高频出现的句子类型”，一旦坏了，整篇就像自动生成。

改进点（语义化优先）：
- transition-weaver：默认模板必须 paper voice；避免分号注释句。
- subsection-writer：明确“不要在正文里写 survey 该怎么写”，把 meta guidance 改写为内容主张。
- 增加 paper-voice palette（正向引导），让 writer 不用靠 Taken together。

---

## 4) 评价（尖锐但公平）

### 优点（值得保留）

- 结构已经回到“少而厚”的正确区间：8 个 H3、4 个核心章，符合对标 survey 的常见 ToC 形态。
- evidence-first 的产物链齐全：notes → evidence_bank → bindings → evidence_drafts → anchor_sheet → context_packs。
- citation 规模不低：bib=220，draft unique=101；这为写作“做实”提供了材料基础。

### 关键短板（会被 reviewer 第一眼抓住）

- transition 中间态像“构建注释”，并且被 merge 直接注入正文（这是最明显的自动化痕迹）。
- Units 合同未闭环：关键 QA 报告缺失，导致流程不可审计、不可回归。
- writer 的“正向写法引导”不足：有禁令（do_not_repeat）但缺少替代句式/微结构，导致模型回到 Taken together / survey should 的省力口吻。

---

## 5) 改进路线图（可落地、可验证）

### P0（必须先做：让 pipeline 可信 + 不再明显像自动生成）

1) 合同闭环：保证 report 类产物必落盘
- 目标：补齐 `output/SECTION_LOGIC_REPORT.md`、`output/GLOBAL_REVIEW.md`（以及未来任何 report 类文件）。

2) 失败沉淀：标准化 error sink
- 目标：失败无需重跑即可定位（`output/QUALITY_GATE.md` / `output/RUN_ERRORS.md`）。

3) transition-weaver 去 planner talk
- 目标：`outline/transitions.md` 不再包含分号注释句；DRAFT 不再出现 4 处 meta transition。

4) DECISIONS 工作区绑定修复
- 目标：checkpoint blocks 永远显示正确 workspace path。

### P1（提升 paper voice：减少“合理但空”的口吻）

1) subsection-briefs 增强：tension_statement + evaluation_anchor_minimal
2) writer-context-pack 增强：paper_voice_palette（替代句式库）
3) 把 “survey should …” 改写成“内容主张句”的显式规则（写在 skills 合同里）

### P2（结构性重构：减少无效劳动 + 降低 drift）

1) visuals：要么 optional，要么闭环注入（新增 visuals-inserter）
2) schema：统一 JSONL 字段与 citations 表达（可选 schema-normalizer skill）
3) 降低 god objects：明确 writer-context-pack / draft-polisher 的职责边界

---

## 6) 验证标准（每次跑完都能客观判断“有没有进步”）

建议把下面作为回归 checklist（不要求一次性全部 blocking，但至少要能报告出来）：

### 6.1 合同/审计（P0）
- target_artifacts 完整：40/40（或明确哪些是 optional）
- `DECISIONS.md` workspace path 正确且可追溯
- 任意失败都有 `output/QUALITY_GATE.md` / `output/RUN_ERRORS.md`

### 6.2 写作风格（paper voice，先 warning 后逐步严格）
- meta transition leakage：0
- `Taken together,`：<=2（或至少不集中重复）
- `survey ... should ...`：<=1
- `this run / pipeline` 类词：0（替换成论文式 method note）

### 6.3 论证密度（避免“长但空”）
- 每个 H3 至少包含：
  - >=2 个 A-vs-B contrasts（同段多 cite）
  - >=1 个 protocol-aware 段落（task/metric/constraint 至少 2 项）
  - >=1 个 limitation 段落（明确条件/边界）
