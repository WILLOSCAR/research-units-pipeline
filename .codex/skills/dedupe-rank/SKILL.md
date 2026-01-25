---
name: dedupe-rank
description: |
  Dedupe and rank a raw paper set (`papers/papers_raw.jsonl`) to produce `papers/papers_dedup.jsonl` and `papers/core_set.csv`.
  **Trigger**: dedupe, rank, core set, 去重, 排序, 精选论文, 核心集合.
  **Use when**: 检索后需要把广覆盖集合收敛成可管理的 core set（用于 taxonomy/outline/mapping）。
  **Skip if**: 已经有人手工整理了稳定的 `papers/core_set.csv`（无需再次 churn）。
  **Network**: none.
  **Guardrail**: 偏 deterministic；输出应可重复（稳定 paper_id、字段规范）。
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
2. Rank by relevance/recency signals (and optionally pin known classics for certain topics). For LLM-agent topics, also ensure a small quota of prior surveys/reviews is present to support a paper-like Related Work section.
3. Write `papers/core_set.csv` with stable `paper_id` values and useful metadata columns (`arxiv_id`, `pdf_url`, categories).

## Quality checklist

- [ ] `papers/papers_dedup.jsonl` exists and is valid JSONL.
- [ ] `papers/core_set.csv` exists and has a header row.

## Script

### Quick Start

- `python .codex/skills/dedupe-rank/scripts/run.py --help`
- `python .codex/skills/dedupe-rank/scripts/run.py --workspace <workspace_dir> --core-size 300`

### All Options

- `--core-size <n>`: target size for `papers/core_set.csv`
- `queries.md` also supports `core_size` / `core_set_size` / `dedupe_core_size` (overrides default when present)

### Examples

- Smaller core set for fast iteration (non-A150++):
  - `python .codex/skills/dedupe-rank/scripts/run.py --workspace <ws> --core-size 25`

### Notes

- This step may annotate `papers/core_set.csv:reason` with tags such as `pinned_classic` and `prior_survey` (deterministic, topic-aware guards for survey writing).
- Systematic-review default: if the active pipeline is `systematic-review` and `core_size` is not specified, the script keeps the full deduped pool in `papers/core_set.csv` (so screening does not silently drop candidates).
- This step is deterministic; reruns should be stable for the same inputs.

## Troubleshooting

### Common Issues

#### Issue: `papers/core_set.csv` is too small / empty

**Symptom**:
- Core set has very few rows.

**Causes**:
- Input `papers/papers_raw.jsonl` is small, or many rows are missing required fields.

**Solutions**:
- Broaden retrieval (or provide a richer offline export) and rerun.
- Lower `--core-size` only if you intentionally want a small core set.

#### Issue: Duplicates still appear after dedupe

**Symptom**:
- Near-identical titles remain.

**Causes**:
- Title normalization is defeated by noisy exports.

**Solutions**:
- Clean title fields in the export (strip prefixes/suffixes, fix encoding) and rerun.

### Recovery Checklist

- [ ] `papers/papers_raw.jsonl` lines contain `title/year/url`.
- [ ] `papers/core_set.csv` has stable `paper_id` values.
