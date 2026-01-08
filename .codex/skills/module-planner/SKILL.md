---
name: module-planner
description: |
  Plan tutorial modules from a concept graph, including module objectives and sequencing, saving as `outline/module_plan.yml`.
  **Trigger**: module plan, tutorial modules, course outline, 模块规划, module_plan.yml.
  **Use when**: tutorial pipeline 的结构阶段（C2），已有 `outline/concept_graph.yml`，需要把概念依赖转成可教学的模块序列。
  **Skip if**: 还没有 concept graph（先跑 `concept-graph`）。
  **Network**: none.
  **Guardrail**: 每模块明确 objectives + outputs（最好含 running example 步骤）；避免 prose 段落。
---

# Skill: module-planner

## Goal

- Produce a module plan that is executable and testable.

## Inputs

- `outline/concept_graph.yml`

## Outputs

- `outline/module_plan.yml`

## Procedure (MUST FOLLOW)
Uses: `outline/concept_graph.yml`.


1. Create 4–10 modules ordered by prerequisites.
2. For each module, list objectives, key concepts, and a short checklist of outputs.
3. Mark which modules require a running example step.

## Acceptance criteria (MUST CHECK)

- [ ] Every module has objectives and outputs.
