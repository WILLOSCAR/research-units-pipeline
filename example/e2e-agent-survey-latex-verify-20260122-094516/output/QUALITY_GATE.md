# Quality gate log

- Append-only report sink for strict-mode unit checks (PASS/FAIL + next actions).
- When a unit is BLOCKED due to quality gate, read the latest entry here.

---

# Quality gate report

- Timestamp: `2026-01-22T09:45:29`
- Unit: `U001`
- Skill: `workspace-init`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:45:29`
- Unit: `U002`
- Skill: `pipeline-router`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:08`
- Unit: `U010`
- Skill: `literature-engineer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:08`
- Unit: `U020`
- Skill: `dedupe-rank`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:08`
- Unit: `U030`
- Skill: `taxonomy-builder`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:09`
- Unit: `U040`
- Skill: `outline-builder`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:09`
- Unit: `U050`
- Skill: `section-mapper`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:09`
- Unit: `U051`
- Skill: `outline-refiner`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:09`
- Unit: `U052`
- Skill: `pipeline-router`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:09`
- Unit: `U058`
- Skill: `pdf-text-extractor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:10`
- Unit: `U060`
- Skill: `paper-notes`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T09:46:10`
- Unit: `U075`
- Skill: `subsection-briefs`

## Status

- FAIL

## Issues

- `subsection_briefs_not_refined`: `outline/subsection_briefs.jsonl` exists but is not marked refined. After you manually refine briefs (especially unique tension/thesis), create `outline/subsection_briefs.refined.ok`.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/subsection-briefs/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U075` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U075 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-22T09:59:46`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- FAIL

## Issues

- `subsection_briefs_not_refined`: `outline/subsection_briefs.jsonl` exists but is not marked refined. After you manually refine briefs (especially unique tension/thesis), create `outline/subsection_briefs.refined.ok`.
- `chapter_briefs_not_refined`: `outline/chapter_briefs.jsonl` exists but is not marked refined. After you manually refine chapter throughlines (avoid generic glue), create `outline/chapter_briefs.refined.ok`.
- `evidence_drafts_not_refined`: `outline/evidence_drafts.jsonl` exists but is not marked refined. After you confirm packs are complete (no `blocking_missing`) and subsection-specific, create `outline/evidence_drafts.refined.ok`.
- `anchor_sheet_not_refined`: `outline/anchor_sheet.jsonl` exists but is not marked refined. After you verify anchors are subsection-specific and cite-backed, create `outline/anchor_sheet.refined.ok`.
- `writer_context_packs_not_refined`: `outline/writer_context_packs.jsonl` exists but is not marked refined. After you spot-check packs for scope/citation constraints and anti-template guidance, create `outline/writer_context_packs.refined.ok`.
- `evidence_bindings_not_refined`: `outline/evidence_bindings.jsonl` exists but is not marked refined. After you verify `binding_gaps` / `tag mix` are subsection-specific, create `outline/evidence_bindings.refined.ok`.
- `sections_missing_files`: Missing per-section files under `sections/` (e.g., sections/S3_1.md, sections/S3_2.md, sections/S4_1.md, sections/S4_2.md, sections/S5_1.md, sections/S5_2.md, sections/S6_1.md, sections/S6_2.md).

## Next action

- Write per-unit prose files under `sections/` (small, verifiable units):
  - `sections/abstract.md` (`## Abstract`), `sections/discussion.md`, `sections/conclusion.md`.
  - `sections/S<section_id>.md` for H2 sections without H3 (body only).
  - `sections/S<sub_id>.md` for each H3 (body only; no headings).
- Each H3 file should have >=3 unique citations and avoid ellipsis/TODO/template boilerplate.
- Keep H3 citations subsection-first: cite keys mapped in `outline/evidence_bindings.jsonl` for that H3; limited reuse from sibling H3s in the same H2 chapter is allowed; avoid cross-chapter “free cite”.
- After files exist, run `writer-selfloop` to enforce draft-profile depth/scope and to generate an actionable fix plan (`output/WRITER_SELFLOOP_TODO.md`).
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/subsection-writer/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U100` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U100 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-22T10:23:09`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- FAIL

