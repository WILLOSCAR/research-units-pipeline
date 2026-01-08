---
name: bias-assessor
description: |
  Add bias/risk-of-bias assessment fields to an extraction table and populate them consistently.
  **Trigger**: bias, risk-of-bias, RoB, evidence quality, 偏倚评估, 证据质量.
  **Use when**: systematic review 已生成 `papers/extraction_table.csv`，需要在 synthesis 前补齐偏倚/质量字段。
  **Skip if**: 不是 systematic review，或还没有 `papers/extraction_table.csv`。
  **Network**: none.
  **Guardrail**: 使用简单可复核刻度（low/unclear/high）+ 简短 notes；保持字段一致性。
---

# Skill: bias-assessor

## Goal

- Make evidence quality explicit in the extraction table.

## Inputs

- `papers/extraction_table.csv`

## Outputs

- Updated `papers/extraction_table.csv`

## Procedure (MUST FOLLOW)

1. Add a small set of bias fields (selection, measurement, confounding, reporting).
2. Fill with a simple scale (low/unclear/high) plus short notes.

## Acceptance criteria (MUST CHECK)

- [ ] Bias fields exist and are populated for included papers.
