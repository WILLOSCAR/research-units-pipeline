---
name: protocol-writer
description: |
  Write a systematic review protocol into `output/PROTOCOL.md` (databases, queries, inclusion/exclusion, time window, extraction fields).
  **Trigger**: protocol, PRISMA, systematic review, inclusion/exclusion, 检索式, 纳入排除.
  **Use when**: systematic review pipeline 的起点（C1），需要先锁定 protocol 再开始 screening/extraction。
  **Skip if**: 不是做 systematic review（或 protocol 已经锁定且不允许修改）。
  **Network**: none.
  **Guardrail**: protocol 必须包含可执行的检索与筛选规则；需要 HUMAN 签字后才能进入 screening。
---

# Skill: protocol-writer

## Goal

- Lock the review protocol before screening/extraction.

## Inputs

- User constraints / `STATUS.md`

## Outputs

- `output/PROTOCOL.md`

## Procedure (MUST FOLLOW)
Uses: `STATUS.md`.


1. Define research questions and scope.
2. Define databases/sources and concrete search strings.
3. Define inclusion/exclusion criteria and time window.
4. Define screening procedure and extraction fields.

## Acceptance criteria (MUST CHECK)

- [ ] Protocol contains query, criteria, workflow, extraction fields.
