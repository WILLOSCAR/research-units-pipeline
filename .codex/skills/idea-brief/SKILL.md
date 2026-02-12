---
name: idea-brief
description: |
  Lock an ideation run into a single-source-of-truth brief (`output/IDEA_BRIEF.md`) and a replayable multi-query plan (`queries.md`).
  **Trigger**: idea brief, ideation brief, research ideas, brainstorm, 找 idea, 选题, 点子, 找方向.
  **Use when**: the user wants research ideas and their input is long / multi-turn; you need to clarify scope+constraints before retrieval.
  **Skip if**: the goal is to write a survey draft directly (use `arxiv-survey*` pipelines instead).
  **Network**: none.
  **Guardrail**: do not invent papers/citations; do not start retrieval here; keep the brief structured (no long prose).
---

# Idea Brief (SSOT for ideation)

Goal: turn "a lot of user thoughts" into an auditable **idea contract** that downstream steps can follow without drift.

This skill does **not** retrieve papers. It only locks:
- scope + constraints + exclusions,
- evaluation rubric (how we will pick ideas),
- multi-query buckets (how we will search),
into `output/IDEA_BRIEF.md` and `queries.md`.

## Role cards (prompt-level guidance)

- **Ideation PM**
  - Mission: lock scope/constraints so the pipeline won't drift.
  - Do: ask only the minimum questions that materially change retrieval or feasibility.
  - Avoid: letting the run proceed with "vague topic + no constraints".

- **Query Architect**
  - Mission: translate scope into a *multi-query* plan (not one giant query).
  - Do: write 3-6 query buckets and explicit exclusions in `queries.md`.
  - Avoid: infinite keyword expansion; keep buckets few and purposeful.

## Inputs

Required:
- `GOAL.md`
- `DECISIONS.md`
- `queries.md`

Optional:
- `PIPELINE.lock.md` (confirm the pipeline is `idea-finder`)
- Existing `output/IDEA_BRIEF.md` (refine in place if re-running)

## Outputs

- `output/IDEA_BRIEF.md`
- `queries.md`
- `DECISIONS.md` (optional: add open questions / constraints reminders)

## Procedure

1) Read `GOAL.md` and the current kickoff block in `DECISIONS.md`
- Extract the topic, the why-now, and any hard constraints/excludes already stated.

2) Ask the minimum clarification questions (max 2 rounds)
- Focus only on decisions that change the run:
  - timebox / compute / data availability
  - in-scope vs out-of-scope
  - what a "good idea" means (rubric weights)
- If the user says "你自己决定", proceed with defaults below.

3) Write or update `output/IDEA_BRIEF.md` (single source of truth)
Must include (bullets/tables; no long prose):
- Scope (in/out)
- Constraints (timebox/compute/data/implementation appetite)
- Exclusions (>=3 or explicit "none")
- Rubric + weights (sum=1.0)
- Targets (core size, pool size, shortlist size)
- Stop rules (bounded iterations)
- Query buckets (3-6) + exclusions
- Open questions (if any)

4) Rewrite `queries.md` as a replayable multi-query plan
Keep it compatible with retrieval scripts (`literature-engineer` reads `- keywords:` / `- exclude:` lists):
- Under `- keywords:` put bucket-level query strings (3-6 lines).
- Under `- exclude:` put explicit exclusions (0-10 lines).
- Set scalars:
  - `- max_results: "1800"`
  - `- core_size: "100"`
  - `- time window:` (optional; from/to)

Also add ideation-only config (for humans/LLM; retrieval may ignore):
- `- draft_profile: "idea_finder"`
- `- idea_pool_min: "60"`
- `- idea_pool_max: "90"`
- `- idea_shortlist_size: "7"`
- `- operator_mix: "50/50"` (cross-domain vs failure/eval)

5) If `PIPELINE.lock.md` exists, sanity-check it
- Confirm it points to `pipelines/idea-finder.pipeline.md`.
- If it points elsewhere, write a warning into `DECISIONS.md` (do not change lock silently).

## Acceptance

- `output/IDEA_BRIEF.md` exists and is actionable (structured, not narrative).
- `queries.md` has non-empty `- keywords:` items and (optional) `- exclude:` items.
- `queries.md` sets `core_size` and ideation targets (pool/shortlist).
- Any unresolved ambiguity is listed under "Open questions" in `output/IDEA_BRIEF.md` and/or `DECISIONS.md`.

## Troubleshooting

### Issue: `queries.md` keywords are empty, retrieval will fail

Fix:
- Add 3-6 bucket-level query strings under `- keywords:` (not single tokens).
- Add exclusions under `- exclude:` to control noise.

### Issue: brief is too vague ("topic only")

Fix:
- Add at least: constraints (timebox/compute/data) + exclusions + rubric weights.
