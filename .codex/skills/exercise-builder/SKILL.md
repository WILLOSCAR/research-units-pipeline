---
name: exercise-builder
description: |
  Add exercises to each tutorial module (inputs, expected outputs, verification steps) and update `outline/module_plan.yml`.
  **Trigger**: exercises, practice, verification checklist, 教程练习, 可验证作业.
  **Use when**: 已有模块计划（`outline/module_plan.yml`），需要为每个模块补齐至少 1 个可验证练习以形成 teaching loop。
  **Skip if**: 还没有 module plan（先跑 `module-planner`）。
  **Network**: none.
  **Guardrail**: 每个练习必须包含 expected output + verification steps；避免只给“思考题”无验收。
---

# Skill: exercise-builder

## Goal

- Ensure each module has at least one verifiable exercise.

## Inputs

- `outline/module_plan.yml`

## Outputs

- Updated `outline/module_plan.yml`

## Procedure (MUST FOLLOW)

1. For each module, add ≥1 exercise with:
   - prompt
   - expected output
   - verification checklist
2. Keep exercises aligned to learning objectives.

## Acceptance criteria (MUST CHECK)

- [ ] Every module has at least one exercise with verification.
