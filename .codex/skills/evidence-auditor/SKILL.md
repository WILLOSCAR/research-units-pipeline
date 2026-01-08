---
name: evidence-auditor
description: |
  Audit the evidence supporting each claim and write gaps/concerns into `output/MISSING_EVIDENCE.md`.
  **Trigger**: evidence audit, missing evidence, unsupported claims, 审稿证据审计, 证据缺口.
  **Use when**: peer review 流程中，需要逐条检查 claim 的证据链、缺 baseline、评测薄弱点。
  **Skip if**: 缺少 claims 输入（例如还没有 `output/CLAIMS.md`）。
  **Network**: none.
  **Guardrail**: 只写“缺口/风险/下一步验证”，不要替作者补写论述或引入新主张。
---

# Skill: evidence-auditor

## Goal

- Make evidence gaps explicit and actionable.

## Inputs

- `output/CLAIMS.md`

## Outputs

- `output/MISSING_EVIDENCE.md`

## Procedure (MUST FOLLOW)
Uses: `output/CLAIMS.md`.


1. For each claim, check what evidence is provided (experiments, proofs, citations).
2. Record missing baselines, unclear datasets, missing ablations, or overclaims.
3. Suggest minimal fixes (what evidence to add).

## Acceptance criteria (MUST CHECK)

- [ ] Every claim has either supporting evidence notes or a gap item.
