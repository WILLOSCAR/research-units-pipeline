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

Goal: convert a paper-level pool into a **subsection-addressable evidence plan**.

This skill is the bridge from “Evidence Bank” → “Writer”: the writer should only use evidence IDs bound to the current subsection.

## Inputs

- `outline/subsection_briefs.jsonl`
- `outline/mapping.tsv`
- `papers/evidence_bank.jsonl`
- Optional:
  - `citations/ref.bib` (to validate cite keys when evidence items carry citations)

## Outputs

- `outline/evidence_bindings.jsonl` (1 JSONL record per subsection)
- `outline/evidence_binding_report.md` (summary; bullets + small tables)

## Output format (`outline/evidence_bindings.jsonl`)

JSONL (one object per H3 subsection). Best-effort fields (keep deterministic):

- `sub_id`, `title`
- `paper_ids` (papers in-scope for this subsection, from `mapping.tsv`)
- `mapped_bibkeys` (bibkeys mapped to this subsection)
- `bibkeys` (a selected subset to encourage subsection-first citations)
- `evidence_ids` (selected evidence items from `papers/evidence_bank.jsonl`)
- `evidence_counts` (small summary by claim_type / evidence_level)

## Binding policy (how strict to be)

- Subsection-first by default: the writer should primarily cite `bibkeys` and use `evidence_ids` bound to this `sub_id`.
- Allow limited within-chapter reuse: citations from sibling H3s within the same H2 chapter may be reused for background/evaluation framing, but:
  - keep >=2 subsection-specific citations per H3 (avoid “free cite drift”)
  - avoid cross-chapter reuse unless the outline explicitly calls for it

## Workflow (NO PROSE)

1. Read `outline/subsection_briefs.jsonl` to understand each H3’s scope/rq/axes.
2. Read `outline/mapping.tsv` to know which papers belong to each subsection.
3. Read `papers/evidence_bank.jsonl` and select a subsection-scoped set of `evidence_id` items per H3.
4. If `citations/ref.bib` exists, sanity-check that any cite keys referenced by selected evidence items are defined.
5. Write `outline/evidence_bindings.jsonl` and `outline/evidence_binding_report.md`.

## Freeze policy

- If `outline/evidence_bindings.refined.ok` exists, the script will not overwrite `outline/evidence_bindings.jsonl`.

## Script

### Quick Start

- `python .codex/skills/evidence-binder/scripts/run.py --help`
- `python .codex/skills/evidence-binder/scripts/run.py --workspace workspaces/<ws>`

### All Options

- `--workspace <dir>`: workspace root
- `--unit-id <U###>`: unit id (optional; for logs)
- `--inputs <semicolon-separated>`: override inputs (rare; prefer defaults)
- `--outputs <semicolon-separated>`: override outputs (rare; prefer defaults)
- `--checkpoint <C#>`: checkpoint id (optional; for logs)

### Examples

- Bind evidence IDs after building the evidence bank:
  - Ensure `papers/evidence_bank.jsonl` exists.
  - Run: `python .codex/skills/evidence-binder/scripts/run.py --workspace workspaces/<ws>`

## Troubleshooting

### Issue: some subsections have too few evidence IDs

**Fix**:
- Strengthen `papers/evidence_bank.jsonl` via `paper-notes` (more extractable evidence items), or broaden the mapped paper set via `section-mapper` + rerun.
