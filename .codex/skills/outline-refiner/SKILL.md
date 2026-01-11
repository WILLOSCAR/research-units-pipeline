---
name: outline-refiner
description: |
  Planner-pass coverage + redundancy report for an outline+mapping, producing `outline/coverage_report.md` and `outline/outline_state.jsonl`.
  **Trigger**: planner, dynamic outline, outline refinement, coverage report, 大纲迭代, 覆盖率报告.
  **Use when**: you have `outline/outline.yml` + `outline/mapping.tsv` and want a verifiable, NO-PROSE planner pass before writing.
  **Skip if**: you don't want any outline/mapping diagnostics (or you have a frozen/approved structure and will not change it).
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent papers; only report coverage/reuse and propose structural actions as bullets.
---

# Outline Refiner (Planner pass, NO PROSE)

Goal: make the outline *auditable* by adding an explicit planner stage that answers:
- Do we have enough evidence per H3?
- Are the same few papers reused everywhere?
- Are subsection axes still generic/scaffold-y?

This is a deterministic “planner” unit: it should not write survey prose.


## Roles (planner council, NO PROSE)

Use a multi-role lens when interpreting the report (still bullets-only):

- **Planner**: is the structure actually answerable (RQ + evidence needs per H3)?
- **Librarian**: do we have enough mapped papers per H3; where are coverage gaps?
- **Taxonomist**: are subsection titles and axes consistent and non-overlapping?
- **Skeptic**: where is the outline generic/scaffold-y; where will writer produce template prose?
- **Integrator**: do `outline.yml`, `mapping.tsv`, and briefs align (no drift / no stale artifacts)?

## Inputs

Required:
- `outline/outline.yml`
- `outline/mapping.tsv`

Optional (improves diagnosis):
- `papers/paper_notes.jsonl` (for evidence levels)
- `outline/subsection_briefs.jsonl` (for axis specificity)
- `GOAL.md` (for scope drift hints)

## Outputs

- `outline/coverage_report.md` (bullets + small tables; NO PROSE)
- `outline/outline_state.jsonl` (append-only JSONL; one record per run)

## Freeze policy

- If `outline/coverage_report.refined.ok` exists, the script will not overwrite `outline/coverage_report.md`.

## What this skill should *not* do

- Do not rewrite the draft.
- Do not fabricate evidence.
- Do not silently change the approved outline.

## Script

- `python .codex/skills/outline-refiner/scripts/run.py --workspace <ws>`
