---
name: tutorial-module-writer
description: Write the tutorial content (`output/TUTORIAL.md`) from an approved module plan, including exercises and answer outlines. Use only after HUMAN sign-off for scope/running example is recorded in `DECISIONS.md`.
---

# Skill: tutorial-module-writer

## Goal

- Produce readable tutorial prose only for approved modules.

## Inputs

- `outline/module_plan.yml`
- `DECISIONS.md` (must authorize writing)

## Outputs

- `output/TUTORIAL.md`

## Procedure (MUST FOLLOW)

1. Check `DECISIONS.md` for approval to write.
2. If missing, write a short request into `DECISIONS.md` and stop.
3. Write module-by-module with consistent structure: objective → explanation → exercise → expected output.

## Acceptance criteria (MUST CHECK)

- [ ] Only approved modules are written.
- [ ] Each module includes its exercises and expected outputs.

