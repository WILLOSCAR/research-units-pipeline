---
name: workspace-init
description: Initialize a new workspace by copying the standard artifact template (STATUS.md, CHECKPOINTS.md, UNITS.csv, DECISIONS.md plus papers/outline/citations/output folders). Use when starting any pipeline workspace.
---

# Workspace Init

Create an artifact-first workspace using the standard template under `assets/workspace-template/`.

This skill is intentionally simple and deterministic.

## Input

- Target workspace directory (usually the current working directory for the run).

## Outputs

- `STATUS.md`, `CHECKPOINTS.md`, `UNITS.csv`, `DECISIONS.md`
- `GOAL.md`
- `queries.md`
- `papers/`, `outline/`, `citations/`, `output/` (with placeholder files)

## Workflow

1. Create the target workspace directory if it does not exist.
2. Copy the contents of `assets/workspace-template/` into the workspace.
3. Do not overwrite existing files unless explicitly requested; prefer merge/append when safe.
4. Ensure the four core files exist: `STATUS.md`, `UNITS.csv`, `CHECKPOINTS.md`, `DECISIONS.md`.

## Quality checklist

- [ ] Workspace contains the template files and folders.
- [ ] `UNITS.csv` is valid CSV with the required header.

## Side effects

- Allowed: create missing workspace files/directories.
- Not allowed: modify the template under `.codex/skills/workspace-init/assets/`.

## Script

- `python .codex/skills/workspace-init/scripts/run.py --workspace <workspace_dir>`
