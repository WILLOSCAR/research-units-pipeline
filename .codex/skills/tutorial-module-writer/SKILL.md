---
name: tutorial-module-writer
description: |
  Write the tutorial content (`output/TUTORIAL.md`) from an approved module plan, including exercises and answer outlines.
  **Trigger**: write tutorial, tutorial modules, 教程写作, TUTORIAL.md.
  **Use when**: tutorial pipeline 的写作阶段（C3），且 `DECISIONS.md` 已记录 HUMAN 对 scope/running example 的批准（C2）。
  **Skip if**: module plan 未完成/未批准（先跑 `module-planner`/`exercise-builder` 并通过 Approve C2）。
  **Network**: none.
  **Guardrail**: 只写已批准范围；保持 running example 一致；每模块包含练习与答案要点。
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
Uses: `outline/module_plan.yml`.


1. Check `DECISIONS.md` for approval to write.
2. If missing, write a short request into `DECISIONS.md` and stop.
3. Write module-by-module with consistent structure: objective → explanation → exercise → expected output.

## Acceptance criteria (MUST CHECK)

- [ ] Only approved modules are written.
- [ ] Each module includes its exercises and expected outputs.
