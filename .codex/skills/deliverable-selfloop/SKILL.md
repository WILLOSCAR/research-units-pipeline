---
name: deliverable-selfloop
description: |
  Self-loop a deliverable until it is publishable by the pipeline standard: diagnose -> fix -> re-check, and write a PASS/FAIL report.
  **Trigger**: self loop, self-loop, polish deliverable, quality gate, fix-on-fail, 收敛, 自循环, 质量门.
  **Use when**: A pipeline has produced a reader-facing deliverable (`output/*.md`) and you want deterministic convergence to PASS.
  **Skip if**: You are still pre-approval for prose (e.g., C2 not approved) or the upstream evidence/structure artifacts are missing.
  **Network**: none.
  **Guardrail**: Do not invent papers/citations/results. Only use in-scope inputs already present in the workspace.
---

# Deliverable Self-Loop (fix-on-fail)

Goal: converge a pipeline deliverable to a stable, reader-facing quality bar.

This is a *generic* self-loop skill that supports multiple pipelines by switching rubrics based on the deliverable file.

## Inputs

Common (recommended):
- `UNITS.csv` (to confirm which deliverable this unit is responsible for)
- `PIPELINE.lock.md` (to confirm which pipeline is active)

One of the following deliverables:
- `output/SNAPSHOT.md`
- `output/TUTORIAL.md`
- `output/SYNTHESIS.md`
- `output/REVIEW.md`
- `output/IDEA_SHORTLIST.md`

Supporting contracts (depends on deliverable type):
- Snapshot: `outline/outline.yml`, `papers/core_set.csv`
- Tutorial: `outline/module_plan.yml`, `DECISIONS.md`
- Systematic synthesis: `papers/extraction_table.csv`, `output/PROTOCOL.md`
- Peer review: `output/CLAIMS.md`, `output/MISSING_EVIDENCE.md`, `output/NOVELTY_MATRIX.md`
- Idea shortlist: `output/IDEA_BRIEF.md`, `outline/taxonomy.yml`, `papers/core_set.csv`

## Outputs

- `output/DELIVERABLE_SELFLOOP_TODO.md` (PASS/FAIL + what changed + what still blocks)
- The chosen deliverable file is rewritten in-place (same path under `output/`).

## Procedure (plan -> act -> diagnose -> fix)

0) Pick the deliverable to fix
- Use the current unit row in `UNITS.csv` (its `inputs`/`outputs`) to avoid ambiguity.
- Use `PIPELINE.lock.md` (if present) to confirm the active pipeline and which rubric applies.
- If multiple deliverables exist, *only* fix the one declared by the unit.

1) Diagnose (write a short failing checklist)
- Read the deliverable and run the rubric for that deliverable type (below).
- List concrete failures with pointers (quote small spans; mention section headings).

2) Fix (rewrite, do not expand scope)
- Apply edits directly to the deliverable file under `output/`.
- When fixing a paragraph, you may generate 2-3 candidate rewrites and pick the best (best-of-N), but keep the final text single-track.

3) Re-check
- Re-run the rubric. If still FAIL, repeat steps 1-3.
- If you cannot reach PASS within 3 iterations, stop and write an actionable TODO list (do not thrash).

4) Write the report
- Always write `output/DELIVERABLE_SELFLOOP_TODO.md` (even on PASS).

## Rubrics (deliverable-specific)

### A) Snapshot (`output/SNAPSHOT.md`)

Hard rules:
- Bullet-first (avoid long paragraph narration).
- Every non-trivial point must cite 1-2 concrete paper pointers from `papers/core_set.csv`.
- No outline narration templates (e.g., "This section surveys...").

PASS signal:
- Most bullets are *content claims* + *why it matters* + *paper pointers*.

### B) Tutorial (`output/TUTORIAL.md`)

Hard rules:
- Must match `outline/module_plan.yml` scope (no silent expansion).
- Each module has: objective -> steps -> exercises -> expected output -> verification.
- Running example is consistent across modules (as approved in `DECISIONS.md`).

PASS signal:
- A reader can follow and verify progress module-by-module.

### C) Systematic review synthesis (`output/SYNTHESIS.md`)

Hard rules:
- Claims must be grounded in `papers/extraction_table.csv` (no free-floating conclusions).
- Explicit bias/limitations section (aligned with `output/PROTOCOL.md`).
- No over-generalization beyond the screened/extracted studies.

PASS signal:
- Each major conclusion points back to extracted evidence (and states limits).

### D) Peer review report (`output/REVIEW.md`)

Hard rules:
- Every major critique must be traceable to a claim in `output/CLAIMS.md` and/or a gap in `output/MISSING_EVIDENCE.md`.
- Novelty commentary must be based on `output/NOVELTY_MATRIX.md` (no invented related work).
- Suggestions must be actionable (what experiment/analysis would resolve it).

PASS signal:
- The report reads like a real referee report: specific, traceable, and actionable.

### E) Idea shortlist (`output/IDEA_SHORTLIST.md`)

Hard rules:
- Must respect the locked brief in `output/IDEA_BRIEF.md` (no silent scope drift).
- Must contain two layers:
  - **Idea Pool (Brainstorm)**: large expansion pool
  - **Final Shortlist**: small, research-grade, executable set

Pool PASS requirements:
- Size: 60-90 ideas (hard min 60).
- Diversity: covers >=6/8 operator families (counterfactual, failure-mode-first, eval swap, component swap, explicit-combination, cross-domain analogy, negative-result, system constraints).
- Each pool idea is a short card and includes:
  - tier label + operator tag
  - key assumption
  - 1-sentence falsification path
  - Tier-1/2 includes at least one `paper_id` pointer from `papers/core_set.csv`.

Shortlist PASS requirements:
- Size: 5-7 (default 7).
- Each shortlisted idea includes:
  - closest-3 prior work pointers (from `papers/core_set.csv`)
  - delta + non-delta
  - 1-week minimal validation plan (task/metric/baseline/resources/expected signal)
  - failure criteria
  - risks/failure modes (>=2)
  - evidence anchors (>=3 pointers)
- Portfolio constraints:
  - covers >=2-3 clusters from `outline/taxonomy.yml`
  - covers >=2 idea types
  - at most 1 item may be labeled "needs verification".

PASS signal:
- The shortlist reads like a "research plan shortlist" (doable + falsifiable + anchored), not inspirational slogans.

## Report format (must follow)

Write `output/DELIVERABLE_SELFLOOP_TODO.md` with:

- Status: PASS | FAIL

## Summary
<one paragraph>

## Changes made
- <bullet list>

## Remaining blockers (if FAIL)
- <bullet list>

## Next step
- If PASS: "Proceed to the next unit."
- If FAIL: "Fix upstream artifact X" or "Rewrite section Y".

## Troubleshooting

### The deliverable is generic / template-heavy

Fix:
- Replace narration bullets with concrete claims + constraints + pointers.
- Prefer fewer, more informative bullets over more bullets.

### The deliverable drifts beyond the approved scope

Fix:
- Re-align to the contract artifact (`outline/outline.yml` or `outline/module_plan.yml` or `output/PROTOCOL.md` or `output/IDEA_BRIEF.md`).
- Delete scope-creep paragraphs instead of trying to justify them.
