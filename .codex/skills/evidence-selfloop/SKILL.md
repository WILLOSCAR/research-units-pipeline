---
name: evidence-selfloop
description: |
  Evidence self-loop for surveys: read evidence bindings + evidence packs, then write an actionable upstream TODO plan (which stage/skill to fix) before writing more prose.
  Writes `output/EVIDENCE_SELFLOOP_TODO.md`.
  **Trigger**: evidence self-loop, evidence loop, evidence gaps, binding gaps, blocking_missing, 证据自循环, 证据缺口回路.
  **Use when**: C4 outputs exist (`outline/evidence_bindings.jsonl`, `outline/evidence_drafts.jsonl`) but writing looks hollow or C5 is BLOCKED due to thin evidence.
  **Skip if**: you are still pre-C3 (no notes/evidence bank yet), or you want to draft anyway and accept a lower evidence bar.
  **Network**: none.
  **Guardrail**: analysis-only; do not edit evidence/writing artifacts; do not invent facts/citations; only write the TODO report.
---

# Evidence Self-loop (C3/C4 fix → rebind → redraft)

Purpose: make the evidence-first pipeline converge **without writing filler prose**.

This skill reads the *intermediate evidence artifacts* (briefs/bindings/packs) and produces an actionable TODO list that answers:

- Which subsections are under-supported?
- Is the problem mapping/coverage (C2) or evidence extraction (C3) or binding/planning (C4)?
- Which skill(s) should be rerun, in what order, to unblock high-quality writing?

## Inputs

- `outline/subsection_briefs.jsonl`
- `outline/evidence_bindings.jsonl` (expects `binding_gaps` / `binding_rationale` if available)
- `outline/evidence_drafts.jsonl` (expects `blocking_missing`, comparisons, eval protocol, limitations)
- Optional (improves routing):
  - `outline/evidence_binding_report.md`
  - `outline/anchor_sheet.jsonl`
  - `papers/paper_notes.jsonl`
  - `papers/fulltext_index.jsonl`
  - `queries.md`

## Outputs

- `output/EVIDENCE_SELFLOOP_TODO.md` (report-class; always written)

## Self-loop contract (what “fixing evidence” means)

- Prefer fixing **upstream evidence**, not writing around gaps.
- If an evidence pack has `blocking_missing`, treat it as a STOP signal: strengthen notes/fulltext/mapping, then regenerate packs.
- If bindings show `binding_gaps`, treat it as a ROUTING signal: either enrich the evidence bank for the mapped papers, expand mapping coverage, or adjust `required_evidence_fields` if unrealistic.

Recommended rerun chain (minimal):

- If C3 evidence is thin: `pdf-text-extractor` → `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`
- If C2 coverage is weak: `section-mapper` → `outline-refiner` → (then rerun C3/C4 evidence skills)

## Workflow (analysis-only)

1) Read `queries.md` (if present)
- Use it only as a soft config hint (evidence_mode / draft_profile); do not override the artifact contract.

2) Read `outline/subsection_briefs.jsonl`
- For each `sub_id`, capture `axes` + `required_evidence_fields` (what evidence types this subsection expects).

3) Read `outline/evidence_bindings.jsonl`
- For each `sub_id`, surface `binding_rationale` and `binding_gaps` (what the binder could/could not cover from the evidence bank).

4) (Optional) Read `outline/evidence_binding_report.md`
- Use it as a human-readable summary; treat it as a view of `outline/evidence_bindings.jsonl`, not a separate truth source.

5) Read `outline/evidence_drafts.jsonl`
- Surface `blocking_missing` (STOP signals), and check for missing comparisons / eval protocol / limitations that would force hollow writing.

6) (Optional) Read `outline/anchor_sheet.jsonl`
- Check whether each subsection has at least a few citation-backed anchors (numbers / evaluation / limitations).

7) (Optional) Read `papers/paper_notes.jsonl` and `papers/fulltext_index.jsonl`
- Use these to route fixes: if evidence is abstract-only and missing eval tokens, prefer enriching notes/fulltext before drafting prose.

## What the report contains

- Summary counts: subsections with `blocking_missing`, with `binding_gaps`, and common failure reasons.
- Per-subsection TODO: the smallest upstream fix path (skills + artifacts) to make the subsection writeable.

## Script

### Quick Start

- `python .codex/skills/evidence-selfloop/scripts/run.py --workspace workspaces/<ws>`

### All Options

- `--workspace <dir>`
- `--unit-id <U###>` (optional)
- `--inputs <semicolon-separated>` (optional override)
- `--outputs <semicolon-separated>` (optional override; default writes `output/EVIDENCE_SELFLOOP_TODO.md`)
- `--checkpoint <C#>` (optional)

### Examples

- Generate an evidence TODO list after C4 packs are generated:
  - `python .codex/skills/evidence-selfloop/scripts/run.py --workspace workspaces/<ws>`
