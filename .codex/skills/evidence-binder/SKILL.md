---
name: evidence-binder
description: |
  Bind addressable evidence IDs from `papers/evidence_bank.jsonl` to each subsection (H3), producing `outline/evidence_bindings.jsonl`.
  **Trigger**: evidence binder, evidence plan, section->evidence mapping, 证据绑定, evidence_id.
  **Use when**: `papers/evidence_bank.jsonl` exists and you want writer/auditor to use section-scoped evidence items (WebWeaver-style memory bank).
  **Skip if**: you are not doing evidence-first section-by-section writing.
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent evidence; only select from the existing evidence bank.
---

# Evidence Binder (NO PROSE)

Goal: convert a paper-level pool into a **section-addressable evidence plan**.

This skill is the bridge from “Evidence Bank” → “Writer”: the writer should only use evidence IDs bound to the current subsection.

## Inputs

Required:
- `outline/subsection_briefs.jsonl`
- `outline/mapping.tsv`
- `papers/evidence_bank.jsonl`

Optional:
- `citations/ref.bib` (to validate cite keys)

## Outputs

- `outline/evidence_bindings.jsonl` (1 line per subsection)
- `outline/evidence_binding_report.md` (summary; bullets + small tables)

## Freeze policy

- If `outline/evidence_bindings.refined.ok` exists, the script will not overwrite `outline/evidence_bindings.jsonl`.

## Script

- `python .codex/skills/evidence-binder/scripts/run.py --workspace <ws>`
