# Working agreements (research-units-pipeline)

## Prime directive
- This repo uses **UNITS** (work units) as the execution contract (not Issues).
- Always work artifact-first: update `STATUS.md`, `UNITS.csv`, `CHECKPOINTS.md`, `DECISIONS.md`.
- Follow checkpoints: **NO PROSE** until the required checkpoints are satisfied and any required HUMAN sign-off is recorded in `DECISIONS.md`.
- Never create workspace artifacts in the repo root; use `workspaces/<name>/`.

## Units contract
- Only mark a unit `DONE` when its acceptance criteria are satisfied and outputs exist.
- If scope grows, add new units (new rows) and keep `UNITS.csv` valid CSV.
- Use `BLOCKED` when a unit is waiting for a human checkpoint or a dependency.

## Skills usage
- Prefer repo skills under `.codex/skills/`.
- If a required capability is missing, propose a new skill folder with `SKILL.md` (do not proceed ad-hoc).

## Citations (when applicable)
- Every BibTeX entry must have a verification record in `citations/verified.jsonl` (at minimum: `url`, `date`, `title`).

## Human-in-the-loop
- Stop at declared human checkpoints.
- Write a concise question list into `DECISIONS.md` and wait for explicit sign-off before proceeding.
- Default to a single approval checkpoint when possible (survey flow: `C2`); avoid asking for repeated confirmations unless the user requests tighter control.
