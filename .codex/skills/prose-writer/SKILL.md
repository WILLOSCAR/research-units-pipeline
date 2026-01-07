---
name: prose-writer
description: Write `output/DRAFT.md` or `output/SNAPSHOT.md` from approved outline and evidence, using only verified citation keys from `citations/ref.bib`. Use only after required HUMAN sign-off is recorded in `DECISIONS.md` (unless writing is explicitly bullets-only).
---

# Prose Writer

Write a survey draft (or short snapshot) that reads like a real paper: motivation → structure → cross-paper synthesis → limitations/future work → conclusion.

This skill is where “human-like iteration” matters: outline + evidence first, then section writing, then a polish pass to remove repetition.

## Non-negotiables

- **No prose without approval**: check `DECISIONS.md` (survey default requires `Approve C2`).
- **No invented citations**: only use keys that exist in `citations/ref.bib`.

## Inputs

- `outline/outline.yml`
- Optional: `outline/claim_evidence_matrix.md`
- Optional: `outline/tables.md`, `outline/timeline.md`, `outline/figures.md` (from `survey-visuals`)
- Optional: `papers/core_set.csv`
- `citations/ref.bib` (when using citations)
- `DECISIONS.md` (must authorize prose when required)

## Outputs

- `output/DRAFT.md` and/or `output/SNAPSHOT.md`

## Decision: snapshot vs draft

- Snapshot: bullets-first, ~1 page, “what exists + what’s missing”.
- Draft: section-by-section prose with tables/timeline and subsection-specific synthesis.

## Workflow (heuristic)

1. Gate check: confirm writing is approved in `DECISIONS.md`.
   - If not approved, write a short request (what you plan to write, and what evidence you will rely on) and stop.
2. Pre-write pass (2–5 minutes):
   - skim `outline/claim_evidence_matrix.md` + `outline/tables.md` + `outline/timeline.md`
   - decide the “through-line” of the paper (what story ties sections together)
3. Write the draft in a paper-like order:
   - Abstract
   - Introduction (motivation, scope, contributions, positioning vs prior surveys)
   - Background / problem setup (only as needed)
   - Body sections per outline with **cross-paper comparisons**
   - Timeline/Evolution section (milestones + citations)
   - Open Problems & Future Directions (make them subsection-specific and concrete)
   - Conclusion
4. Synthesis style (avoid per-paper lists):
   - compare 2–4 approaches in one paragraph
   - name the trade-off and the evidence (benchmarks, settings, failure modes)
   - mention limitations with citations when possible
   - **rule of thumb**: each subsection should contain at least one paragraph that cites ≥2 works (so it reads like synthesis, not a paper-by-paper list)
5. Tables/figures:
   - include ≥2 tables directly in the draft (the tables can be copied from `outline/tables.md`)
   - reference figure specs (you can include them as “Figure X (spec)” until real figures are drawn)
6. Polish pass:
   - remove repeated template phrasing (“本小节聚焦…”, identical open-problems lines, identical takeaways)
   - ensure each subsection has at least one citation
   - ensure language/style is consistent (choose Chinese-first or English-first)

## Quality checklist

- [ ] Writing respects checkpoint policy (no prose without approval).
- [ ] All citation keys referenced exist in `citations/ref.bib`.
- [ ] Draft includes: Introduction, Timeline/Evolution, Open Problems & Future Directions, Conclusion.
- [ ] Draft includes ≥2 comparison tables and avoids repeated boilerplate across subsections.
- [ ] Most subsections include at least one “multi-citation” paragraph (≥2 citations in the same paragraph) to enforce cross-paper comparisons.

## Helper script (optional)

Scaffold + guardrails only:
- Run `python .codex/skills/prose-writer/scripts/run.py --help` first.
- Then: `python .codex/skills/prose-writer/scripts/run.py --workspace <workspace_dir>`

The helper only scaffolds if missing and never overwrites an existing refined draft; when `outline/mapping.tsv` + `papers/paper_notes.jsonl` exist it will also include starter mapped paper IDs + citation keys to make section writing less “empty template”. In `pipeline.py --strict` the quality gate will block template-y drafts.
