---
name: extraction-form
description: Extract full-text data into a structured table (`papers/extraction_table.csv`) using a defined extraction schema from the protocol. Use after screening to prepare evidence for synthesis.
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

1. Derive extraction fields from the protocol.
2. For each included paper, fill extraction fields and capture key outcomes/limitations.
3. Keep provenance (paper id/url) for each row.

## Acceptance criteria (MUST CHECK)

- [ ] All included papers have extraction rows.

