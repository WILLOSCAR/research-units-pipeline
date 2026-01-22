# Pipeline / Skills Improvement Backlog (arxiv-survey-latex)

Last updated: 2026-01-22

本文件只跟踪 **pipeline + skills 的结构性改进**（不是某次 draft 的内容修修补补）。

主诊断文档：`PIPELINE_DIAGNOSIS_AND_IMPROVEMENT.md`

回归与对标锚点（用于复现问题与验证改进；不改 workspace 产物）：
- 最新基线 workspace：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/`
- 回归基线 workspace：`workspaces/_refs/baselines/e2e-agent-survey-latex-verify-20260119-120720/`
- 对标材料：`ref/agent-surveys/STYLE_REPORT.md`

---

## 0) 上一版内容 Summary（change log 视角；作为新起点）

上一版（2026-01-21）的 question.md 把“从终稿倒推”的诊断结论任务化，核心是三类 P0/P1/P2 改造：

- P0（可信 + 可审计 + 不再一眼自动化）：修 transition 注入源（post-merge voice gate）、把 front matter 方法学段落变成硬合同、numeric claim 的最小协议上下文、两条 self-loop 的路由、以及“脚本不写语义内容”的分层。
- P1（paper voice + 论证密度）：写作 role 化（Section Author / Evidence Steward / Style Harmonizer）、chapter lead 条件必做、transitions 两条路线二选一。
- P2（结构性重构）：visuals（表/时间线/图规格）的产品策略、outline 预算自循环、以及 schema/接口一致性方向。

最新基线（20260122）验证了其中一部分方向确实有效（methodology note 落盘、post-merge voice PASS、H3 预算收敛），但也暴露了新的共性缺陷：风格同质化（“Two limitations …” 槽位句式）、audit sink 断链、以及 C3 briefs 的轴表达仍有 scaffold 坏味道。

---

## P0 — 必须先修（paper voice 可信 + 审计可回放 + 自循环能收敛）

### P0-1 Writer self-loop 增加 “Style Smell Appendix”（PASS 也要可见）

问题（终稿可证）：
- “Two limitations …” 在所有 H3 反复出现：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/DRAFT.md:55`

状态（已落地）：
- `writer-selfloop` 在 PASS 时也会写出 `## Style Smells (non-blocking)`（见 `output/WRITER_SELFLOOP_TODO.md`）。
- 修复：writer-selfloop 的 regex 曾因 raw string 过度转义导致 Style Smells 永远是 `(none)`，且 FAIL 时难以抽取 failing file paths；已修正以便稳定路由到 `style-harmonizer`。
- 新增 `style-harmonizer`（局部去槽位句式/去同质化；不改 citation keys），作为 PASS 后的默认路由动作。

设计改造（建议）：
- writer-selfloop 在 PASS 时也输出 “Style Smells”（不一定 BLOCK，但必须可路由）：
  - 计数式 opener（Two limitations/Three takeaways）跨小节高频复用
  - 固定收束句式（The key point is that…）过密
  - 旁白式 opener（This section provides an overview… / … overview …）跨小节复用
  - limitation 槽位模式化（同一句式、同一位置）
- 路由策略：只触发 Style Harmonizer 对应的局部改写（不动事实/不动 citation keys），而不是重写全稿。

验证：
- `workspaces/<ws>/output/WRITER_SELFLOOP_TODO.md` 在 PASS 时包含 “Style Smells” 小节，且同一主题迭代后 smell 数量下降。

---

### P0-2 写作技能合同：禁止“计数式段落开头”成为默认句式

问题（共性）：
- 即使没有 “This subsection…” 模板，计数式 opener 仍会形成“生成器味”的高信号。

设计改造（建议）：
- 对 `subsection-writer` / `front-matter-writer` / `chapter-lead-writer` 统一追加写作合同：
  - 禁止把 “Two limitations … / Three contributions …” 当作固定段落开头（除非整篇只用一次且非常自然）。
  - limitation 的三种可选落点（给 writer 选择，不给模板句）：
    - 融入对比段最后一句（限定适用边界）
    - 单独段落但 opener 必须变化（A caveat is… / Evidence remains thin when… / These results hinge on…）
    - verify targets（缺哪些协议字段才能升级结论）

