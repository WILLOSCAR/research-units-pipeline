---
name: pipeline-router
description: |
  Select the most appropriate pipeline for a user goal, lock it in `PIPELINE.lock.md`, and route checkpoint questions into `DECISIONS.md`.
  **Trigger**: pipeline router, choose pipeline, workflow selection, PIPELINE.lock.md, 选择流程.
  **Use when**: 用户目标/交付物不清晰，需要在 snapshot/survey/tutorial/systematic-review/peer-review 中选一个并设置最小 HITL 问题集。
  **Skip if**: pipeline 已锁定（`PIPELINE.lock.md` 存在）且所需问题已回答/签字完成。
  **Network**: none.
  **Guardrail**: 尽量一次性提问；信息不足就写 `DECISIONS.md` 并停下等待。
---

# Pipeline Router

Pick the right pipeline for the deliverable, lock it in the workspace, and set up the minimal human checkpoints.

When the user request is ambiguous, prefer asking a small set of questions once (survey flow usually uses a single approval checkpoint at C2).

## Inputs

- User request and constraints, or workspace context (`STATUS.md`, `DECISIONS.md`).
- Optional: `assets/pipeline-selection-form.md` as a question template.

## Outputs

- `PIPELINE.lock.md` (in the workspace root)
- Updates to `STATUS.md` and/or `DECISIONS.md` (if needed)

## Decision tree

User goal → choose:
- “survey / 综述 / 调研” → `pipelines/arxiv-survey*.pipeline.md`
- “tutorial / 教程” → `pipelines/tutorial.pipeline.md`
- “systematic review / PRISMA / 系统综述” → `pipelines/systematic-review.pipeline.md`
- “peer review / 审稿” → `pipelines/peer-review.pipeline.md`
- “snapshot / 速览” → `pipelines/lit-snapshot.pipeline.md`

## Workflow
Uses: `assets/pipeline-selection-form.md`.


1. Identify the intended deliverable and constraints (time window, paper count, language, need PDF output).
2. If key details are missing, write a concise question list into `DECISIONS.md` and stop.
3. Select exactly one pipeline file under `pipelines/`.
4. Write `PIPELINE.lock.md` with:
   - `pipeline: <path>`
   - `units_template: <path from pipeline front matter>`
   - `locked_at: <YYYY-MM-DD>`
5. Update `STATUS.md` “Current pipeline” to the chosen pipeline path.

## Quality checklist

- [ ] `PIPELINE.lock.md` exists and points to one pipeline file.
- [ ] If questions were required, they are written to `DECISIONS.md` and execution stops until answered.

## Side effects

- Allowed: create `PIPELINE.lock.md`; edit `STATUS.md`; append to `DECISIONS.md`.
- Not allowed: modify files under `.codex/skills/` assets/templates.

## Script

### Quick Start

- `python .codex/skills/pipeline-router/scripts/run.py --help`
- `python .codex/skills/pipeline-router/scripts/run.py --workspace <workspace_dir> --checkpoint C0`

### All Options

- `--checkpoint C0|C2`: which checkpoint question block to draft/update

### Examples

- Kickoff questions + seed queries (C0):
  - `python .codex/skills/pipeline-router/scripts/run.py --workspace <ws> --checkpoint C0`
- Scope/outline approval summary (C2):
  - `python .codex/skills/pipeline-router/scripts/run.py --workspace <ws> --checkpoint C2`

### Notes

- This helper updates `DECISIONS.md` and seeds `queries.md` from `GOAL.md` (for C0).
- It does not select a pipeline; pipeline selection is handled by `scripts/pipeline.py kickoff` / `PIPELINE.lock.md`.
