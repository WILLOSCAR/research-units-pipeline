---
name: draft-polisher
description: |
  Audit-style editing pass for `output/DRAFT.md`: remove template boilerplate, improve coherence, and enforce citation anchoring.
  **Trigger**: polish draft, de-template, coherence pass, remove boilerplate, 润色, 去套话, 去重复, 统一术语.
  **Use when**: a first-pass draft exists but reads like scaffolding (repetition/ellipsis/template phrases) or needs a coherence pass before global review/LaTeX.
  **Skip if**: the draft already reads human-grade and passes quality gates; or prose is not approved in `DECISIONS.md`.
  **Network**: none.
  **Guardrail**: do not add/remove/invent citation keys; do not move citations across subsections; do not change claims beyond what existing citations support.
---

# Draft Polisher (Audit-style editing)

Goal: turn a first-pass draft into readable survey prose **without breaking the evidence contract**.

This is Stage D (local polish): de-template + coherence + terminology + redundancy pruning.

## Inputs

- `output/DRAFT.md`
- Optional context (read-only):
  - `outline/outline.yml`
  - `outline/subsection_briefs.jsonl`
  - `outline/evidence_drafts.jsonl`
  - `citations/ref.bib`

## Output

- `output/DRAFT.md` (in-place refinement)

## Non-negotiables (hard rules)

1) **Citation keys are immutable**
- Do not add new `[@BibKey]` keys.
- Do not delete citation markers.

2) **Citation anchoring is immutable**
- Do not move citations across `###` subsections.
- If you must restructure across subsections, stop and push the change upstream (outline/briefs/evidence), then regenerate.

3) **No evidence inflation**
- If a sentence sounds stronger than the evidence level (abstract-only), rewrite it into a qualified statement.

4) **No pipeline voice**
- Remove scaffolding phrases like:
  - “We use the following working claim …”
  - “The main axes we track are …”
  - “abstracts are treated as verification targets …”
  - “Scope and definitions / Design space / Evaluation practice …”

## Three passes (recommended)

### Pass 1 — Subsection polish (structure + de-template)

Role split:
- **Editor**: rewrite sentences for clarity and flow.
- **Skeptic**: deletes any generic/template sentence.

Targets:
- Each H3 reads like: tension → contrast → evidence → limitation.
- Remove repeated “disclaimer paragraphs”; keep evidence-level note in one place.

### Pass 2 — Terminology normalization

Role split:
- **Taxonomist**: chooses canonical terms and synonym policy.
- **Integrator**: applies consistent replacements across the draft.

Targets:
- One concept = one name across sections.
- Headings, tables, and prose use the same canonical terms.

### Pass 3 — Redundancy pruning (global repetition)

Role split:
- **Compressor**: collapses repeated boilerplate.
- **Narrative keeper**: ensures removing repetition does not break the argument chain.

Targets:
- Cross-section repeated intros/outros are removed.
- Only subsection-specific content remains inside subsections.

## Helper script (gate wrapper + anchoring baseline)

This skill includes a deterministic wrapper script so it can be used as a verifiable unit in `UNITS.csv`.

- `python .codex/skills/draft-polisher/scripts/run.py --workspace <ws>`

Behavior:
- On first run, it writes a citation anchoring baseline: `output/citation_anchors.prepolish.jsonl`.
- On subsequent runs, it blocks if citations drift across H3 subsections.

### Resetting the baseline (only if intentional)

If you intentionally need to restructure and accept citation drift:
- Delete `output/citation_anchors.prepolish.jsonl`, then rerun the polisher to regenerate a new baseline.

## Acceptance checklist

- [ ] No `TODO/TBD/FIXME/(placeholder)`.
- [ ] No `…` or `...` truncation.
- [ ] No repeated boilerplate sentence across many subsections.
- [ ] Citation anchoring passes (no cross-subsection drift).
- [ ] Each H3 has at least one cross-paper synthesis paragraph (>=2 citations).
