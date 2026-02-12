---
name: idea-shortlist-curator
description: |
  Converge a brainstorm pool into a research-grade shortlist via select→evaluate→subset→fuse, writing `output/IDEA_SHORTLIST.md`.
  **Trigger**: idea shortlist, curate ideas, select ideas, 选题, 收敛, 选段融合, shortlist.
  **Use when**: you already have an Idea Pool and want 5-7 *doable* research ideas with explicit validation plans.
  **Skip if**: you need more expansion first (run `idea-pool-expander`).
  **Network**: none.
  **Guardrail**: no invented papers; each shortlisted idea must anchor to `papers/core_set.csv`; keep the output crisp (no essay prose).
---

# Idea Shortlist Curator (select → evaluate → subset → fuse)

Goal: turn a large Idea Pool into a **small, research-grade** shortlist that is:
- feasible under constraints,
- novelty is expressed as delta vs closest prior work,
- falsifiable (clear failure criteria),
- portfolio-diverse.

This skill rewrites `output/IDEA_SHORTLIST.md` by:
- keeping the Pool section,
- adding/replacing the "Final Shortlist" section.

## Inputs

- `output/IDEA_BRIEF.md`
- `output/IDEA_SHORTLIST.md` (must contain the Idea Pool)
- `outline/taxonomy.yml`
- `papers/paper_notes.jsonl`
- `papers/core_set.csv`

## Outputs

- `output/IDEA_SHORTLIST.md`

## Rubric (weights come from the brief)

Score candidates on:
- novelty_delta (vs closest-3)
- feasibility (fits constraints)
- evidence_density / traceability
- consistency (task/eval definitions don't conflict)
- writeability (can be written into a coherent paper/report)
- portfolio_diversity (cluster coverage + idea type coverage)

## Shortlist card contract (per idea)

Each shortlisted idea must include:
- Problem (1-2 sentences; testable)
- Closest-3 (3 `paper_id` pointers from `papers/core_set.csv`)
- Delta (2-4 bullets)
- Non-Delta (1-2 bullets; what is NOT actually new)
- Minimal validation plan (1 week): task + metric + baseline + resources + expected signal
- Failure criteria (what result kills it)
- Risks / failure modes (>=2)
- Evidence anchors: >=3 core paper pointers total

Portfolio constraints:
- cover >=2-3 clusters from `outline/taxonomy.yml`
- cover >=2 idea types (e.g., eval/protocol vs mechanism vs system constraint)
- at most 1 item may be labeled "needs verification" (and it must say what evidence is missing)

## Procedure

1) Read constraints + rubric weights from `output/IDEA_BRIEF.md`
- If constraints are missing, add a blocking question to `DECISIONS.md` (do not pretend).

2) Parse the Idea Pool from `output/IDEA_SHORTLIST.md`
- Discard candidates that violate exclusions.
- De-duplicate near-identical ideas (keep the best phrasing).

3) Build evidence anchors using `papers/paper_notes.jsonl` + `papers/core_set.csv`
- For each candidate, attach 1-3 plausible paper pointers.
- Prefer pointers that directly relate to the candidate's failure mode / protocol gap.

4) Propose 2-3 shortlist compositions internally
- Composition A: feasibility-heavy
- Composition B: novelty-heavy
- Composition C: portfolio-diverse

5) Select the best composition and fuse overlaps
- If two shortlisted ideas overlap, keep one and merge the strongest parts.

6) Write "Final Shortlist" into `output/IDEA_SHORTLIST.md`
- Size default: 7 (or follow `idea_shortlist_size` in the brief)
- For each idea, write the full card contract (closest-3/delta/validation/failure/risks/anchors).

7) Add a short "Selection Rationale" section
- Why these ideas (top 3 reasons)
- Top 5 excluded high-scoring ideas and why they were excluded (e.g., infeasible, duplicate, weak evidence)

## Acceptance

- `output/IDEA_SHORTLIST.md` contains a Final Shortlist (5-7; default 7).
- Every shortlisted idea satisfies the card contract and points to `papers/core_set.csv` paper_ids.
- Portfolio constraints are satisfied (>=2-3 clusters; >=2 idea types).

## Troubleshooting

### Issue: shortlist is too wild / not doable

Fix:
- Tighten feasibility weight in the brief and rerun.
- Replace the item with the best next candidate from the same cluster.

### Issue: novelty is hand-wavy

Fix:
- Enforce closest-3 + delta/non-delta.
- If you can't name closest prior work from `papers/core_set.csv`, mark the idea as "needs verification" and keep it out of the shortlist.
