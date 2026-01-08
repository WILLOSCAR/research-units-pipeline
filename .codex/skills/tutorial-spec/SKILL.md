---
name: tutorial-spec
description: |
  Define tutorial scope, target audience, prerequisites, learning objectives, and a running example; output a tutorial spec for downstream planning.
  **Trigger**: tutorial spec, scope, audience, prerequisites, learning objectives, running example, 教程规格.
  **Use when**: tutorial pipeline 的起点（C1），需要先锁定教学目标与边界，再进入 concept graph / module planning。
  **Skip if**: 你不是在做教程产出（或已经有明确且不允许改动的 tutorial spec）。
  **Network**: none.
  **Guardrail**: 结构化 spec 优先；避免提前写长教程 prose（prose 在 C3）。
---

# Skill: tutorial-spec

## Goal

- Produce a clear tutorial spec that constrains downstream writing.

## Inputs

- `STATUS.md` (optional existing context)
- User requirements

## Outputs

- `output/TUTORIAL_SPEC.md`

## Procedure (MUST FOLLOW)
Uses: `STATUS.md`.


1. Define target audience and prerequisites.
2. Define 5–10 learning objectives (measurable).
3. Define one running example and what artifacts learners will produce.
4. Define in-scope and out-of-scope topics.

## Acceptance criteria (MUST CHECK)

- [ ] Spec includes audience, prerequisites, objectives, running example, scope.