状态（已落地，仍可继续细化）：
- 已在 `subsection-writer` / `front-matter-writer` / `chapter-lead-writer` 的写作合同中显式加入 “count-based opener slot” 禁止项与改写指引。
- 已在 `writer-context-pack` 的 `paper_voice_palette.json` 中加入相关 watchlist（soft guidance），降低 writer 默认落入同一句式槽位的概率。

验证：
- 终稿中 “Two limitations …” <= 1 次（或 0 次），但每个 H3 仍然存在 limitation 动作（语义不丢）。

---

### P0-3 Auditability：让 QUALITY_GATE 作为单一入口可回放 “FAIL -> 修复 -> PASS”

问题（终稿可证）：
- `output/QUALITY_GATE.md` 文件尾仍停留在 FAIL，但 pipeline 实际已经完成：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/QUALITY_GATE.md:410`

设计改造（建议）：
- 把审计链闭环写成 pipeline/skills 合同：任何“质量门”在最终通过时必须回写到一个统一入口（QUALITY_GATE 或等价的 run summary）。
- 最小策略：即使保留各 skill 独立 report，也要在 QUALITY_GATE 的尾部写入 “最终 PASS + 指向最终 report 的链接”。

验证：
- QUALITY_GATE 的最后一个条目必须是 PASS（或明确链接到最终 PASS 的 report），避免“尾部 FAIL 误导”。

状态（已落地：最小策略）：
- `artifact-contract-auditor` 会在 pipeline 完成（或检测到 DONE outputs 丢失）时向 `output/QUALITY_GATE.md` 追加一条 PASS/FAIL 快照，使 QUALITY_GATE 尾部状态可读且可回放。

---

### P0-4 C3 briefs 的 “axes contract” 要修（避免逗号切碎与 and-leading）

问题（中间态可证）：
- axes 被逗号切碎、条目以 and 开头：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/outline/subsection_briefs.jsonl:1`

设计改造（建议）：
- `subsection-briefs` 明确 axes 的输出合同：
  - 每个 axis 必须是一个完整的名词短语（atomic phrase），不得依赖逗号拆分
  - axis 条目不得以 and/以及/并且 开头
  - 如需子轴：用分号或括号描述，但整体仍作为单一 axis 条目
- `schema-normalizer` 或 evidence-selfloop 增加 “brief smell” 报告（不一定 BLOCK，但必须显式提示）。

验证：
- 任意 H3 的 axes list 不再出现被切碎的条目；并且能被 writer packs 直接消费而不产生 slash-list 写法诱因。

状态（已落地）：
- `subsection-briefs` 的脚本侧 list 抽取逻辑已修复：不再在括号内逗号处分裂 axis；同时会清理 and/以及/并且 等 leading 连接词碎片。
- `subsection-briefs/SKILL.md` 已补充 axes contract（建议用分号做顶层分隔；括号内逗号允许）。

---

### P0-5 transitions 合同对齐（避免“写了但不注入 / gate 与注入错位”）

问题（设计错位）：
- transitions 文件同时包含 H2 与 H3 过渡，但默认 merge 只注入 H3；质量门却可能按 bullets 计数导致补写无效内容。

设计改造（建议，二选一并固化）：
- 路线 A：拆分 transitions（例如 H2 与 H3 分开管理），并让 gate 与 merge 注入严格对齐。
- 路线 B：保留单文件，但 gate 规则按“预计注入条目数”计算（基于 H3 结构），避免用硬阈值逼出无效 bullets。

验证：
- transitions 的每一条“要求写”的内容，都能在终稿中找到对应注入点（或明确标记为 intent-only）。

状态（已落地：路线 B）：
- `tooling/quality_gate.py` 的 transitions gate 已从硬阈值改为“按 outline 的 H3 邻接边数量计算 expected transitions”，并要求 `outline/transitions.md` 覆盖这些 H3→H3 边（避免补写无效 bullets）。

---

## P1 — 提升 survey 形态（对标材料差距的主要来源）

