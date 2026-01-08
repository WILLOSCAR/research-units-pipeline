---
name: concept-graph
description: |
  Build a concept graph (nodes + prerequisite edges) from a tutorial spec, saving as `outline/concept_graph.yml`.
  **Trigger**: concept graph, prerequisite graph, dependency graph, 概念图, 先修关系.
  **Use when**: tutorial pipeline 的结构阶段（C2），需要把教程知识点拆成可排序的依赖图（在写教程 prose 前）。
  **Skip if**: 还没有 tutorial spec（例如缺少 `output/TUTORIAL_SPEC.md`）。
  **Network**: none.
  **Guardrail**: 只做结构；避免写长 prose 段落。
---

# Skill: concept-graph

## Goal

- Make concept dependencies explicit to drive module ordering.

## Inputs

- `output/TUTORIAL_SPEC.md`

## Outputs

- `outline/concept_graph.yml`

## Procedure (MUST FOLLOW)
Uses: `output/TUTORIAL_SPEC.md`.


1. Extract key concepts (≥10 nodes).
2. Add prerequisite edges and short node descriptions.
3. Keep it structural (no prose explanations).

## Acceptance criteria (MUST CHECK)

- [ ] Concept graph has nodes, edges, and descriptions.
