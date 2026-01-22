# Pipeline Diagnosis & Improvement (skills-first LaTeX survey)

Last updated: 2026-01-22

本文件只诊断 **pipeline + skills 的结构设计**（不做“某次草稿的内容打磨”）。

定位锚点（用于复现/对标；不改 workspace 产物）：
- Pipeline spec：`pipelines/arxiv-survey-latex.pipeline.md`（当前 v3.0）
- 对标材料：`ref/agent-surveys/`（尤其 `ref/agent-surveys/STYLE_REPORT.md`）
- 最新基线 workspace：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/`
- 回归基线 workspace：`workspaces/_refs/baselines/e2e-agent-survey-latex-verify-20260119-120720/`

目标（你要的“会带人 / 会带模型做事”）：
- 语义化：skill 的职责边界清晰、可组合、可解释（读 `SKILL.md` 就知道“要做什么 / 禁止什么 / 怎么判断完成”）。
- 可审计：每次 run 的关键决策、失败原因、回退路径都能在 workspace 中回放（不用重跑才能知道哪里坏了）。
- 写作像论文：不是靠“最后一刻硬 gate 堵住”，而是靠 **中间态合同**（brief/evidence/binding/transition/front matter）让 writer 在落笔之前就被引导到论文式论证动作。

---

## 0) 上一版内容 Summary（change log 视角；作为新起点）

上一版（2026-01-21）已经把问题收敛到“写作不是最后一关，而是中间态合同的自然结果”，并形成了三条可复用结论：

1) 对标标尺被明确化
- 基于 `ref/agent-surveys/STYLE_REPORT.md` 固化“成熟 survey 的外形”：H2 通常 ~6–8、H3 少而厚、front matter 引用密度更高。
- 把“论文感”拆成可执行的论证动作：张力 → 对比 → 评测锚点 → 局限/边界，而不是模板句与目录旁白。

2) root causes 被“从终稿倒推”方式钉住
- gate 边界错位：只看 `sections/*.md` 会漏掉 `outline/transitions.md` 这种高频注入源。
- schema-valid ≠ writeable：C3/C4 产物即使 JSONL 合法，也可能语义同构/偏泛，导致 writer 只能写“正确但空”。
- front matter 如果不是“一等合同”，方法学/范围边界会在正文里变成重复免责声明与旁白。
- numeric claims 需要“最小协议上下文”（task/metric/constraint），否则 reviewer 会用 “underspecified” 直接打穿。

3) 两条 self-loop 被提升为结构中心
- evidence-selfloop：写作前的 prewrite routing（证据不可写时禁止用 prose 填洞）。
- writer-selfloop：只重写失败的 `sections/*.md`，并把“证据薄导致的失败”路由回 evidence loop。
- refined markers：把“已精炼”显式化为可审计信号，避免 scaffold 静默流入写作。
- post-merge voice gate：把 merge 后终稿作为 gate 边界，专门拦截“注入源口吻”。

---

## 1) 最新基线 run 的结果校验：哪些问题确实被修掉了（对标上一版的 root causes）

基线：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md`。

已经显著改善（与 20260119 对比）：
- front matter “方法学底座”落到论文正文且只出现一次：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:17`（candidate pool / dedupe / core set / evidence policy）。
- 终稿不再出现高信号 planner-talk transitions（post-merge voice PASS）：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/POST_MERGE_VOICE_REPORT.md:8`。
- “This subsection… / Next, we move…” 等目录旁白式模板句消失（全稿检索无命中）。
- 结构预算更接近成熟 survey：H3=8（少而厚）：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/AUDIT_REPORT.md:9`。
- PDF 交付尺寸基本对齐 survey 体量（页数 22）：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/LATEX_BUILD_REPORT.md:8`。

这说明：上一版提出的“front matter 一等合同 + post-merge gate + 结构预算”方向是有效的（至少能把“第一眼自动化信号”压下去）。

---

## 2) 从终稿倒推：最新 draft 仍然存在的可见问题清单（严格体检）

### 2.1 高信号“生成器口吻”仍然残留（不是硬模板，但会累积成风格噪音）

1) “Two limitations …” 在所有 H3 中重复出现（同一段落位置、同一语气）
- 终稿证据（只列部分）：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:55`、`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:197`
- 源头证据（per-section 文件一致复现）：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/sections/S3_1.md:11`、`workspaces/e2e-agent-survey-latex-verify-20260122-094516/sections/S6_1.md:11`
- 为什么是问题：读者会把它识别为“固定槽位的句式”，即使内容是真的，也会降低论文感与作者可信度。

2) “The key point is that …” 多次复用，且用于相同修辞功能（收束句）
- 证据：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:65`、`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:209`
- 影响：比模板句弱，但仍属于“discourse stem 单一化”的信号。

### 2.2 与成熟 survey 的结构性差距：缺少“可复用结构产物”（不是“写多点”能补齐）

1) 关键表格/结构化视觉产物缺失（taxonomy/evaluation/protocol 表）
- 证据：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/GLOBAL_REVIEW.md:12`（tables/timeline/figures=0）
- 对标含义：对标 survey 往往至少有 1–2 个“读者可复用”的表格；缺表会让稿子更像“长文综述”而不是“survey paper”。

2) methodology 仍然偏“一段 evidence policy”，缺少更强的可复现结构（可选，但能显著拉近对标）
- 对标参考：`ref/agent-surveys/text/2508.17281.txt:33` 起的 survey 常见做法是把 methodology 拆成 RQ / search / selection / dataset accounting。
- 当前 draft 已有“候选池/核心集合/证据模式”，但缺少“筛选规则 / RQ 列表 / benchmark accounting”这类结构锚点。

### 2.3 证据/引用层面的差距：bibliography 大，但正文消费偏少

1) 220 条 BibTeX 只消费了 76 个 unique keys（lite profile 虽 PASS，但与 survey 期待仍有差距）
- 证据：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/AUDIT_REPORT.md:8`
- 风险：读者会感觉“文献池很大，但正文证据链仍偏稀”，尤其是 Related Work / Intro 预期引用更密集。
- 直接原因：该基线用的是 `draft_profile: lite`（用于“跑通链路”验证），会把 global unique-citation 目标显著下调，从而让 `citation-diversifier`/`citation-injector` 可能不触发增密动作；要交付 citation-rich survey，应使用 `draft_profile: survey`（survey profile 的全局 unique-cite 门槛建议 >=110）。

2) per-H3 citation scope 合规率 100%（好），但也暗示“绑定集合偏窄”导致可用 citations 没被写作阶段消费
- 证据：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/AUDIT_REPORT.md:15`
- 解释：scope contract 成功了，但“可写性/证据密度”仍需通过 binder/packs/citation budget 继续拉高。

### 2.4 可审计性/可回放性还不够稳定（会影响“别人拿来复现你的 pipeline”）

1) `output/QUALITY_GATE.md` 作为 append-only sink 的语义不稳定：文件尾仍停留在 FAIL，但 pipeline 实际已完成
- 证据：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/QUALITY_GATE.md:410`（transitions_too_short FAIL），但当前 `workspaces/e2e-agent-survey-latex-verify-20260122-094516/outline/transitions.md:1` 已满足更高质量。
- 后果：读者/贡献者会误判流程“卡死”，削弱 auditability。

---

## 3) 终稿问题 ↔ 中间态证据 ↔ skill 产出：因果链（从终稿倒推到最早责任点）

| 终稿症状 | 终稿证据 | 最早责任中间态 | 对应 skill（最小修复点） | 传播路径（如何被放大/掩盖） |
|---|---|---|---|---|
| “Two limitations …” 固定句式反复出现 | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:55` | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/sections/S*.md` | `subsection-writer`（Style Harmonizer contract）+ `writer-selfloop`（style-smell 输出） | per-section gate 只检查“有没有 limitation”，不检查“limitation 语气是否模板化”→ PASS 后被 merge 固化 |
| discourse stem 单一化（key point 复用） | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:65` | `sections/S*.md` | `subsection-writer`（opener/closer palette） | writer 角色已存在，但缺少“跨小节的多样性约束”，导致每节都独立地“写得合理但像同一人机模板” |
| 视觉产物缺失（表/时间线/图规格） | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/GLOBAL_REVIEW.md:27` | `outline/table_schema.md` / `outline/tables.md` 等不存在 | `table-schema`/`table-filler`/`survey-visuals`（从 optional 升级为 profile-aware 合同） | pipeline 里视觉技能是 optional → 产物不生成 → writer/LaTeX 阶段没有可插入对象 → survey “可复用性”不足 |
| bibliography 大但正文消费少 | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/AUDIT_REPORT.md:8` | `outline/evidence_bindings.jsonl` + writer packs 的 allowed sets 偏窄 | `evidence-binder`（更宽的 mapped/selected 策略）+ `citation-diversifier`（更高 profile 目标） | scope 合规做得很对，但 budget 目标在 lite 下偏低 → 最终 draft PASS 但“像轻量综述” |
| C3 briefs 语义仍有 scaffold 痕迹（axes 被逗号切碎、条目以 and 开头） | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/outline/subsection_briefs.jsonl:1` | `outline/subsection_briefs.jsonl` | `subsection-briefs`（axes contract）+ `schema-normalizer`（smell 报告） | briefs 是 writer 的上游语义底座；这类小瑕疵不一定泄露到正文，但会增加漂移与模板化倾向 |
| QUALITY_GATE sink 不可回放 | `workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/QUALITY_GATE.md:410` | gate sink 没记录“后续已通过”的状态变化 | 各 skill 的“审计写法合同” | FAIL 能落盘，但缺少“闭环写回”（PASS 回写/链接到最终 report）→ auditability 断链 |

---

## 4) 共性 root causes（新的、且会持续影响写作质量的结构缺陷）

RC-1 “硬 gate 能拦住坏输出，但拦不住风格同质化”
- 当前 gate 很擅长拦模板句/旁白/占位符，但对“跨章节的修辞重复”几乎无感。
- 结果是：每个 H3 单看都像论文，但连起来读会出现“同一个句式槽位反复出现”的生成器信号。

RC-2 “optional structural artifacts” 导致 survey 的可复用性缺口长期存在
- 表格/时间线/图规格如果一直 optional，系统会倾向于用 prose 代替结构产物，但对标 survey 的差距正是这些“可复用结构件”。

RC-3 refined markers 目前更像“checkbox”，而不是“语义精炼的完成证明”
- 当 `*.refined.ok` 只是人工触发信号、缺少最小可验证质量点时，很容易出现“标记 refined 但 substrate 仍有 scaffold 痕迹”的情况。

RC-4 审计链条断在“失败之后”
- FAIL 能落盘，但 PASS 的最终状态未回写到统一 sink，会让协作者难以回放一次 run 的真实收敛过程。

---

## 5) 改造建议（只谈结构与合同：改哪里、为什么、收益/风险、怎么验证）

### 5.1 进一步强化两条 self-loop（把“修错”前移、把“风格漂移”可见化）

Evidence self-loop（C4）新增“可写性坏味道”维度（即使 blocking_missing=0 也要提示）：
- axes/briefs 结构坏味道：逗号切碎、以 and 开头、scope_rule 过泛 -> 路由 `subsection-briefs` 的精炼动作（而不是让 writer 自己吞）。
- packs 缺“评测锚点句”的最小字段（task/metric/constraint）-> 路由 `paper-notes`/`evidence-draft` 补齐 verify_fields。
- binder 过窄导致引用池未被消费 -> 路由 `evidence-binder`（扩大 mapped/selected 的宽度）或提高 citation budget profile。

状态（已落地到 repo 设计）：
- `evidence-selfloop` 脚本在 PASS 时也会输出 “writability smells (non-blocking)”（comparisons/eval/anchors/limitations/snippets 的低信号提示），把“schema-valid 但不可写”的风险前置显式化。

Writer self-loop（C5）在 PASS 时也输出 “Style Smell Appendix”（不一定 BLOCK，但要可见、可路由）：
- discourse stems 高频重复（例如 “Two limitations …” 跨 8 个 H3 重复）：提示 `Style Harmonizer` 只做局部改写（不动 citations）。
- 旁白式 opener（例如 “This section provides an overview …”）跨小节复用：提示把“overview”改写为 tension/lens/decision opener（不改事实与 citations）。
- limitation 槽位模式化：提示“换表达方式/换位置/合并到对比段落”，并给正反例。
- 句式收束词复用（key point / in practice / as a result 过密）：提示节奏变化策略（短句+长句交替、避免每段同构）。

状态（已落地到 repo 设计）：
- `writer-selfloop` 在 PASS 时会产出 `## Style Smells (non-blocking)`（写入 `output/WRITER_SELFLOOP_TODO.md`）。
- 修复：writer-selfloop 的 style-smell/path-extract regex 曾因 raw string 过度转义失效（导致 Style Smells 永远为 `(none)`，FAIL 时也难以定位 failing files）；已修正以保证风格自循环可用。
- 新增 `style-harmonizer` skill 作为默认路由动作（局部去槽位句式/去同质化；不改 citation keys）。

验证方式（最小可复现）：
- 在 `workspaces/<ws>/output/WRITER_SELFLOOP_TODO.md` 中，即使 PASS 也应出现一个 “Style Smells” 小节；对同一 draft，smell 数量应随迭代下降。

### 5.2 写作 skills 的“语义化约束”要更前置（把“如何写好”编码进合同，而不是事后打回）

对 `subsection-writer`/`front-matter-writer`/`chapter-lead-writer` 的共同写作合同建议统一增加：
- 禁止“计数式 opener”：不要以 “Two limitations…”、“Three takeaways…” 作为固定段落开头（除非整篇只用一次且非常自然）。
- limitation 写法的可选动作（给 writer 选择，而非强制模板）：
  - 作为对比段的最后一句（限定适用边界）
  - 作为单独段落，但 opener 必须变化（e.g., “A caveat is…”, “Evidence remains thin when…”, “These results hinge on…”）
  - 以 “verification targets” 形式表达（缺哪些协议字段才能升级结论）
- 统一 discourse palette：提供 6–8 种可替换的收束句式（但明确“不是模板句”，必须语义一致）。

收益：
- 直接削弱“固定槽位句式”的生成器信号；同时不需要靠硬编码规则阻断。

风险：
- 过度强调多样性可能导致漂移/花哨；缓解：多样性只约束“句式槽位”，不约束论证动作与证据链。

### 5.3 profile-aware 的“survey 交付门槛”需要更清晰（lite=验证链路；survey/deep=对标产出）

建议把 `draft_profile` 的语义从“gate 轻重”升级为“交付形态合同”：
- lite：验证 pipeline 能跑通 + 论文外形不崩（结构预算、无旁白、方法学段落 1 次）。
- survey：必须包含 >=2 张关键表（taxonomy + evaluation/protocol）+ 更高 global unique citations（建议 >=110）。
- deep：默认 fulltext evidence（成本高，但对标更像论文）+ 更厚 H3（更严格的对比/评测锚点要求）。

验证方式：
- `output/GLOBAL_REVIEW.md` 的 “Tables/Timeline/Figures” 不再长期为 0（至少在 survey/deep）。
- `output/AUDIT_REPORT.md` 的 unique citations 在 survey profile 下达到更高门槛。

### 5.4 审计链闭环：让 “FAIL -> 修复 -> PASS” 在单一入口可回放

设计目标：任何读者只看 `output/QUALITY_GATE.md` 就能知道“现在是否通过、最终证据在哪里”。

最小验证：
- `output/QUALITY_GATE.md` 的最后一个条目必须是 PASS（或明确链接到最终 PASS 的 report），避免“尾部 FAIL 误导”。

状态（已落地到 repo 设计）：
- `artifact-contract-auditor` 在 pipeline 完成（或检测到 contract drift）时会向 `output/QUALITY_GATE.md` 追加 PASS/FAIL 快照，作为单一入口的尾部状态。

---

## 6) 下一轮回放建议（验证改造是否真的拉近对标）

建议用同一主题做两次回放（只改 profile），来验证“结构改造能否可控地产生更强的 survey 形态”：

1) survey 回放（默认交付；对齐最终目标）
- 目标：>=2 表、global unique citations >=110、front matter 引用密度明显更高、Style Smell Appendix 明显下降、PDF 成功编译。
- 对标：`ref/agent-surveys/STYLE_REPORT.md` 的 section count 与论文形态。

2) deep 回放（更严格；更像论文）
- 目标：优先使用 `evidence_mode: fulltext`；H3 更厚（>=10 段、>=12 unique cites）；global unique citations 达到 deep profile 门槛；numeric claims 的最小评测上下文更完整。

注：`lite` 仅用于“跑通链路/快速调试”，会显著下调 global unique-citation 目标，不再作为默认建议（容易偏离你的最终交付标准）。

如果 survey 能稳定 PASS，但 deep 反复 FAIL，则说明问题不在写作阶段，而在 C3/C4 的 substrate（brief/binding/pack/anchors）仍不足以支撑更高密度的论证动作：应优先加强 evidence self-loop 的“可写性坏味道”路由，而不是让 writer 去硬写。
