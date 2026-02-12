---
name: idea-finder
version: 2.3
target_artifacts:
  - STATUS.md
  - UNITS.csv
  - CHECKPOINTS.md
  - DECISIONS.md
  - GOAL.md
  - queries.md
  - output/IDEA_BRIEF.md
  - papers/papers_raw.jsonl
  - papers/papers_dedup.jsonl
  - papers/core_set.csv
  - papers/retrieval_report.md
  - outline/taxonomy.yml
  - papers/paper_notes.jsonl
  - papers/evidence_bank.jsonl
  - output/IDEA_SHORTLIST.md
  - output/DELIVERABLE_SELFLOOP_TODO.md
  - output/QUALITY_GATE.md
  - output/RUN_ERRORS.md
  - output/CONTRACT_REPORT.md
default_checkpoints: [C0,C1,C2,C3,C4,C5]
units_template: templates/UNITS.idea-finder.csv
---

# Pipeline: research ideation (idea shortlist)

Goal: produce a **research idea shortlist** (`output/IDEA_SHORTLIST.md`) that balances:
- **expansion**: a structured brainstorm pool (60–90 candidates),
- **convergence**: select→evaluate→subset→fuse into 5–7 *doable* ideas,
- **auditability**: every shortlisted idea has explicit assumptions + falsification + paper pointers (no invented papers).

This pipeline is designed for “找 research idea / brainstorm / 选题 / 找方向”, not for writing a full survey paper.

Default profile (Lite+):
- Retrieval route: `literature-engineer` (multi-route recall)
- `core_size=100`
- Idea Pool: 60–90 (50/50: cross-domain framing vs failure/eval-protocol)
- Final shortlist: 7 ideas
- Evidence mode: `abstract` (no fulltext download by default)

## Stage 0 - Init + idea brief (C0)
required_skills:
- workspace-init
- pipeline-router
- idea-brief
- human-checkpoint
produces:
- STATUS.md
- UNITS.csv
- CHECKPOINTS.md
- DECISIONS.md
- GOAL.md
- queries.md
- output/IDEA_BRIEF.md

Notes:
- The brief (`output/IDEA_BRIEF.md`) is the single source of truth (scope/constraints/rubric/query buckets).
- The pipeline should **block once** at C0 for human approval of the brief before retrieval.

## Stage 1 - Retrieval + core set (C1)
required_skills:
- literature-engineer
- dedupe-rank
produces:
- papers/papers_raw.jsonl
- papers/papers_dedup.jsonl
- papers/core_set.csv
- papers/retrieval_report.md

Notes:
- Use multi-query buckets from `queries.md` (not a single giant query).
- If recall is too low/noisy, fix it upstream (rewrite buckets + exclusions) and rerun C1 (bounded iterations).

## Stage 2 - Idea map / focus (C2) [NO PROSE]
required_skills:
- taxonomy-builder
- pipeline-router
- human-checkpoint
produces:
- outline/taxonomy.yml
- DECISIONS.md

human_checkpoint:
- approve: focus clusters + exclusions (based on `outline/taxonomy.yml`)
- write_to: DECISIONS.md

Notes:
- This is intentionally lighter than a survey outline: taxonomy is used as an **idea map**.
- Default behavior: pause at C2 so the human can pick 1–2 clusters (and hard excludes) before ideation.

## Stage 3 - Evidence substrate (C3) [NO PROSE]
required_skills:
- paper-notes
produces:
- papers/paper_notes.jsonl
- papers/evidence_bank.jsonl

Notes:
- Notes must include limitations/failure modes (otherwise ideation collapses into “only stronger” ideas).

## Stage 4 - Ideation: expand → triage → fuse (C4)
required_skills:
- idea-pool-expander
- idea-shortlist-curator
produces:
- output/IDEA_SHORTLIST.md

Notes:
- Idea Pool is large (60–90) and operator-driven (explicit ideation operators).
- Final shortlist is small (default 7) and research-grade (closest-3 delta + 1-week validation plan + failure criteria).

## Stage 5 - Deliverable self-loop + contract audit (C5)
required_skills:
- deliverable-selfloop
- artifact-contract-auditor
produces:
- output/IDEA_SHORTLIST.md
- output/DELIVERABLE_SELFLOOP_TODO.md
- output/CONTRACT_REPORT.md

Notes:
- `deliverable-selfloop` must treat `output/IDEA_SHORTLIST.md` as a first-class deliverable (PASS/FAIL rubric).
- The contract audit ensures the workspace is shareable and complete for this pipeline’s `target_artifacts`.

