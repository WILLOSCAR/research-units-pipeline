---
name: keyword-expansion
description: Expand and refine search keywords (synonyms, acronyms, exclusions) and update `queries.md` accordingly. Use when retrieval coverage is poor or the topic has many aliases.
---

# Skill: keyword-expansion

## Goal

- Improve recall/precision of `queries.md` without drifting scope.

## Inputs

- `queries.md`
- Optional: `DECISIONS.md` scope notes

## Outputs

- Updated `queries.md`

## Procedure (MUST FOLLOW)

1. Extract the current topic scope and exclusions.
2. Propose keyword expansions (synonyms, related terms, acronyms) and add explicit exclusions for common false positives.
3. Update `queries.md` with a clear “why” note for each change.

## Acceptance criteria (MUST CHECK)

- [ ] `queries.md` contains updated keywords and excludes.
- [ ] Changes do not contradict `DECISIONS.md` scope constraints.

