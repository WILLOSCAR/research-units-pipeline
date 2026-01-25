# Quality gate log

- Append-only report sink for strict-mode unit checks (PASS/FAIL + next actions).
- When a unit is BLOCKED due to quality gate, read the latest entry here.

---

# Quality gate report

- Timestamp: `2026-01-25T16:50:20`
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

- Timestamp: `2026-01-25T16:50:21`
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

- Timestamp: `2026-01-25T16:50:37`
- Unit: `U010`
- Skill: `literature-engineer`

## Status

- FAIL

## Issues

- `raw_too_small`: `papers/papers_raw.jsonl` has 209 records; target >= 1200 for survey-quality runs (expand queries/imports/snowballing; raise `max_results` and add more buckets).

## Next action

- Provide multiple offline exports under `papers/imports/` (different queries/routes) to reach a large candidate pool (survey target: >=200).
- Ensure most records contain stable IDs (`arxiv_id`/`doi`) and non-empty `url`; prefer arXiv/OpenReview/ACL exports with IDs.
- If network is available, rerun with `--online` (and optionally `--snowball`) to expand coverage via arXiv API and citation graph.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/literature-engineer/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U010` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U010 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-25T16:56:20`
- Unit: `U010`
- Skill: `literature-engineer`

## Status

- FAIL

## Issues

- `raw_too_small`: `papers/papers_raw.jsonl` has 209 records; target >= 1200 for survey-quality runs (expand queries/imports/snowballing; raise `max_results` and add more buckets).

## Next action

- Provide multiple offline exports under `papers/imports/` (different queries/routes) to reach a large candidate pool (survey target: >=200).
- Ensure most records contain stable IDs (`arxiv_id`/`doi`) and non-empty `url`; prefer arXiv/OpenReview/ACL exports with IDs.
- If network is available, rerun with `--online` (and optionally `--snowball`) to expand coverage via arXiv API and citation graph.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/literature-engineer/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U010` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U010 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-25T17:00:41`
- Unit: `U010`
- Skill: `literature-engineer`

## Status

- FAIL

## Issues

- `raw_too_small`: `papers/papers_raw.jsonl` has 207 records; target >= 1200 for survey-quality runs (expand queries/imports/snowballing; raise `max_results` and add more buckets).

## Next action

- Provide multiple offline exports under `papers/imports/` (different queries/routes) to reach a large candidate pool (survey target: >=200).
- Ensure most records contain stable IDs (`arxiv_id`/`doi`) and non-empty `url`; prefer arXiv/OpenReview/ACL exports with IDs.
- If network is available, rerun with `--online` (and optionally `--snowball`) to expand coverage via arXiv API and citation graph.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/literature-engineer/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U010` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U010 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-25T17:05:28`
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

- Timestamp: `2026-01-25T17:05:36`
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

- Timestamp: `2026-01-25T17:05:36`
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

- Timestamp: `2026-01-25T17:05:37`
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

- Timestamp: `2026-01-25T17:05:37`
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

- Timestamp: `2026-01-25T17:05:37`
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

- Timestamp: `2026-01-25T17:05:37`
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

- Timestamp: `2026-01-25T17:05:37`
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

- Timestamp: `2026-01-25T17:05:38`
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

