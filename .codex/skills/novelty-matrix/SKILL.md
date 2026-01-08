---
name: novelty-matrix
description: |
  Create a novelty/prior-work matrix comparing the submission’s contributions against related work (overlaps vs deltas).
  **Trigger**: novelty matrix, prior-work matrix, overlap/delta, 相关工作对比, 新颖性矩阵.
  **Use when**: peer review 中评估 novelty/positioning，需要把贡献与相关工作逐项对齐并写出差异点证据。
  **Skip if**: 缺少 claims（先跑 `claims-extractor`）或你不打算做新颖性定位分析。
  **Network**: none (retrieval of additional related work is out-of-scope unless provided).
  **Guardrail**: 明确 overlap 与 delta；尽量给出可追溯证据来源（来自稿件/引用/作者陈述）。
---

# Skill: novelty-matrix

## Goal

- Provide a structured novelty assessment.

## Inputs

- `output/CLAIMS.md`
- Optional: provided related work list

## Outputs

- `output/NOVELTY_MATRIX.md` (recommended)

## Procedure (MUST FOLLOW)
Uses: `output/CLAIMS.md`.


1. List contributions/claims as rows.
2. List closest related works as columns.
3. Mark overlap and differentiation with short evidence notes.

## Acceptance criteria (MUST CHECK)

- [ ] Matrix identifies at least 5 related works or explains why unavailable.
