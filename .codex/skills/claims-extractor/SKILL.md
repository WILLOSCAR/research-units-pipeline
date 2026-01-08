---
name: claims-extractor
description: |
  Extract key claims, contributions, and assumptions from a paper/manuscript into `output/CLAIMS.md` with traceability to source locations.
  **Trigger**: claims extractor, extract claims, contributions, assumptions, peer review, 审稿, 主张提取.
  **Use when**: 审稿/评审或 evidence audit，需要把主张列表落盘并可追溯到原文位置（section/page/quote）。
  **Skip if**: 没有可用的稿件/全文（例如缺少 `output/PAPER.md` 或等价文本）。
  **Network**: none.
  **Guardrail**: 每条 claim 必须带可定位的 source pointer；区分 empirical vs conceptual claims。
---

# Skill: claims-extractor

## Goal

- Produce a claim list that can be audited for evidence.

## Inputs

- A paper text file (e.g., `output/PAPER.md`) or provided manuscript content

## Outputs

- `output/CLAIMS.md`

## Procedure (MUST FOLLOW)
Uses: `output/PAPER.md`.


1. List main claims and contributions.
2. For each claim, include a pointer to the source (section/page/quote).
3. Separate empirical claims vs. conceptual claims.

## Acceptance criteria (MUST CHECK)

- [ ] Each claim includes a traceable source pointer.
