---
name: pipeline-auditor
description: |
  Audit/regression checks for the evidence-first survey pipeline: citation health, per-section coverage, placeholder leakage, and template repetition.
  **Trigger**: auditor, audit, regression test, quality report, 审计, 回归测试.
  **Use when**: `output/DRAFT.md` exists and you want a deterministic PASS/FAIL report before LaTeX/PDF.
  **Skip if**: you are still changing retrieval/outline/evidence packs heavily (audit later).
  **Network**: none.
  **Guardrail**: do not change content; only analyze and report.
---

# Pipeline Auditor (draft audit + regression)

Goal: catch the failures your writer/polisher can accidentally produce:
- placeholder leakage (`...`, `…`, TODO)
- repeated boilerplate sentences
- missing/undefined/duplicate citations
- subsection coverage drift (H3 headings not matching outline)

Outputs are deterministic and auditable.

## Inputs

- `output/DRAFT.md`
- `outline/outline.yml`
- `outline/evidence_bindings.jsonl` (recommended)
- `citations/ref.bib`

## Outputs

- `output/AUDIT_REPORT.md`

## Script

- `python .codex/skills/pipeline-auditor/scripts/run.py --workspace <ws>`
