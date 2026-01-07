---
name: unit-executor
description: Execute exactly one runnable unit from `UNITS.csv` (first TODO whose dependencies are DONE), using its referenced skill, then update unit status and artifacts. Use when driving the pipeline step-by-step with strict artifact outputs and checkpoint checks.
---

# Skill: unit-executor

## Goal

- Execute **one** unit end-to-end and leave the workspace in a consistent state.

## Inputs

- `UNITS.csv`
- Unit inputs listed in the row (files)

## Outputs

- Unit outputs listed in the row (files)
- Updated `UNITS.csv` status (`TODO → DOING → DONE/BLOCKED`)
- Optional: `STATUS.md` updated

## Procedure (MUST FOLLOW)

1. Load `UNITS.csv` and find the first unit with:
   - `status=TODO`
   - all `depends_on` units are `DONE`
2. Set its status to `DOING` and persist `UNITS.csv`.
3. Run the referenced skill (by following that skill’s `SKILL.md`).
4. Check the unit’s `acceptance` against produced artifacts.
5. If acceptance passes, set status to `DONE`; otherwise set to `BLOCKED` with a short note in `STATUS.md`.
6. Stop after one unit (do not start the next unit automatically).

## Acceptance criteria (MUST CHECK)

- [ ] Exactly one unit changes from `TODO` to `DONE/BLOCKED` (via `DOING`).
- [ ] Output files exist (or acceptance explicitly allows otherwise).

## Side effects

- Allowed: edit workspace artifacts (`UNITS.csv`, `STATUS.md`, unit outputs).
- Not allowed: modify `.codex/skills/` content.

## Script

- Run one unit (script runner): `python .codex/skills/unit-executor/scripts/run.py --workspace <workspace_dir> --strict`
- Or use repo wrapper: `python scripts/pipeline.py run-one --workspace <workspace_dir> --strict`