## Issues

- `subsection_briefs_not_refined`: `outline/subsection_briefs.jsonl` exists but is not marked refined. After you manually refine briefs (especially unique tension/thesis), create `outline/subsection_briefs.refined.ok`.
- `chapter_briefs_not_refined`: `outline/chapter_briefs.jsonl` exists but is not marked refined. After you manually refine chapter throughlines (avoid generic glue), create `outline/chapter_briefs.refined.ok`.
- `evidence_drafts_not_refined`: `outline/evidence_drafts.jsonl` exists but is not marked refined. After you confirm packs are complete (no `blocking_missing`) and subsection-specific, create `outline/evidence_drafts.refined.ok`.
- `anchor_sheet_not_refined`: `outline/anchor_sheet.jsonl` exists but is not marked refined. After you verify anchors are subsection-specific and cite-backed, create `outline/anchor_sheet.refined.ok`.
- `writer_context_packs_not_refined`: `outline/writer_context_packs.jsonl` exists but is not marked refined. After you spot-check packs for scope/citation constraints and anti-template guidance, create `outline/writer_context_packs.refined.ok`.
- `evidence_bindings_not_refined`: `outline/evidence_bindings.jsonl` exists but is not marked refined. After you verify `binding_gaps` / `tag mix` are subsection-specific, create `outline/evidence_bindings.refined.ok`.

## Next action

- Write per-unit prose files under `sections/` (small, verifiable units):
  - `sections/abstract.md` (`## Abstract`), `sections/discussion.md`, `sections/conclusion.md`.
  - `sections/S<section_id>.md` for H2 sections without H3 (body only).
  - `sections/S<sub_id>.md` for each H3 (body only; no headings).
- Each H3 file should have >=3 unique citations and avoid ellipsis/TODO/template boilerplate.
- Keep H3 citations subsection-first: cite keys mapped in `outline/evidence_bindings.jsonl` for that H3; limited reuse from sibling H3s in the same H2 chapter is allowed; avoid cross-chapter “free cite”.
- After files exist, run `writer-selfloop` to enforce draft-profile depth/scope and to generate an actionable fix plan (`output/WRITER_SELFLOOP_TODO.md`).
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/subsection-writer/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U100` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U100 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-22T10:24:37`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-22T10:24:37`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_too_short`: `sections/S3_1.md` looks too short (4822 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_too_short`: `sections/S3_2.md` looks too short (4871 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_too_short`: `sections/S4_1.md` looks too short (4898 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 1; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_too_short`: `sections/S4_2.md` looks too short (4777 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_too_short`: `sections/S5_1.md` looks too short (4882 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_too_short`: `sections/S5_2.md` looks too short (4936 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S5_2.md` lacks explicit contrast phrasing (need >= 1; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_too_short`: `sections/S6_1.md` looks too short (4731 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S6_1.md` lacks explicit contrast phrasing (need >= 1; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_too_short`: `sections/S6_2.md` looks too short (4815 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S6_2.md` lacks explicit contrast phrasing (need >= 1; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

## Next action

- Open `output/WRITER_SELFLOOP_TODO.md` and fix only the failing `sections/*.md` files listed there (do not rewrite everything).
- Keep citations in-scope (per `outline/evidence_bindings.jsonl` / writer packs) and avoid narration templates (`This subsection ...`, `Next, we ...`).
- Rerun the `writer-selfloop` script until the report shows `- Status: PASS`, then proceed to the next unit.
- If the failures point to thin evidence (missing anchors/comparisons/limitations), loop upstream: `paper-notes` → `evidence-binder` → `evidence-draft` → `anchor-sheet` → `writer-context-pack`.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/writer-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1005` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1005 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-22T10:32:45`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- FAIL

## Issues

- `missing_transitions`: `outline/transitions.md` does not exist.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/transition-weaver/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U098` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U098 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-22T10:33:52`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- FAIL

## Issues

- `transitions_too_short`: `outline/transitions.md` looks too short (bullets=4); generate more subsection transitions.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/transition-weaver/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U098` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U098 --status DONE --note "LLM refined"`).
