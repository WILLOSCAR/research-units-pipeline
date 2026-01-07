# Skill & Pipeline Standard (Codex CLI + Claude Code)

This repo is meant to work well across:
- OpenAI Codex (Codex CLI / IDE)
- Anthropic Claude Code (Claude Code CLI)

The goal is **LLM-first semantic work + deterministic helper scripts**, with a clear artifact contract (`UNITS.csv`) and explicit human checkpoints (`DECISIONS.md`).

## 1) Skill bundle contract (Anthropic-style)

Each skill is a folder under `.codex/skills/<skill>/` and must include:
- `SKILL.md` (required): YAML front matter + operational instructions
- `scripts/` (optional): deterministic helpers (scaffold/compile/validate)
- `references/` (optional): deeper docs, checklists (avoid bloating `SKILL.md`)
- `assets/` (optional): templates, schemas, fixtures

### Progressive disclosure (recommended)

1. **YAML front matter**: only `name` + `description` (for discovery/routing).
2. **`SKILL.md` body**: the workflow + checklists + guardrails.
3. **Scripts/resources**: loaded only when the workflow calls for them.

## 2) Script policy (deterministic helpers only)

Borrowing the best pattern from Anthropic’s `skills` repos:
- Scripts are treated as **black-box helpers**.
- Always run scripts with `--help` first (do not ingest source unless necessary).
- Scripts should be used for:
  - scaffolding (create directories/files/templates)
  - validation (format/schema checks)
  - compilation (LaTeX build, QA reports)
  - deterministic transforms (MD→LaTeX conversion, dedupe/ranking)

**Avoid** scripts that “replace” semantic work (taxonomy/outline/notes/writing). If a script exists for those, it must be clearly labeled **bootstrap only** and the workflow must still require LLM refinement before marking a unit `DONE`.

## 3) Pipeline/Units contract (repo-specific)

### Single source of truth

- `UNITS.csv` is the execution contract (one row = one deliverable with acceptance criteria).
- `pipelines/*.pipeline.md` defines the pipeline intent and checkpoints, and points to the concrete `templates/UNITS.*.csv`.
- If a pipeline doc and its units template diverge, **the inconsistency is a bug** and must be resolved by syncing them.

### Checkpoints & no-prose rule

- Checkpoints are enforced via `DECISIONS.md` approvals (`- [ ] Approve C*`).
- Units with `owner=HUMAN` block until the corresponding checkbox is ticked.
- Prose writing is only allowed after the required approval (survey default: `C2`).

## 4) “LLM-first” execution model (recommended)

For semantic units:
- Follow the referenced skill’s `Procedure` and write the listed outputs directly.
- Only mark `DONE` when acceptance criteria are satisfied and outputs exist.
- If you use helper scripts to scaffold, treat the outputs as **starting points**, not final.

For deterministic units (retrieval/dedupe/compile/format checks):
- Use scripts under the skill’s `scripts/` folder.

## 5) Minimal authoring checklist

### New skill

- [ ] Has `SKILL.md` with `name` + `description`.
- [ ] Declares clear **Inputs / Outputs** and **Acceptance criteria**.
- [ ] If scripts exist: they are deterministic and safe; `SKILL.md` explains when to use them.

### New pipeline

- [ ] `pipelines/<name>.pipeline.md` has YAML front matter with `units_template`.
- [ ] Every `required_skills` listed in the pipeline appears in the units template CSV.
- [ ] Units template references only existing skill folders.

## 6) Cross-tool compatibility (.claude + .codex)

Codex discovers skills under `.codex/skills/`. For Claude Code, keep `.claude/skills/` pointing at the same set (symlink or copy).

Repo helper: `python scripts/validate_repo.py` checks pipeline↔template↔skill alignment.