- Timestamp: `2026-01-25T17:05:38`
- Unit: `U075`
- Skill: `subsection-briefs`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:05:38`
- Unit: `U076`
- Skill: `chapter-briefs`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:05:38`
- Unit: `U090`
- Skill: `citation-verifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:05:38`
- Unit: `U091`
- Skill: `evidence-binder`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:06:54`
- Unit: `U092`
- Skill: `evidence-draft`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:07:00`
- Unit: `U0925`
- Skill: `table-schema`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:07:00`
- Unit: `U093`
- Skill: `anchor-sheet`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:07:00`
- Unit: `U0926`
- Skill: `table-filler`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:09:18`
- Unit: `U0927`
- Skill: `appendix-table-writer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:09:25`
- Unit: `U0935`
- Skill: `schema-normalizer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:09:25`
- Unit: `U099`
- Skill: `writer-context-pack`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:09:25`
- Unit: `U0995`
- Skill: `evidence-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:09:25`
- Unit: `U094`
- Skill: `claim-matrix-rewriter`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T17:16:22`
- Unit: `U100`
- Skill: `subsection-writer`

## Status

- FAIL

## Issues

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

- Timestamp: `2026-01-25T17:27:48`
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

- Timestamp: `2026-01-25T17:27:48`
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

- Timestamp: `2026-01-25T17:27:58`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_missing_contrast`: `sections/S3_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S3_2.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S3_2.md` cites keys not mapped to subsection 3.2 (or its chapter 3) (e.g., Zhang2025Security); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S4_1.md` cites keys not mapped to subsection 4.1 (or its chapter 4) (e.g., Hu2025Survey, Zhang2025Generalizability, Zhang2025Security); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_too_short`: `sections/S4_2.md` looks too short (4958 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S4_2.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S4_2.md` cites keys not mapped to subsection 4.2 (or its chapter 4) (e.g., Kim2025Bridging, Zhang2025Generalizability, Zhang2025Security, Zou2025Based); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_missing_contrast`: `sections/S5_1.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S5_1.md` cites keys not mapped to subsection 5.1 (or its chapter 5) (e.g., Gasmi2025Bridging, Hu2025Evaluating, Ji2024Testing, Wu2025Agentic, Zhang2025Generalizability, Zou2025Based); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_missing_contrast`: `sections/S5_2.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S5_2.md` cites keys not mapped to subsection 5.2 (or its chapter 5) (e.g., Hu2025Evaluating, Ji2024Testing, Kim2025Bridging, Silva2025Agents, Zhang2025Generalizability); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_too_short`: `sections/S6_1.md` looks too short (4989 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S6_1.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S6_1.md` cites keys not mapped to subsection 6.1 (or its chapter 6) (e.g., Du2025Memr, Hu2025Evaluating, Hu2025Survey, Ji2024Testing); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_short`: `sections/S6_2.md` looks too short (4922 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S6_2.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

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

- Timestamp: `2026-01-25T17:39:44`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_sparse_citations`: `sections/S3_1.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_missing_contrast`: `sections/S3_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_h3_missing_contrast`: `sections/S3_2.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S3_2.md` cites keys not mapped to subsection 3.2 (or its chapter 3) (e.g., Zhang2025Security); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_missing_contrast`: `sections/S4_1.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S4_1.md` cites keys not mapped to subsection 4.1 (or its chapter 4) (e.g., Hu2025Survey, Zhang2025Generalizability, Zhang2025Security); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_too_short`: `sections/S4_2.md` looks too short (4958 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S4_2.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S4_2.md` cites keys not mapped to subsection 4.2 (or its chapter 4) (e.g., Kim2025Bridging, Zhang2025Generalizability, Zhang2025Security, Zou2025Based); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_missing_contrast`: `sections/S5_1.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S5_1.md` cites keys not mapped to subsection 5.1 (or its chapter 5) (e.g., Gasmi2025Bridging, Hu2025Evaluating, Ji2024Testing, Wu2025Agentic, Zhang2025Generalizability, Zou2025Based); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_missing_contrast`: `sections/S5_2.md` lacks explicit contrast phrasing (need >= 2; found 1). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S5_2.md` cites keys not mapped to subsection 5.2 (or its chapter 5) (e.g., Hu2025Evaluating, Ji2024Testing, Kim2025Bridging, Silva2025Agents, Zhang2025Generalizability); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_too_short`: `sections/S6_1.md` looks too short (4989 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S6_1.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.
- `sections_cites_outside_mapping`: `sections/S6_1.md` cites keys not mapped to subsection 6.1 (or its chapter 6) (e.g., Du2025Memr, Hu2025Evaluating, Hu2025Survey, Ji2024Testing); keep citations subsection- or chapter-scoped (or fix mapping/bindings).
- `sections_h3_sparse_citations`: `sections/S6_2.md` has <12 unique citations (11); each H3 should be evidence-first for survey-quality runs.
- `sections_h3_too_short`: `sections/S6_2.md` looks too short (4922 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.
- `sections_h3_missing_contrast`: `sections/S6_2.md` lacks explicit contrast phrasing (need >= 2; found 0). Use whereas/in contrast/相比/不同于 to compare routes, not only summarize.

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

- Timestamp: `2026-01-25T17:56:47`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_too_short`: `sections/S6_1.md` looks too short (4999 chars after removing citations; min=5000). Expand with concrete comparisons + evaluation details + synthesis + limitations from the evidence pack.

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

- Timestamp: `2026-01-25T18:00:56`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:05:36`
- Unit: `U102`
- Skill: `section-logic-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:05:43`
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

- Timestamp: `2026-01-25T18:07:00`
- Unit: `U098`
- Skill: `transition-weaver`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:07:10`
- Unit: `U101`
- Skill: `section-merger`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:07:10`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- FAIL

## Issues

- `post_merge_slash_list_axes`: slash-list axis markers (source: draft)

## Next action

- Open `output/POST_MERGE_VOICE_REPORT.md` and fix the earliest responsible artifact it points to.
- If the report says `source: transitions`: rewrite `outline/transitions.md` as content-bearing argument bridges (no planner talk, no A/B/C slash labels), then rerun `section-merger` and this gate.
- If the report says `source: draft`: route to `writer-selfloop` / `subsection-polisher` / `draft-polisher` for the flagged section, then rerun `section-merger` and this gate.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/post-merge-voice-gate/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U103` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U103 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-25T18:12:22`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- FAIL

## Issues

- `post_merge_slash_list_axes`: slash-list axis markers (source: draft)

## Next action

- Open `output/POST_MERGE_VOICE_REPORT.md` and fix the earliest responsible artifact it points to.
- If the report says `source: transitions`: rewrite `outline/transitions.md` as content-bearing argument bridges (no planner talk, no A/B/C slash labels), then rerun `section-merger` and this gate.
- If the report says `source: draft`: route to `writer-selfloop` / `subsection-polisher` / `draft-polisher` for the flagged section, then rerun `section-merger` and this gate.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/post-merge-voice-gate/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U103` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U103 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-25T18:14:09`
- Unit: `U103`
- Skill: `post-merge-voice-gate`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:14:18`
- Unit: `U104`
- Skill: `citation-diversifier`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:14:18`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:14:18`
- Unit: `U105`
- Skill: `draft-polisher`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:14:19`
- Unit: `U108`
- Skill: `global-reviewer`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:47:09`
- Unit: `U109`
- Skill: `pipeline-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:47:10`
- Unit: `U110`
- Skill: `latex-scaffold`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:47:16`
- Unit: `U120`
- Skill: `latex-compile-qa`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:47:16`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T18:47:16`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T19:31:04`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- FAIL

## Issues

- `missing_outputs`: Missing outputs: output/ARGUMENT_SELFLOOP_TODO.md, output/SECTION_ARGUMENT_SUMMARIES.jsonl, output/ARGUMENT_SKELETON.md

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/argument-selfloop/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1025` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1025 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-01-25T19:39:27`
- Unit: `U1025`
- Skill: `argument-selfloop`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T19:39:27`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.

---

# Quality gate report

- Timestamp: `2026-01-25T19:39:27`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.
