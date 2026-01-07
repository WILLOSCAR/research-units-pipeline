---
name: section-mapper
description: Map papers from the core set to each outline subsection and write `outline/mapping.tsv` with coverage tracking. Use when ensuring each subsection has enough supporting papers before writing.
---

# Section Mapper

Create a paper→subsection map that supports evidence building and later synthesis.

Good mapping is **diverse** (avoids reusing the same paper everywhere) and **explainable** (short semantic “why”, not just keyword overlap).

## When to use

- You have `outline/outline.yml` and a `papers/core_set.csv` and need coverage per subsection.
- You want to identify weak-signal subsections early (so you can adjust scope or add papers).

## Inputs

- `papers/core_set.csv`
- `outline/outline.yml`

## Outputs

- `outline/mapping.tsv`
- `outline/mapping_report.md` (diagnostics: reuse hotspots, weak-signal subsections)

## Workflow (heuristic)

1. Start from the outline subsections (each subsection should be “mappable”).
2. For each subsection, pick ~3–6 papers that are:
   - representative (canonical / frequently-cited)
   - complementary (different design choices, different eval setups)
   - not overly reused elsewhere unless truly foundational
3. Fill `why` with a short semantic rationale (one line is enough), e.g.:
   - mechanism: “decouples planner/executor; tool calling API”
   - evaluation: “interactive web tasks; strong tool error analysis”
   - safety: “agentic jailbreak surface; mitigation study”
4. After initial mapping, scan for:
   - subsections with <3 papers → either broaden, merge, or expand retrieval
   - a few papers mapped everywhere → diversify; reserve “foundational” papers for only the truly relevant parts

## Quality checklist

- [ ] `outline/mapping.tsv` exists and is non-empty.
- [ ] Most subsections have ≥3 mapped papers (or a clear exception noted in `why`).
- [ ] `why` is semantic (not just `matched_terms=...`).
- [ ] No single paper dominates unrelated subsections.

## Helper script (optional)

Bootstrap + diagnostics:
- Run `python .codex/skills/section-mapper/scripts/run.py --help` first.
- Then: `python .codex/skills/section-mapper/scripts/run.py --workspace <workspace_dir> --per-subsection 3`

This helper adds a global reuse penalty and writes `outline/mapping_report.md`. In `pipeline.py --strict` it may be blocked until you replace generic `why` rationales with semantic ones.
