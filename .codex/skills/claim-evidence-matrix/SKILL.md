---
name: claim-evidence-matrix
description: Build a section-by-section claim–evidence matrix (`outline/claim_evidence_matrix.md`) using the outline and paper notes, ensuring each subsection has at least one claim backed by multiple sources. Use before any prose writing to make evidence explicit.
---

# Claim–Evidence Matrix

Make the survey’s claims explicit and auditable **before** writing prose.

This should stay **bullets-only** (NO PROSE). The goal is to make later writing *easy* and to prevent “template prose” from sneaking in.

## Inputs

- `outline/outline.yml`
- `papers/paper_notes.jsonl`
- Optional: `outline/mapping.tsv`

## Output

- `outline/claim_evidence_matrix.md`

## Workflow (heuristic)

1. For each subsection, write 1–3 claims that are:
   - specific (mechanism / assumption / empirical finding)
   - falsifiable (“X reduces tool errors under Y evaluation”, not “X is important”)
2. For each claim, list ≥2 evidence sources:
   - prefer different styles of evidence (method paper + eval/benchmark paper, or two competing approaches)
3. Keep it tight: claim → evidence → (optional) caveat/limitations.
4. If evidence is weak or only abstract-level, say so explicitly (don’t overclaim).
5. If `bibkey` exists in `papers/paper_notes.jsonl`, include `[@BibKey]` next to evidence items to make later prose/LaTeX conversion smoother.

## Quality checklist

- [ ] Every subsection has ≥1 claim.
- [ ] Each claim lists ≥2 evidence sources (or an explicit exception).
- [ ] Claims are not copy-pasted templates (avoid “围绕…总结…” boilerplate).

## Helper script (optional)

Bootstrap scaffold only:
- Run `python .codex/skills/claim-evidence-matrix/scripts/run.py --help` first.
- Then: `python .codex/skills/claim-evidence-matrix/scripts/run.py --workspace <workspace_dir>`

The helper produces a generic scaffold. In `pipeline.py --strict` it will be blocked if scaffold markers remain or if claims look templated.
