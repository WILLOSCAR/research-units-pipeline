---
name: concept-graph
description: Build a concept graph (nodes and prerequisite edges) from a tutorial spec, saving it as YAML under `outline/concept_graph.yml`. Use when structuring a tutorial before prose writing.
---

# Skill: concept-graph

## Goal

- Make concept dependencies explicit to drive module ordering.

## Inputs

- `output/TUTORIAL_SPEC.md`

## Outputs

- `outline/concept_graph.yml`

## Procedure (MUST FOLLOW)

1. Extract key concepts (≥10 nodes).
2. Add prerequisite edges and short node descriptions.
3. Keep it structural (no prose explanations).

## Acceptance criteria (MUST CHECK)

- [ ] Concept graph has nodes, edges, and descriptions.

