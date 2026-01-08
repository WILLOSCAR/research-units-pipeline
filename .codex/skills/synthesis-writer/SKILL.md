---
name: synthesis-writer
description: |
  Synthesize evidence into a structured narrative (`output/SYNTHESIS.md`) grounded in `papers/extraction_table.csv`, including limitations and bias considerations.
  **Trigger**: synthesis, evidence synthesis, systematic review writing, 综合写作, SYNTHESIS.md.
  **Use when**: systematic review 完成 screening+extraction（含 bias 评估）后进入写作阶段（C4）。
  **Skip if**: 还没有 `papers/extraction_table.csv`（或 protocol/screening 尚未完成）。
  **Network**: none.
  **Guardrail**: 以 extraction table 为证据底座；明确局限性与偏倚；不要在无数据支撑时扩写结论。
---

# Skill: synthesis-writer

## Goal

- Produce an evidence-grounded synthesis with explicit limitations.

## Inputs

- `papers/extraction_table.csv`
- Optional: `DECISIONS.md` (writing approval)

## Outputs

- `output/SYNTHESIS.md`

## Procedure (MUST FOLLOW)
Uses: `papers/extraction_table.csv`.


1. If the pipeline requires approval to write prose, check `DECISIONS.md`; otherwise stop and request sign-off.
2. Group findings by themes and compare across studies.
3. Include a limitations/bias subsection.

## Acceptance criteria (MUST CHECK)

- [ ] Each major claim cites specific rows/papers from the extraction table.
