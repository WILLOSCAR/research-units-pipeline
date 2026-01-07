---
name: synthesis-writer
description: Synthesize evidence into a structured narrative (`output/SYNTHESIS.md`) grounded in the extraction table, including limitations and bias considerations. Use after protocol+screening+extraction checkpoints allow writing.
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

1. If the pipeline requires approval to write prose, check `DECISIONS.md`; otherwise stop and request sign-off.
2. Group findings by themes and compare across studies.
3. Include a limitations/bias subsection.

## Acceptance criteria (MUST CHECK)

- [ ] Each major claim cites specific rows/papers from the extraction table.
