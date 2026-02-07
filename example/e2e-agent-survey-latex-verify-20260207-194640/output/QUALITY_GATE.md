# Quality gate log

- Append-only report sink for strict-mode unit checks (PASS/FAIL + next actions).
- When a unit is BLOCKED due to quality gate, read the latest entry here.

---

# Quality gate report

- Timestamp: `2026-02-07T19:46:51`
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

- Timestamp: `2026-02-07T19:46:51`
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

- Timestamp: `2026-02-07T19:51:31`
- Unit: `U010`
- Skill: `literature-engineer`

## Status

- FAIL

## Issues

- `empty_raw`: No records found in `papers/papers_raw.jsonl`.

## Next action

- Provide multiple offline exports under `papers/imports/` (different queries/routes) to reach a large candidate pool (survey target: >=200).
- Ensure most records contain stable IDs (`arxiv_id`/`doi`) and non-empty `url`; prefer arXiv/OpenReview/ACL exports with IDs.
- If network is available, rerun with `--online` (and optionally `--snowball`) to expand coverage via arXiv API and citation graph.
- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/literature-engineer/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U010` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U010 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-02-07T19:52:57`
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

- Timestamp: `2026-02-07T19:53:11`
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

- Timestamp: `2026-02-07T19:53:12`
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

- Timestamp: `2026-02-07T19:53:12`
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

- Timestamp: `2026-02-07T19:53:12`
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

- Timestamp: `2026-02-07T19:53:12`
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

- Timestamp: `2026-02-07T19:53:12`
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

- Timestamp: `2026-02-07T19:55:32`
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

- Timestamp: `2026-02-07T19:55:33`
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

- Timestamp: `2026-02-07T19:55:33`
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

- Timestamp: `2026-02-07T19:55:33`
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

- Timestamp: `2026-02-07T19:55:33`
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

- Timestamp: `2026-02-07T19:55:33`
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

- Timestamp: `2026-02-07T19:55:34`
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

- Timestamp: `2026-02-07T19:55:34`
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

- Timestamp: `2026-02-07T19:55:34`
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

- Timestamp: `2026-02-07T19:55:34`
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

- Timestamp: `2026-02-07T20:01:24`
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

- Timestamp: `2026-02-07T20:01:31`
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

- Timestamp: `2026-02-07T20:01:31`
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

- Timestamp: `2026-02-07T20:01:31`
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

- Timestamp: `2026-02-07T20:01:31`
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

- Timestamp: `2026-02-07T20:27:56`
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

- Timestamp: `2026-02-07T20:27:56`
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

- Timestamp: `2026-02-07T20:28:04`
- Unit: `U1005`
- Skill: `writer-selfloop`

## Status

- FAIL

## Issues

- `sections_h3_citation_dump_paragraphs`: `sections/S3_1.md` has 7 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S3_2.md` has 6 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S4_1.md` has 6 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S4_2.md` has 7 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S5_1.md` has 8 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S5_2.md` has 6 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S6_1.md` has 8 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.
- `sections_h3_citation_dump_paragraphs`: `sections/S6_2.md` has 6 paragraph(s) where citations appear only as a trailing dump (e.g., ending with `[@a; @b; @c]`). Embed citations into the sentence they support (system name + claim), rather than tagging the paragraph at the end.

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

- Timestamp: `2026-02-07T20:30:23`
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

- Timestamp: `2026-02-07T20:44:07`
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

- Timestamp: `2026-02-07T20:44:07`
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

- Timestamp: `2026-02-07T20:52:36`
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

- Timestamp: `2026-02-07T20:52:36`
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

- Timestamp: `2026-02-07T20:53:29`
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

- Timestamp: `2026-02-07T20:53:29`
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

- Timestamp: `2026-02-07T20:53:29`
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

- Timestamp: `2026-02-07T20:53:29`
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

- Timestamp: `2026-02-07T20:53:29`
- Unit: `U1045`
- Skill: `citation-injector`

## Status

- FAIL

## Issues

- `citation_injection_failed`: `output/CITATION_INJECTION_REPORT.md` is not PASS; add more in-scope unused citations (or expand C1/C2 mapping), then rerun citation injection.

## Next action

- Treat the current outputs as a starting point (often a scaffold).
- Follow `.codex/skills/citation-injector/SKILL.md` to refine the required artifacts until the issues above no longer apply.
- Then mark `U1045` as `DONE` in `UNITS.csv` (or run `python scripts/pipeline.py mark --workspace <ws> --unit-id U1045 --status DONE --note "LLM refined"`).

---

# Quality gate report

- Timestamp: `2026-02-07T20:58:26`
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

- Timestamp: `2026-02-07T20:58:26`
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

- Timestamp: `2026-02-07T20:58:26`
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

- Timestamp: `2026-02-07T20:58:27`
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

- Timestamp: `2026-02-07T20:58:27`
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

- Timestamp: `2026-02-07T20:58:34`
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

- Timestamp: `2026-02-07T20:58:34`
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

- Timestamp: `2026-02-07T20:58:34`
- Unit: `U130`
- Skill: `artifact-contract-auditor`

## Status

- PASS

## Issues

- (none)

## Next action

- Proceed to the next unit.
