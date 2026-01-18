# Pipeline / Skills Improvement Backlog (arxiv-survey-latex)

本文件只跟踪 **pipeline + skills 的结构性改进**（不是某次 draft 的内容修修补补）。

诊断主文档：`PIPELINE_DIAGNOSIS_AND_IMPROVEMENT.md`

回归基线 workspace（用于复现问题与验证改进，不是交付物）：
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/`

对标材料（写法/结构基准）：
- `ref/agent-surveys/STYLE_REPORT.md`

---

## P0 — 必须先修（可信 + 可审计 + 不再一眼自动化）

### P0-1 合同闭环：DONE 必须意味着“产物存在”

现象（baseline 可证）：
- pipeline `target_artifacts`=38，workspace 缺 2 个 QA 报告：
  - `workspaces/e2e-agent-survey-latex-verify-20260118-182656/output/SECTION_LOGIC_REPORT.md`
  - `workspaces/e2e-agent-survey-latex-verify-20260118-182656/output/GLOBAL_REVIEW.md`

为什么是 P0：
- 这是 Units 合同失效，会直接让自循环失去证据（只能靠“感觉”改写）。

建议改动（偏合同/流程，不靠硬风格 gate）：
- 把“报告类 skill”合同写死：PASS/FAIL 都必须写 report 文件。
  - 目标 skill：`section-logic-polisher`, `global-reviewer`（至少这两个）
- 新增（或合并进 `pipeline-auditor`）：`artifact-contract-auditor`
  - 输出：`output/CONTRACT_REPORT.md`（缺失项列表 + PASS/FAIL）

预期收益：
- 每个 workspace 可作为回归样本；质量与失败可复盘。

风险：
- 更严格会暴露更多“以前假装跑通”的 run（属预期）。

验证：
- 任意一次 e2e：38/38 target artifacts 存在；或 `CONTRACT_REPORT` 明确列出 optional/missing。

---

### P0-2 失败沉淀：BLOCKED 不再需要重跑才能定位

现象（baseline 可证）：
- `STATUS.md` 有 `BLOCKED (script failed)` / `BLOCKED (quality gate: output/QUALITY_GATE.md)`，但 workspace 中没有对应的错误沉淀文件。

建议改动：
- 为所有 pipeline 定义两个标准 error sinks（append-only）：
  - `output/QUALITY_GATE.md`：gate code + 路由建议（回到哪个 stage/skill 修）
  - `output/RUN_ERRORS.md`：unit_id + timestamp + stderr 摘要

验证：
- 人为制造失败（删 input），run 结束后上述两个文件必存在且可定位到具体 unit。

---

### P0-3 transition-weaver 去“planner talk”（最影响论文感）

现象（baseline 可证）：
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/outline/transitions.md` 含大量构建注释句（分号枚举、turning framing into…）。
- 被 merge 后出现在 `output/DRAFT.md:59/111/165/221`。

为什么是 P0：
- transition 是全篇高频句型，一旦像注释，读者第一眼判定“自动生成”。

建议改动（优先语义化引导）：
- transition-weaver 的默认输出必须是“内容论证桥”（1 句即可）：
  - 写：上一节结论/局限 → 下一节为什么重要
  - 不写：工具链路/构建过程/“setting up a cleaner A-vs-B comparison”
- 明确禁止模式（写入 SKILL.md + auditor 检测）：
  - `After .* makes the bridge explicit via`
  - `follows naturally by turning .* framing into`
  - 分号 `;` 形式的枚举规划句

验证：
- `outline/transitions.md` 不包含上述模式；`output/DRAFT.md` 也为 0。

---

### P0-4 DECISIONS checkpoint 绑定 workspace（审计性 canary）

现象（baseline 可证）：
- `workspaces/e2e-agent-survey-latex-verify-20260118-182656/DECISIONS.md` 的 C0 kickoff block workspace 路径是旧的。

建议改动：
- pipeline-router 写 checkpoint block 时必须刷新 workspace/pipeline 行。
- block 中增加 self-check：显示当前目录名（使 drift 可见）。

验证：
- 新 workspace 的 DECISIONS.md C0 block 永远指向自身目录。

---

## P1 — 提升 paper voice（减少“正确但空”）

### P1-1 subsection-briefs：让 thesis/contrast 更“具体张力”

现象：
- thesis/contrast_hook 偏泛（如 tension 只落在“mechanism/data”轴），writer 容易回到 `Taken together` / `survey should` 省力口吻。

建议改动：
- 给每个 H3 强制新增两个字段（NO PROSE）：
  - `tension_statement`：具体张力句（例如“表达性 vs 可验证性”），必须可直接做段落 1 的核心句
  - `evaluation_anchor_minimal`：task + metric + constraint 三元组（允许 unknown slot，但要显式标注）
- connector_phrase 改为 clause-level 短提示，禁止整句（降低 copy-paste 模板化）。

验证：
- audit：`Taken together` <=2；`survey ... should` <=1。

---

### P1-2 writer-context-pack：补“正向写法引导”（替代句式库）

现象：
- pack 已有禁令（do_not_repeat）但缺少替代句式/微结构提示。

建议改动：
- 新增结构化字段 `paper_voice_palette`：
  - opener archetypes（decision-first/tension-first/evidence-first）示例
  - synthesis alternatives（替代 Taken together）
  - rewrite rules（把 survey should → 内容主张句 的映射）

验证：
- audit report 中 phrase family 复发显著下降；且不靠硬 blocking。

---

### P1-3 evidence-binder：从“同构配方”变成 subsection-specific 证据计划

现象（baseline 可证）：
- `outline/evidence_binding_report.md` 每节同样 mix：limitation=1/method=1/result=10。

建议改动：
- evidence-binder 输出增加：
  - `binding_rationale`（短 bullet）：这些 evidence 如何覆盖 axes
  - `binding_gaps`：哪些 required_evidence_fields 未覆盖（回退到 C3 或 C1）

验证：
- binding report 能看到小节差异；gaps 能驱动自循环回到上游补证据。

---

## P2 — 结构性重构（减少无效劳动 + 降 drift）

### P2-1 visuals（tables/timeline/figures）：要么 optional，要么闭环注入

现象（baseline 可证）：
- workspace 有 `outline/tables.md`/`timeline.md`/`figures.md`，但 `latex/main.tex` 不包含它们。

二选一决策：
1) 简化：把 table-schema/table-filler/survey-visuals 改为 optional（默认不跑）。
2) 闭环：新增 `visuals-inserter`（C5）把这些内容插入 DRAFT/LaTeX。

验证：
- 若闭环：PDF 中至少出现 1–2 张表（或 timeline/figure placeholder），且引用可编译。

---

### P2-2 schema 规范化（减少 best-effort heuristics）

现象（baseline 可证）：
- briefs 有 section_id，evidence_drafts 没有；citations 表达格式不统一。

建议改动：
- 在 `SKILLS_STANDARD.md` 写清 JSONL interface schema（必填字段 + citation key 规范）。
- 可选：新增 `schema-normalizer` skill（NO PROSE，deterministic）。

验证：
- briefs → evidence packs → writer packs 无需 heuristics join。

---

## 产品/策略问题（需要你拍板）

- “一键跑”默认 profile：`lite`（速度）还是 `survey`（论文感）？
- transition/meta-voice：长期保持 warning，还是成熟后升级为 blocking？
- citation scope：想要严格计划（writer 必须跟 plan），还是软计划（writer 可在 mapped 内选 + injector 补）？

