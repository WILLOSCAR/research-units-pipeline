---
name: exercise-builder
description: Add exercises to each tutorial module (inputs, expected outputs, verification steps) and update the module plan accordingly. Use when enforcing a teaching loop where each module has at least one verifiable exercise.
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

