---
name: subsection-writer
description: |
  Write section/subsection prose into per-unit files under `sections/`, so each unit can be QA’d independently before merging into `output/DRAFT.md`.
  **Trigger**: subsection writer, per-section writing, split sections, sections/, 分小节写, 按章节拆分写作.
  **Use when**: `Approve C2` is recorded and evidence packs exist; you want evidence-first drafting without a monolithic one-shot draft.
  **Skip if**: `DECISIONS.md` approval is missing, or `outline/evidence_drafts.jsonl` is incomplete/scaffolded.
  **Network**: none.
  **Guardrail**: do not invent facts/citations; no ellipsis/TODO/placeholder leakage; H3 body files must not contain headings.
---

# Subsection Writer (Per-section drafting)

Goal: write prose in **small, independently verifiable units** so we can catch:
- placeholder leakage (…/TODO)
- template boilerplate
- subsection→citation drift

This skill produces multiple files under `sections/`, plus a machine-readable manifest.

## Outputs

Required:
- `sections/sections_manifest.jsonl`
- `sections/abstract.md`
- `sections/open_problems.md`
- `sections/conclusion.md`

Per-outline units:
- `sections/S<section_id>.md` for H2-only sections (e.g., `S1.md`)
- `sections/S<sub_id>.md` for each H3 (e.g., `2.1` → `S2_1.md`)

Optional:
- `sections/evidence_note.md` (recommended when evidence is abstract-only)

## File contract (H3)

For `sections/S2_1.md` (H3 body files):

- **Body only**: MUST NOT contain headings (`#`, `##`, `###`).
- **Evidence-first**: MUST include citations `[@BibKey]` (survey default: `>=3` unique citations per H3).
- **Grad-paragraph shape** (avoid “summary-only”): across the file, include:
  - explicit **contrast** phrasing (e.g., whereas / in contrast / 相比 / 不同于)
  - an **evaluation anchor** (benchmark/dataset/metric/protocol/评测)
  - at least one explicit **limitation / provisional** sentence (limited/unclear/受限/待验证)
- **No pipeline voice**: do not leak scaffold phrases like “working claim”, “axes we track”, “verification targets”.

## Roles (recommended two-pass)

### Role A: Argument Planner

For each H3 subsection, extract from evidence packs:
- 1 subsection thesis (subsection-specific)
- 2 contrasts (A vs B) grounded in mapped citations
- 1 evaluation anchor sentence
- 1 limitation / verification sentence

If you can’t do this without guessing, stop and push the gap upstream (`paper-notes` / `evidence-draft`).

### Role B: Writer

Write 2–3 paragraphs that realize the plan:
- paragraph 1: tension/RQ + first contrast
- paragraph 2: second contrast + evaluation anchor
- paragraph 3 (optional): limitation + bridge to next subsection

Use `grad-paragraph` as a micro-skill for each paragraph.

### Role C: Skeptic (quick pass)

Delete or rewrite any sentence that is:
- copy-pastable into other subsections
- purely generic (“depends on metrics”, “important considerations include…”) without concrete nouns

## Inputs

- `outline/outline.yml`
- `outline/subsection_briefs.jsonl`
- `outline/evidence_drafts.jsonl`
- `outline/evidence_bindings.jsonl` (allowed citations per H3)
- `citations/ref.bib`
- `DECISIONS.md`

## Quick Start

- `python .codex/skills/subsection-writer/scripts/run.py --workspace workspaces/<ws>`

## Troubleshooting

### Issue: blocked by section-file quality gates

**Symptom**:
- `output/QUALITY_GATE.md` reports missing eval anchor / missing contrast / too few paragraphs.

**Cause**:
- The subsection reads like a title/abstract summary, not a survey comparison.

**Fix**:
- Rebuild the subsection using `grad-paragraph` (tension → contrast → eval anchor → limitation).
- If evidence packs don’t contain concrete comparison snippets, strengthen upstream evidence.

### Issue: citations outside mapped subset

**Symptom**:
- “cites keys not mapped to subsection …”

**Fix**:
- Either (a) replace with mapped citations, or (b) fix `outline/mapping.tsv` + rerun `evidence-binder`.
