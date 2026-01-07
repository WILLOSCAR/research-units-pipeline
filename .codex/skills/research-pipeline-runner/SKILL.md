---
name: research-pipeline-runner
description: >
  Run this repo’s Units+Checkpoints research pipelines end-to-end (survey/综述/review/调研/教程/系统综述/审稿),
  including kickoff, workspace creation under workspaces/, and auto-running units with a single HITL approval checkpoint (usually C2).
  Use when a user says “写一篇关于 X 的 survey/综述/review/调研” or asks to start/continue/run the pipeline.
---

# Research Pipeline Runner

Use this skill to run the repo’s **UNITS + checkpoints** workflow end-to-end, while keeping semantic work LLM-driven (scripts are helpers, not the author).

## Non-negotiables

- Use `UNITS.csv` as the execution contract; one unit at a time.
- Respect checkpoints (`CHECKPOINTS.md`): **no long prose** until required approvals are recorded in `DECISIONS.md` (survey default: `C2`).
- Stop at HUMAN checkpoints and wait for explicit sign-off.
- Never create workspace artifacts (`STATUS.md`, `UNITS.csv`, `DECISIONS.md`, etc.) in the repo root; always use `workspaces/<name>/`.
- Treat skill scripts as **helpers** (deterministic tasks / scaffolding). For semantic units, the “real work” is done by following the relevant `SKILL.md` and refining outputs until quality gates pass.

## Decision tree: pick a pipeline

User goal → choose:
- Survey/综述/调研 + Markdown draft → `pipelines/arxiv-survey.pipeline.md`
- Survey/综述/调研 + PDF output → `pipelines/arxiv-survey-latex.pipeline.md`
- Snapshot/速览 → `pipelines/lit-snapshot.pipeline.md`
- Tutorial/教程 → `pipelines/tutorial.pipeline.md`
- Systematic review/系统综述 → `pipelines/systematic-review.pipeline.md`
- Peer review/审稿 → `pipelines/peer-review.pipeline.md`

## Recommended run loop (human-like)

1. Create a workspace under `workspaces/` and kick off the pipeline.
2. Run units in `--strict` mode so “scaffolds that look finished” don’t silently pass.
3. Treat each blocked unit as a mini writing loop:
   - read the unit’s `SKILL.md`
   - refine the artifacts until they look like real work (not templates)
   - then mark the unit `DONE` and continue
4. Stop once for the human checkpoint (survey default: `C2`), then proceed to writing after approval.

## Practical commands (optional helpers)

- Kickoff + run (recommended): `python scripts/pipeline.py kickoff --topic "<topic>" --pipeline <pipeline-name> --run --strict`
- Resume: `python scripts/pipeline.py run --workspace <ws> --strict`
- Approve checkpoint: `python scripts/pipeline.py approve --workspace <ws> --checkpoint C2`
- Mark refined unit: `python scripts/pipeline.py mark --workspace <ws> --unit-id <U###> --status DONE --note "LLM refined"`

## Handling common blocks

- **HUMAN approval required**: summarize produced artifacts, ask for approval, then record it and resume.
- **Quality gate blocked** (`output/QUALITY_GATE.md` exists): treat current outputs as scaffolding; refine per the unit’s `SKILL.md`; mark `DONE`; resume.
- **No network**: ask the user for an export; use `arxiv-search` offline import.
- **Weak coverage** (mapping/notes): broaden queries or reduce/merge subsections before writing.

## Quality checklist

- [ ] `UNITS.csv` statuses reflect actual outputs (no `DONE` without outputs).
- [ ] No prose is written unless `DECISIONS.md` explicitly approves it for the relevant checkpoint/sections.
- [ ] The run stops at HUMAN checkpoints with clear next questions.
- [ ] In `--strict` mode, scaffold/stub outputs do not get marked `DONE` without LLM refinement.
