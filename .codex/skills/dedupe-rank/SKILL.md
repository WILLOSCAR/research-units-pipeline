---
name: dedupe-rank
description: Dedupe and rank a raw paper set (`papers/papers_raw.jsonl`) to produce a deduplicated set and a curated core set (`papers/papers_dedup.jsonl`, `papers/core_set.csv`). Use after retrieval to prepare the core paper list for taxonomy/outline building.
---

# Dedupe + Rank

Turn a broad retrieved set into a smaller **core set** for taxonomy/outline building.

This is a deterministic “curation” step: it should be stable and repeatable.

## Input

- `papers/papers_raw.jsonl`

## Outputs

- `papers/papers_dedup.jsonl`
- `papers/core_set.csv`

## Workflow (high level)

1. Dedupe by normalized `(title, year)` and keep the richest metadata per duplicate cluster.
2. Rank by relevance/recency signals (and optionally pin known classics for certain topics).
3. Write `papers/core_set.csv` with stable `paper_id` values and useful metadata columns (`arxiv_id`, `pdf_url`, categories).

## Quality checklist

- [ ] `papers/papers_dedup.jsonl` exists and is valid JSONL.
- [ ] `papers/core_set.csv` exists and has a header row.

## Script

- `python .codex/skills/dedupe-rank/scripts/run.py --workspace <workspace_dir> --core-size 50`
