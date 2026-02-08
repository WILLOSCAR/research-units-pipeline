---
name: paragraph-curator
description: |
  Structured paragraph curation for C5: **select -> evaluate -> subset -> fuse**, so drafts converge instead of only expanding.
  **Trigger**: paragraph curator, curation, select evaluate fuse, paragraph selection, 选段, 评价, 融合, 收敛, 去冗余.
  **Use when**: you are in C5, `sections/*.md` exist, and the writing loop drifts toward 'longer by accumulation' (repetition, redundant paragraphs, weak synthesis).
  **Skip if**: evidence packs are thin / `evidence-selfloop` is BLOCKED; or you are pre-C2 (NO PROSE).
  **Network**: none.
  **Guardrail**: do not invent facts; do not add/remove citation keys; do not move citations across subsections; keep section-level claims consistent with `output/ARGUMENT_SKELETON.md# Consistency Contract`.
---

# Paragraph Curator (select -> evaluate -> subset -> fuse)

Purpose: turn “keep rewriting and getting longer” into a controlled convergence step.

This skill adds a decision layer between “draft paragraphs” and “polish voice”:
- keep the best paragraphs
- merge redundant ones
- rewrite for clearer argument moves
- expand only when coverage is missing (using existing evidence cards)

This is a content-structure pass (not a style pass). Run `style-harmonizer` and `opener-variator` after curation.

## Inputs

Required:
- `sections/` (especially H3 bodies: `sections/S<sub_id>.md`)
- `outline/writer_context_packs.jsonl` (what each H3 must cover + allowed citations)
- `output/ARGUMENT_SKELETON.md` (single source of truth for terminology + premises)

Recommended:
- `output/SECTION_ARGUMENT_SUMMARIES.jsonl` (paragraph moves + outputs)
- `output/SECTION_LOGIC_REPORT.md` (paragraph linkage risks)
- `output/WRITER_SELFLOOP_TODO.md` (style smells / scope/citation warnings)

## Outputs

- Updated `sections/*.md` (same filenames; body-only; no headings)
- `output/PARAGRAPH_CURATION_REPORT.md` (short; PASS/FAIL + what changed)
- Create `sections/paragraphs_curated.refined.ok` when done (empty file; pipeline contract signal)

## What this skill optimizes (rubric)

You are not trying to “shorten”. You are trying to increase information density while keeping the section verifiable.

Score each paragraph on a simple 0-2 rubric:

| Criterion | 0 (bad) | 1 (ok) | 2 (good) |
|---|---|---|---|
| Coverage | does not match any required axis/card | matches one axis, thin | directly executes a must-use card/comparison |
| Novelty | repeats nearby content | partially redundant | adds a distinct comparison/insight |
| Move clarity | unclear what it does | move exists, weak output | clear move + reusable output |
| Consistency | premise/term drift vs skeleton | minor mismatch | fully aligned with Consistency Contract |
| Citation hygiene | uncited when it should be; cite-dump vibe | acceptable | citations are local and anchored (not just tail) |
| Fusion readiness | cannot merge; tangled | mergeable with edits | clean unit that can be fused or kept |

Decision labels:
- `KEEP`: keep mostly as-is
- `REWRITE`: keep content, rewrite for clearer move/output
- `FUSE`: merge with neighbor(s) and rewrite into one stronger paragraph
- `REPLACE`: keep the slot, but rewrite using existing evidence cards (when coverage is missing)

## Paragraph budget (profile-aware)

Default per-H3 target:
- `draft_profile=survey`: 10-12 paragraphs
- `draft_profile=deep`: 11-13 paragraphs

If you exceed the budget, do not delete content blindly. Prefer `FUSE` (merge redundancy) and make the fused paragraph denser.

## Must-have coverage checklist (per H3)

