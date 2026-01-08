---
name: rubric-writer
description: |
  Write a rubric-based peer review report (`output/REVIEW.md`) using extracted claims and evidence gaps (novelty/soundness/clarity/impact).
  **Trigger**: rubric review, referee report, peer review write-up, 审稿报告, REVIEW.md.
  **Use when**: peer-review pipeline 的最后阶段（C3），已有 `output/CLAIMS.md` + `output/MISSING_EVIDENCE.md`（以及可选 novelty matrix）。
  **Skip if**: 上游产物未就绪（claims/evidence gaps 缺失）或你不打算输出完整审稿报告。
  **Network**: none.
  **Guardrail**: 给可执行建议（actionable feedback），并覆盖 novelty/soundness/clarity/impact；避免泛泛而谈。
---

# Skill: rubric-writer

## Goal

- Produce a complete referee report with actionable items.

## Inputs

- `output/CLAIMS.md`
- `output/MISSING_EVIDENCE.md`
- Optional: `output/NOVELTY_MATRIX.md`

## Outputs

- `output/REVIEW.md`

## Procedure (MUST FOLLOW)
Uses: `output/CLAIMS.md`, `output/MISSING_EVIDENCE.md`, `output/NOVELTY_MATRIX.md`.


1. Summarize contributions in 3–6 bullets.
2. Evaluate: novelty, soundness, clarity, impact.
3. List major concerns and minor comments.
4. Provide recommendation (accept/reject/weak accept/weak reject) with rationale.

## Acceptance criteria (MUST CHECK)

- [ ] Review includes rubric sections and actionable suggestions.
