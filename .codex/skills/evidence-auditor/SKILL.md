---
name: evidence-auditor
description: Audit the evidence supporting each claim and write gaps/concerns into `output/MISSING_EVIDENCE.md`. Use when reviewing a paper to identify unsupported claims, missing baselines, or weak evaluation.
---

# Skill: evidence-auditor

## Goal

- Make evidence gaps explicit and actionable.

## Inputs

- `output/CLAIMS.md`

## Outputs

- `output/MISSING_EVIDENCE.md`

## Procedure (MUST FOLLOW)

1. For each claim, check what evidence is provided (experiments, proofs, citations).
2. Record missing baselines, unclear datasets, missing ablations, or overclaims.
3. Suggest minimal fixes (what evidence to add).

## Acceptance criteria (MUST CHECK)

- [ ] Every claim has either supporting evidence notes or a gap item.

