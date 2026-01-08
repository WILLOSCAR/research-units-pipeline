---
name: extraction-form
description: |
  Extract study data into a structured table (`papers/extraction_table.csv`) using the protocol’s extraction schema.
  **Trigger**: extraction form, extraction table, data extraction, 信息提取, 提取表.
  **Use when**: systematic review 在 screening 后进入 extraction（C3），需要把纳入论文按字段落到 CSV 以支持后续 synthesis。
  **Skip if**: 还没有 `papers/screening_log.csv` 或 protocol 未锁定。
  **Network**: none.
  **Guardrail**: 严格按 schema 填字段；不要在此阶段写 narrative synthesis（那是 `synthesis-writer`）。
---

# Skill: extraction-form

## Goal

- Create a consistent extraction table for synthesis.

## Inputs

- `papers/screening_log.csv`
- `output/PROTOCOL.md`

## Outputs

- `papers/extraction_table.csv`

## Procedure (MUST FOLLOW)
Uses: `papers/screening_log.csv`, `output/PROTOCOL.md`.


1. Derive extraction fields from the protocol.
2. For each included paper, fill extraction fields and capture key outcomes/limitations.
3. Keep provenance (paper id/url) for each row.

## Acceptance criteria (MUST CHECK)

- [ ] All included papers have extraction rows.
