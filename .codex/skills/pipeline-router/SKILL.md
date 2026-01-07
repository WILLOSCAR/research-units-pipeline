---
name: pipeline-router
description: Select the most appropriate pipeline for a user goal (snapshot/survey/tutorial/systematic-review/peer-review), lock it in `PIPELINE.lock.md`, and create/route human checkpoint questions into `DECISIONS.md`. Use when the workflow or pipeline choice is unclear or needs confirmation.
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

- Draft checkpoint questions / summaries: `python .codex/skills/pipeline-router/scripts/run.py --workspace <workspace_dir> --checkpoint C0|C2`
