---
name: survey-visuals
description: Draft non-prose visuals artifacts (tables, timeline, figure specs) for a survey, grounded in notes/claims and using verified citation keys from `citations/ref.bib`.
---

# Survey Visuals (NO PROSE)

Create non-prose “visual thinking” artifacts that make the actual writing stage less template-y:

- comparison tables (method + evaluation)
- timeline / evolution bullets
- figure specs (what to draw, why it matters, what papers support it)

## Inputs

- `outline/outline.yml`
- `outline/claim_evidence_matrix.md`
- `papers/paper_notes.jsonl`
- `citations/ref.bib`

## Outputs

- `outline/tables.md`
- `outline/timeline.md`
- `outline/figures.md`

## Workflow (heuristic)

1. Read the outline + claim–evidence matrix and pick the **comparison axes** that recur across sections:
   - control loop / planner-executor split
   - tool interface & orchestration
   - memory / retrieval / reflection
   - environments & benchmarks
   - safety / security / alignment surfaces
2. Tables (`outline/tables.md`):
   - Write **≥2 Markdown tables** with real entries and citations.
   - Prefer one “method matrix” and one “evaluation/benchmark matrix”.
3. Timeline (`outline/timeline.md`):
   - Write year → key milestone bullets (aim for breadth and citations).
4. Figures (`outline/figures.md`):
   - Write 2–4 figure specs that a human could draw:
     - purpose (“what insight this figure communicates”)
     - required elements (boxes/arrows/axes)
     - what papers support each element (cite keys)
5. Use only citation keys present in `citations/ref.bib`.

## Quality checklist

- [ ] No `TODO` and no `<!-- SCAFFOLD ... -->` markers remain in the outputs.
- [ ] `outline/tables.md` contains ≥2 Markdown tables with real content and citations.
- [ ] `outline/timeline.md` contains ≥8 year bullets and each bullet has ≥1 citation marker `[@...]`.
- [ ] `outline/figures.md` contains ≥2 figure specs and each mentions at least one supporting citation.

## Helper script (optional)

Bootstrap scaffold only:
- Run `python .codex/skills/survey-visuals/scripts/run.py --help` first.
- Then: `python .codex/skills/survey-visuals/scripts/run.py --workspace <workspace_dir>`

The helper only creates scaffolds if missing and never overwrites non-placeholder artifacts. When `papers/paper_notes.jsonl` is present it will prefill candidate rows/bullets with real `paper_id` + `bibkey` citation markers to make refinement faster. In `pipeline.py --strict` it will be blocked until you replace scaffold markers and `TODO`s with real content.
