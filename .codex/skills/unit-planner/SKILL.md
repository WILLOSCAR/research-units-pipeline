---
name: unit-planner
description: Instantiate or update a workspace `UNITS.csv` from a selected pipeline and units template, including dependencies, checkpoints, and acceptance criteria. Use when creating the execution contract or when scope changes require new/updated units.
---

# Skill: unit-planner

## Goal

- Turn a pipeline (`pipelines/*.pipeline.md`) into a concrete `UNITS.csv` contract for a specific workspace.

## Inputs

- `PIPELINE.lock.md` (preferred) or a chosen `pipelines/*.pipeline.md`
- `templates/UNITS.*.csv` referenced by the pipeline front matter
- Existing workspace artifacts (to adjust scope if needed)

## Outputs

- `UNITS.csv` (in the workspace root)
- Optional: `STATUS.md` updated with next runnable units

## Procedure (MUST FOLLOW)

1. Read `PIPELINE.lock.md` (or ask to create it via `pipeline-router`).
2. Copy the pipeline’s `units_template` into the workspace as `UNITS.csv` if missing.
3. If `UNITS.csv` exists, only edit it to reflect:
   - new scope (add rows)
   - corrected dependencies
   - clarified acceptance criteria
4. Ensure every unit has: `unit_id`, `skill`, `outputs`, `acceptance`, `checkpoint`, `status`, `owner`.
5. Keep checkpoints consistent with `CHECKPOINTS.md`; add missing checkpoints if the pipeline uses custom checkpoints.

## Acceptance criteria (MUST CHECK)

- [ ] `UNITS.csv` parses as CSV and includes all required columns.
- [ ] Every `depends_on` references an existing `U###`.

## Side effects

- Allowed: edit `UNITS.csv`, `STATUS.md`, `CHECKPOINTS.md` (for adding custom checkpoints).
- Not allowed: change pipeline files in `pipelines/` unless requested.
