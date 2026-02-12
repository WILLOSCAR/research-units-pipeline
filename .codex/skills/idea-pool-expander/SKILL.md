---
name: idea-pool-expander
description: |
  Generate a large, structured brainstorm pool (60-90) for ideation and write it into `output/IDEA_SHORTLIST.md`.
  **Trigger**: idea pool, brainstorm pool, expand ideas, 发散, 头脑风暴, idea candidates.
  **Use when**: you have a core set + taxonomy map and want to expand thinking before curating a shortlist.
  **Skip if**: you only want a small, feasibility-first shortlist (use `idea-shortlist-curator` directly).
  **Network**: none.
  **Guardrail**: no invented papers; each Tier-1/2 idea must point to `papers/core_set.csv` paper_ids; keep cards short.
---

# Idea Pool Expander (operator-driven)

Goal: create a **big pool** of idea candidates that genuinely expands thinking, but remains controllable and auditable.

This skill writes the **Idea Pool** section of `output/IDEA_SHORTLIST.md`.
The final shortlist is handled by `idea-shortlist-curator`.

## Inputs

- `output/IDEA_BRIEF.md`
- `outline/taxonomy.yml`
- `papers/paper_notes.jsonl`
- `papers/core_set.csv`

## Outputs

- `output/IDEA_SHORTLIST.md`

## Operators (use explicitly)

Use these operator families to force diversity. Target >=6/8 families represented.

1) Counterfactual / constraint flip
2) Failure-mode-first
3) Evaluation protocol swap (task/metric/budget)
4) Component swap in an agent loop
5) Combination with explicit assumptions
6) Cross-domain analogy import
7) Negative-result mining
8) System/product constraints (cost/latency/auditability)

## Procedure (best-of-N, then write)

1) Read the contract from `output/IDEA_BRIEF.md`
- Scope / exclusions / constraints
- Targets: pool size range, shortlist size, operator mix (default 50/50)

2) Use `outline/taxonomy.yml` as the idea map
- Ensure the pool covers multiple clusters (avoid all ideas collapsing into one bucket).

3) Use `papers/paper_notes.jsonl` to avoid fantasy ideas
- Prefer ideas that respond to explicit limitations/failure modes recorded in notes.

4) Multi-sample within each operator family (best-of-N)
- For each operator family, generate 2-3 alternative mini-sets.
- Choose the best mini-set by: novelty, clarity, falsifiability.

5) Write the Idea Pool into `output/IDEA_SHORTLIST.md`
- Pool size: 60-90 (hard min 60)
- Each idea is a short card (3-6 lines):
  - Tier label (Tier-0 Wild / Tier-1 Plausible / Tier-2 Ready)
  - Operator tag
  - One-liner problem statement
  - Key assumption
  - How to falsify (1 sentence)
  - Evidence pointers:
    - Tier-0: optional
    - Tier-1/2: required (>=1 `paper_id` from `papers/core_set.csv`)

6) Add a small "Pool Diagnostics" block
- Counts by tier
- Counts by operator family
- Coverage across taxonomy clusters

## Acceptance

- `output/IDEA_SHORTLIST.md` contains an "Idea Pool" section with 60-90 ideas.
- Operator coverage >=6/8.
- Every Tier-1/2 idea includes at least one pointer to `papers/core_set.csv` (paper_id).
- Cards are short; no long paragraphs.

## Troubleshooting

### Issue: pool feels repetitive / not expanding

Fix:
- Increase operator coverage (force missing families).
- Add at least 5 ideas that are *failure-mode-first* and 5 that are *evaluation-protocol-swap*.

### Issue: too many wild ideas

Fix:
- Convert some Tier-0 into Tier-1 by attaching at least one `paper_id` pointer.
- Or explicitly tag as "needs verification" and keep it out of the final shortlist.
