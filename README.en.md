# research-units-pipeline-skills

> **In one sentence**: Make pipelines that can "guide humans / guide models" through research—not a bunch of scripts, but a set of **semantic skills**, where each skill knows "what to do, how to do it, when it's done, and what NOT to do."

---

## Core Design: Skills-First + Decomposed Pipeline + Evidence-First

**The traditional problem**: Research pipelines are either black-box scripts (hard to debug) or loose documentation (requires human judgment at runtime).

**Our solution**:

1. **Semantic Skills**: Each skill is not a function, but a **guided execution unit**—
   - `inputs / outputs`: explicit dependencies and artifacts
   - `acceptance`: completion criteria (e.g., "each subsection maps to >=8 papers")
   - `notes`: how to do it, edge cases, common mistakes
   - `guardrail`: what NOT to do (e.g., **NO PROSE** in C2-C4)

2. **Decomposed Pipeline**: 6 checkpoints (C0→C5), 36 atomic units, dependencies explicit in `UNITS.csv`
3. **Evidence-First**: C2-C4 enforce building evidence substrate first (taxonomy → mapping → evidence packs), C5 writes prose

**Design Goals**:
- **Reusable**: Same skill (e.g., `subsection-writer`) works across pipelines—no rewriting logic
- **Guided**: Newcomers/models follow `acceptance` + `notes`—no guessing "how much is enough"
- **Constrained**: `guardrail` prevents executors (especially models) from going off-rails (e.g., writing prose in C3)
- **Locatable**: Failures point to specific skill + artifact—fix and resume from failure point

---

**Why this design?**

| Property | Traditional | This Design |
|----------|-------------|-------------|
| **Visible** | Black-box scripts | Each unit produces intermediate files (`papers/`, `outline/`, `citations/`, `sections/`) |
| **Auditable** | Scattered logs | `UNITS.csv` records execution history + acceptance criteria; `DECISIONS.md` records human checkpoints |
| **Self-healing** | Failure = full restart | Quality gate FAIL → report tells you what to fix → resume from failed unit |
| **Reusable** | Rewrite per project | Skills are modular, reusable across pipelines (e.g., `taxonomy-builder`, `evidence-binder`) |
| **Guided** | Human judgment | Each skill has `acceptance` + `notes`—executor knows "what done looks like" |

中文版本：[`README.md`](README.md).

## One-line Activation (recommended: run in chat)

Send this to Codex (or Claude Code):

> Write me an agent LaTeX survey

This triggers skills routing and executes the pipeline (artifacts written per `UNITS.csv` contract).

Optional:
- Specify pipeline: `pipelines/arxiv-survey-latex.pipeline.md`
- No auto-approval at C2: remove "auto-approve C2" from your prompt

More explicit (less routing errors):

> Use `pipelines/arxiv-survey-latex.pipeline.md` to write me an agent LaTeX survey (strict quality gates; auto-approve C2)

## What You Get (Layered Artifacts + Self-Healing Entry Points)

**Execution Layer**:
- `UNITS.csv`: 36 atomic units as execution contract (dependencies → inputs → outputs → acceptance)
- `DECISIONS.md`: Human checkpoints (**C2 requires outline approval** before prose)

**Artifact Layer** (by checkpoint):
```
C1: papers/papers_raw.jsonl → core_set.csv              # Retrieval 200+ → dedupe to 150+
C2: outline/taxonomy.yml → outline.yml → mapping.tsv    # Structure (NO PROSE) → human approval
C3: papers/paper_notes.jsonl → subsection_briefs.jsonl  # Evidence substrate (NO PROSE)
C4: citations/ref.bib → evidence_drafts.jsonl           # Citations + evidence packs (NO PROSE)
C5: sections/*.md → output/DRAFT.md → latex/main.pdf    # Evidence-based writing + compile
```

**Self-Healing Entry Points** (on quality gate FAIL):
- `output/QUALITY_GATE.md`: tells you which artifact to fix
- `output/SECTION_LOGIC_REPORT.md`: thesis + connector density
- `output/CITATION_BUDGET_REPORT.md`: citation density suggestions

## Conversational Execution (0 to PDF)

```
You: Write me an agent LaTeX survey

↓ [C0-C1] Retrieve 200+ papers → dedupe to 150+ core set (arXiv auto-fills metadata)
↓ [C2] Build taxonomy + outline + mapping (NO PROSE) → pause at C2 for approval

You: Approve C2, continue

↓ [C3-C4] Build evidence substrate (paper notes + evidence packs + citations) (NO PROSE)
↓ [C5] Evidence-based writing → quality gate check

【PASS】→ output/DRAFT.md + latex/main.pdf ✓
【FAIL】→ output/QUALITY_GATE.md points to artifact needing fix

You (if FAIL): Fix the file (e.g., outline/evidence_drafts.jsonl), say "continue"
→ Resume from failed unit, no full restart needed
```

**Key principle**: C2-C4 enforce NO PROSE—build evidence substrate first; C5 writes prose; failures are point-fixable.

## Example Artifacts (v0.1, full intermediate outputs)

Path: `example/e2e-agent-survey-latex-verify-20260118-182656/` (pipeline: `pipelines/arxiv-survey-latex.pipeline.md`).
Config: `draft_profile: lite` / `evidence_mode: abstract` / `core_size: 220` (see `queries.md`).

Directory map:

```text
example/e2e-agent-survey-latex-verify-20260118-182656/
  STATUS.md            # progress + run log (current checkpoint)
  UNITS.csv            # execution contract (deps / acceptance / outputs)
  DECISIONS.md         # human checkpoints (Approve C*)
  CHECKPOINTS.md       # checkpoint rules
  PIPELINE.lock.md     # selected pipeline (single source of truth)
  GOAL.md              # goal/scope seed
  queries.md           # retrieval + writing profile config
  papers/              # C1/C3: retrieval outputs and paper "substrate"
  outline/             # C2/C3/C4: taxonomy/outline/mapping + briefs + evidence packs
  citations/           # C4: BibTeX + verification records
  sections/            # C5: per-H2/H3 writing units (incl. chapter leads)
  output/              # C5: merged DRAFT + reports
  latex/               # C5: LaTeX scaffold + compiled PDF
```

Pipeline view (how folders connect):

```mermaid
flowchart LR
  C0["Contract files<br/>(STATUS/UNITS/DECISIONS)"] --> C1["papers/ (retrieval + core set)"]
  C1 --> C2["outline/ (taxonomy/outline/mapping)"]
  C2 --> C4["citations/ (ref.bib + verified)"]
  C4 --> C5s["sections/ (per-H3 writing units)"]
  C5s --> OUT["output/ (DRAFT + reports)"]
  OUT --> TEX["latex/ (main.tex + main.pdf)"]
```

Final deliverables only:
- Draft (Markdown): `example/e2e-agent-survey-latex-verify-20260118-182656/output/DRAFT.md`
- PDF: `example/e2e-agent-survey-latex-verify-20260118-182656/latex/main.pdf`
- QA report: `example/e2e-agent-survey-latex-verify-20260118-182656/output/AUDIT_REPORT.md`

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
