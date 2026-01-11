---
name: section-merger
description: |
  Deterministically merge per-section files under `sections/` (plus evidence-first visuals under `outline/`) into `output/DRAFT.md`, preserving outline order.
  **Trigger**: merge sections, merge draft, combine section files, sections/ -> output/DRAFT.md, 合并小节, 拼接草稿.
  **Use when**: you have per-unit prose files under `sections/` and want a single `output/DRAFT.md` for polishing/review/LaTeX.
  **Skip if**: section files are missing or still contain scaffolding markers (fix `subsection-writer` first).
  **Network**: none.
  **Guardrail**: deterministic merge only (no new facts/citations); preserve section order from `outline/outline.yml`.
---

# Section Merger

Goal: assemble a single `output/DRAFT.md` from:
- `sections/*.md` (per-section/per-subsection prose)
- `outline/tables.md`, `outline/timeline.md`, `outline/figures.md`
- `outline/transitions.md` (inserted as transition paragraphs)

This skill is **deterministic**: it does not rewrite content or invent prose; it only merges and inserts already-generated transition sentences.

## Outputs

- `output/DRAFT.md`
- `output/MERGE_REPORT.md`

## Quick Start

- `python .codex/skills/section-merger/scripts/run.py --workspace workspaces/<ws>`