### P1-1 survey/deep profile 的“>=2 张关键表”门槛（taxonomy + evaluation/protocol）

问题（对标差距）：
- 视觉/结构产物缺失：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/GLOBAL_REVIEW.md:27`

设计改造（建议）：
- profile-aware 合同：
  - debug（lite）：允许 0 表（仅用于跑通链路/快速调试；不作为默认交付）
  - survey/deep：默认 >=2 表（taxonomy 表 + benchmark/protocol 表）
- 将 `table-schema` -> `table-filler` 的产物视为“写作一等输入”（writer 必须引用/解释表，而不是把表当附件）。

验证：
- survey/deep profile 的 `output/DRAFT.md`（或 LaTeX/PDF）出现 >=2 张可编译表，且每行有 citations。

---

### P1-2 引用密度：从 “PASS(76/220)” 升级到 survey 期望（>=110 unique keys）

问题（基线可证）：
- Bib entries 220，但 draft unique citations 只有 76：`workspaces/e2e-agent-survey-latex-verify-20260122-094516/output/AUDIT_REPORT.md:8`

设计改造（建议）：
- survey profile 的 citation budget 全局目标提高（建议 >=110），并显式要求 front matter 引用密度更高（Intro/Related Work 更密）。
- binder/packs 要给 writer 更宽的可选 citations（在不破坏 scope 的前提下），让 citation-diversifier/injector 有空间发挥。
- 防误用：`draft_profile: lite` 会显著降低 global unique-citation 目标（用于“跑通链路”验证），从而让 citation-injector 可能 no-op；要交付 citation-rich survey，请用 `draft_profile: survey`。

验证：
- survey profile 的 `output/AUDIT_REPORT.md` unique citations >=110，且 per-H3 不出现“引用堆砌段”（仍保持 argument moves）。

---

### P1-3 methodology 升级为更可复现的结构（可选但高收益）

现状：
- 已有 one-paragraph evidence policy（含候选池/核心集合/证据模式），但缺少 RQ/selection/dataset accounting 等结构锚点。

设计改造（建议）：
- 在 front matter 合同中新增可选 block（仍保持短）：
  - research questions（3–7 条）
  - inclusion/exclusion 的一句话准则
  - benchmark/dataset accounting（至少给出“覆盖哪些类型 benchmark”的结构点）

验证：
- 读者在前 2 页内能回答：范围是什么、怎么选的、证据强度如何、本文用什么 lens 组织。

---

## P2 — 结构性重构（降低 drift，提高可组合性）

### P2-1 refined markers 从“checkbox”升级为“最小可验证精炼证明”

问题（共性）：
- 标记 refined 并不能保证 substrate 没有 scaffold 坏味道（例如 axes 切碎仍存在）。

设计改造（建议）：
- 为每类 refined marker 定义最小检查点（例如 axes 格式、paragraph_plan 是否含对比/评测锚点/局限动作、blocking_missing 是否为 0）。
- 将检查点写入 skills 合同与 self-loop TODO 中（避免靠脚本硬拦，但必须可审计）。

验证：
- refined.ok 不再只是“人为触发”，而是伴随一份“我检查过什么”的可回放记录。

---

### P2-2 角色化写作技能再拆分（可组合，而不是一锅 writer）

方向（建议）：
- 把写作阶段明确拆成可组合的语义单元（不必都脚本化）：
  - Section Author：论证动作
  - Evidence Steward：可核查性挑刺（数字上下文/过度外推）
  - Style Harmonizer：去同质化、去槽位句式、统一节奏

验证：
- writer-selfloop 的 TODO 能清晰区分：“证据不足” vs “论证动作缺失” vs “风格同质化”。

---

## 产品/策略问题（需要你拍板）

- Style Smells：是 “PASS 但提示” 还是 “直接 BLOCK”？（建议先提示，等误报率低再升级）
- survey profile：是否把 “>=2 表 + >=110 unique citations” 定义为默认门槛？
- transitions：是否要把 H2 transitions 默认注入，还是保持 intent-only？
- methodology：你想要“轻量一段 policy”还是“短 RQ + selection/accounting”的更论文式做法？