Each H3 must contain at least:
- 1x `Definition/Setup` (only if this H3 introduces a new term/protocol field)
- 2x concrete `Contrast` paragraphs (A-vs-B comparisons; not just “many papers do...”)
- 1x `Evaluation anchor` paragraph (task + metric + constraint/budget/tool access; cite-backed)
- 1x cross-paper `Synthesis` paragraph (what generalizes, what does not; cite-backed)
- 1x `Boundary/Failure` paragraph (limitations; threats to validity; cite-backed when possible)
- 1x `Local conclusion` (a reusable takeaway used downstream)

If any item is missing, use `REPLACE` to write that paragraph from the writer context pack (do not invent new facts).

## Workflow (minimal)

1) Pick the target set
- Start with the H3 bodies listed in `output/SECTION_LOGIC_REPORT.md`, plus any H3 flagged in `output/WRITER_SELFLOOP_TODO.md` as repetitive/template-y, plus any H3 that keeps growing across edits.
- Work file-by-file: each target is a concrete `sections/S<sub_id>.md`.

2) Build a paragraph inventory (scratch only; do not paste into the paper)
- If `output/SECTION_ARGUMENT_SUMMARIES.jsonl` exists, use its per-paragraph `moves`/`output` as the first draft of your inventory, then reconcile with the actual text.
For each paragraph, write one line:
- `P<i> :: move(s) -> output (1 sentence) :: citations (keys)`

3) Apply the rubric and label each paragraph
- Mark `KEEP/REWRITE/FUSE/REPLACE`.
- If two adjacent paragraphs repeat the same axis, `FUSE`.
- For any paragraph you plan to change (`REWRITE`/`REPLACE`/`FUSE`), draft 2-3 candidate rewrites in parallel (different angles: contrast-first / protocol-first / synthesis-first).
  - Score candidates quickly with the rubric; keep one winner (or fuse two if they cover complementary axes).
  - Keep citation keys unchanged while sampling; you are choosing surface form + structure, not changing the evidence set.

4) Construct the curated set
- Use `outline/writer_context_packs.jsonl` to enforce must-have coverage (paragraph_plan/must_use/comparison_cards/limitation_hooks) without inventing new content.
- Enforce the must-have coverage checklist.
- Enforce the paragraph budget by fusing redundancy rather than deleting substance.

5) Fuse + rewrite (keep citation keys fixed)
Rules that keep the pipeline stable:
- Do not add/remove citation keys; when fusing, carry citations forward and re-anchor them to the right sentence.
- Do not move citations across subsections.
- Avoid adjacent citation blocks (e.g., `[@a] [@b]`) and duplicate keys in one block (e.g., `[@a; @a]`).
- When fusing, it is often faster to write two fused candidates (one contrast-heavy, one synthesis-heavy) and pick the better one.

6) Write the report + marker
- `output/PARAGRAPH_CURATION_REPORT.md` should be short and actionable:
  - `- Status: PASS|FAIL`
  - per H3: paragraph count before/after; what was fused; any remaining gaps
  - (minimal) how many candidates you tried for the main rewrites (e.g., 2-3), so future passes can see whether this was a real selection step
- Create `sections/paragraphs_curated.refined.ok`.

## Routing rules

- If you cannot fill a missing must-have paragraph without new evidence: stop and route upstream (`evidence-selfloop` / C3-C4). Do not pad.
- If you feel forced to change a definition or evaluation premise: update `output/ARGUMENT_SKELETON.md# Consistency Contract` first, then rerun `argument-selfloop`.
- If the only issue is surface cadence/openers: do not overwork curation; run `style-harmonizer` / `opener-variator`.

## Done checklist

- [ ] Each targeted H3 stays within its paragraph budget (survey 10-12; deep 11-13) without losing required moves.
- [ ] Redundant paragraphs are fused into denser, clearer ones (not just deleted).
- [ ] No citation keys were added/removed; citation shape is reader-facing (no adjacent blocks, no dup keys).
- [ ] `output/PARAGRAPH_CURATION_REPORT.md` exists and is understandable.
- [ ] `sections/paragraphs_curated.refined.ok` exists.
