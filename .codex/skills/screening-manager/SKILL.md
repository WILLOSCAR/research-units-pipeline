---
name: screening-manager
description: Manage title/abstract screening and record decisions into `papers/screening_log.csv` according to an approved protocol. Use when implementing the screening stage of a systematic review pipeline.
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

1. Read inclusion/exclusion criteria from protocol.
2. For each candidate paper, record: decision (include/exclude), reason, reviewer (HUMAN/CODEX), timestamp.
3. If full metadata is missing, mark as `needs_info`.

## Acceptance criteria (MUST CHECK)

- [ ] Screening log has decisions and reasons for all candidates.

