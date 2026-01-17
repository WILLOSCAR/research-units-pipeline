# Pipeline Questions / Improvement Backlog (skills-first)

This file tracks *pipeline/skills* improvement work (not per-workspace artifacts).

## Canonical E2E Run (for regression)

- `workspaces/e2e-agent-survey-skilllogic-20260117-004215/`
  - Draft: `workspaces/e2e-agent-survey-skilllogic-20260117-004215/output/DRAFT.md`
  - PDF: `workspaces/e2e-agent-survey-skilllogic-20260117-004215/latex/main.pdf`
  - Audit: `workspaces/e2e-agent-survey-skilllogic-20260117-004215/output/AUDIT_REPORT.md`

## What’s Still Weak (Writer-facing)

- Citation density is sometimes *globally* OK but can still feel locally “thin” if too many citations are reused across H3.
- Transitions can still be overly templated if subsection briefs lack `bridge_terms` / `contrast_hook` specificity.
- Evidence packs can be “long but low-signal” if claim candidates / highlights are truncated too aggressively.

## Changes Implemented (so far)

- Fixed numeric-anchor detection bug in `tooling/quality_gate.py` (regex `\\d` → `\d`).
- Raised context-pack trimming limits + added `pack_stats` so truncation/drop isn’t silent:
  - `.codex/skills/writer-context-pack/scripts/run.py`
- Reduced evidence loss from truncation:
  - `.codex/skills/evidence-draft/scripts/run.py` (claim candidates up to ~400 chars; highlights up to ~280 chars; no `...` suffix)
- Enforced paper-like outline budgets:
  - `tooling/quality_gate.py` now blocks if outline H2 > 8 or H3 > 12 (arxiv-survey profile).
- Added writer-stage logic polish unit:
  - `.codex/skills/section-logic-polisher/` (thesis + connector density report)
- Added a skills-first fix for low unique citations:
  - `.codex/skills/citation-diversifier/` (writes `output/CITATION_BUDGET_REPORT.md`)
  - referenced in `.codex/skills/pipeline-auditor/SKILL.md` and Stage C5 optional skills.

## Next Candidates (P1/P2)

- P1: Add a deterministic “citation embedding” heuristic gate (detect end-of-sentence cite dumps) to push toward evidence-as-argument.
- P1: Add a C5 “per-H3 evidence consumption” check against `must_use` minima (anchors/comparisons/limitations) to prevent long-but-hollow prose.
- P2: Add a small optional `outline-budgeter` skill to merge over-fragmented taxonomies into 3–4 core chapters (paper-like default).
- P2: Consider a `citation-injector` skill that writes per-H3 subset `.bib` files (harder cite-scope), if drift remains a problem.
