---
name: screening-manager
description: |
  Manage title/abstract screening and record decisions into `papers/screening_log.csv` according to an approved protocol.
  **Trigger**: screening, title/abstract screening, inclusion/exclusion, screening_log.csv, 文献筛选, 纳入排除.
  **Use when**: systematic review 的 screening 阶段（C2），protocol 已锁定并通过 HUMAN 审批。
  **Skip if**: 还没有 `output/PROTOCOL.md`（或 protocol 未通过签字）。
  **Network**: none.
  **Guardrail**: 每条记录包含决策与理由；保持可审计（不要把“未读/不确定”当作纳入）。
---

# Skill: screening-manager

## Goal

- Produce an auditable screening log.

## Inputs

- `output/PROTOCOL.md`
- A candidate paper list (format chosen per workspace)

## Outputs

- `papers/screening_log.csv`

## Procedure (MUST FOLLOW)
Uses: `output/PROTOCOL.md`.


1. Read inclusion/exclusion criteria from protocol.
2. For each candidate paper, record: decision (include/exclude), reason, reviewer (HUMAN/CODEX), timestamp.
3. If full metadata is missing, mark as `needs_info`.

## Acceptance criteria (MUST CHECK)

- [ ] Screening log has decisions and reasons for all candidates.
