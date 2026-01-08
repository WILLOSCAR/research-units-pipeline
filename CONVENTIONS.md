# Conventions

## Workspaces

推荐每次运行一个 workspace（目录自定义），并保持“状态可审计、工件落盘”：

- `STATUS.md`：当前进度摘要
- `PIPELINE.lock.md`：锁定本次运行选择的 pipeline（单一事实来源）
- `GOAL.md`：本次目标/主题（用于自动生成 queries 与决策问题）
- `UNITS.csv`：执行合同（逐条 unit、依赖、验收、状态）
- `CHECKPOINTS.md`：检查点标准（每个 checkpoint 的可检查条件）
- `DECISIONS.md`：人类签字页（HITL）

模板位于：`.codex/skills/workspace-init/assets/workspace-template/`

## Human approvals

推荐用 `DECISIONS.md` 的 `## Approvals` 勾选项作为可机读的签字点：
- `## Approvals` 会根据 `UNITS.csv` 中 `owner=HUMAN` 的行自动生成（只包含当前 pipeline 需要的 checkpoint）。
- 执行器遇到 `owner=HUMAN` 的 unit 时，会检查对应 `Approve C*` 是否已勾选；已勾选则自动通过，否则停下等待。

## Skills

本 repo 的 skill 约定（结构、脚本使用、LLM-first）见 `SKILLS_STANDARD.md`。

## Offline-first (no network) conventions

当网络受限/不可用时，优先使用“先落盘可审计工件，再择机验证”的流程：

- 引用验证：`citations/verified.jsonl` 允许 `verification_status=offline_generated`（表示已记录但尚未联网核验）；联网后用 `citation-verifier --verify-only` 进行补验证。
- 全文证据：优先 `queries.md` 设 `evidence_mode: "abstract"`（不下载）；如必须全文，用 `papers/pdfs/<paper_id>.pdf` + `pdf-text-extractor --local-pdfs-only`，并查看 `output/MISSING_PDFS.md` 补齐缺失 PDF。

## File formats (suggested)

### `papers/*.jsonl`
- 1 行 1 条 JSON 记录（便于追加与 diff）
- 最小字段建议：`title`, `authors`, `year`, `url`（以及可选的 `abstract`, `source`, `query`, `score`）

### `papers/core_set.csv`
- 核心论文集合（建议含 `paper_id`, `title`, `year`, `url`, `topic`, `reason`）

### `outline/taxonomy.yml`
- 至少 2 层 taxonomy；每个节点要有简短解释

### `outline/outline.yml`
- 仅 bullets（无长 prose），用于驱动写作与映射
- 推荐结构：section/subsection 使用显式 `id`（例如 `2.1`），便于脚本化处理

### `outline/mapping.tsv`
- 每小节映射论文列表，便于追踪覆盖率

### `citations/verified.jsonl`
- 每条 bib entry 一条验证记录（至少：`url`, `date`, `title`；可加 `bibkey`, `notes`）
- 建议字段：`verification_status` ∈ `offline_generated` | `verified_online` | `verify_failed` | `needs_manual_verification`
