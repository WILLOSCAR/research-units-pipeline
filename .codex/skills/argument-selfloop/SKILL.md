---
name: argument-selfloop
description: |
  Argument self-loop: maintain an argument ledger + premise consistency report for drafted sections.
  **Trigger**: argument self-loop, argument chain, premise consistency, section self-check, paragraph contract, 论证自循环, 论证链路, 前提一致性, 段落论证动作.
  **Use when**: you are in C5 (PROSE allowed), `sections/*.md` exist, and you want to prevent “smooth but hollow” writing by enforcing argument moves + premise hygiene before merge.
  **Skip if**: you are pre-C2 (NO PROSE), or evidence packs are scaffolded/thin (route upstream to `evidence-selfloop` first).
  **Network**: none.
  **Guardrail**: do not invent facts; do not add/remove/move citation keys; do not move citations across subsections; the argument ledger is an intermediate artifact and must never be inserted into the paper.
---

# Argument Self-loop (write -> self-check -> ledger -> revise)

Purpose: upgrade C5 from “generate text” to “execute argument actions under explicit constraints”.

This skill operationalizes the mechanism you described as a reusable, pipeline-native component:
- write section-by-section
- self-check paragraph-by-paragraph
- maintain a small argument ledger that makes dependencies explicit
- revise only what fails until the chain is continuous

It complements (not replaces) the other self-loops:
- `evidence-selfloop`: blocks writing when packs are not writeable (do not pad)
- `writer-selfloop`: blocks template voice, missing sections/leads, scope/citation violations
- `argument-selfloop` (this skill): blocks *argument discontinuity* and *premise drift* (even when prose is fluent)


## Core idea: two intermediate artifacts (never in the paper)

This skill treats “argument structure” as a first-class intermediate artifact, like evidence packs.

Outputs:
- `output/SECTION_ARGUMENT_SUMMARIES.jsonl` (structured; per-section/per-paragraph argument moves)
- `output/ARGUMENT_SKELETON.md` (compact narrative + dependency map; not a prose restatement)
- `output/ARGUMENT_SELFLOOP_TODO.md` (PASS/FAIL + actionable edits)

These files are *not* reader-facing and must never be merged into `output/DRAFT.md`.


## What this self-loop enforces (your 3 invariants)

After you complete a section (H3 or key front matter), the section must satisfy:

1) **Correct narrative linkage (paragraph-to-paragraph)**
- the relation between adjacent paragraphs is explicit (cause/contrast/refinement/boundary)
- no silent topic-switch; no “jump cut”

2) **Closed argument loop (section-level)**
The section answers, in its own text (not in a hidden outline):
- what question is it resolving?
- what argument path does it take?
- what is the conclusion?
- what premises does the conclusion rely on?

3) **Premises + definitions are explicit and stable**
- new terms / protocol assumptions are defined at first use
- the definition matches global usage (no drift)
- task/metric/constraint assumptions do not silently change across sections

The self-check must result in concrete edits: add a missing definition, add a bridge sentence, add an explicit contrast, add a scope boundary, delete/reorder a paragraph, or strengthen the local conclusion.


## Paragraph contract (argument actions)

Every paragraph must execute at least one argument action and be locally self-consistent.
Use this action set (can be combined, but never empty):

- `Claim`: a testable judgement/conclusion (avoid generic background)
- `Definition/Setup`: introduce a concept, assumption, task definition, protocol, comparison set
- `Justification`: reasoning chain or evidence support (including citations)
- `Contrast/Differentiation`: clarify differences, remove ambiguity
- `Boundary/Failure`: applicability limits, failure modes, threats to validity
- `Local Conclusion`: a reusable takeaway / constraint that downstream paragraphs can rely on

One-sentence self-check (per paragraph):
- "This paragraph’s action(s) are: <…>. Its output is: <…>."

If you cannot answer, the paragraph must be rewritten/merged/split until the action and output are clear.


## How to run it (LLM-first workflow)

1) Pick the scope of this pass
- default: run it after `writer-selfloop` PASS, before merge
- incremental: run it after finishing 1-2 H3s, so you catch drift early

2) For each target section file (start with H3 bodies)
- read the section
- do a paragraph-by-paragraph action labeling *in the ledger*, not in the prose
- identify failures (missing definition, missing bridge, missing conclusion, implicit premise)
- apply the fix to the *section file* (`sections/S<sub_id>.md`) without changing citation keys

3) Update the two-level ledger
- write/update the record for that section in `output/SECTION_ARGUMENT_SUMMARIES.jsonl`
- update `output/ARGUMENT_SKELETON.md` so it reflects:
  - the section’s functional role in the paper
  - what premises it consumes
  - what conclusions/definitions it produces for downstream sections

4) Write `output/ARGUMENT_SELFLOOP_TODO.md`
- `- Status: FAIL` + a list of concrete edits when any section fails
- `- Status: PASS` only when all required sections are coherent and premises are stable

5) Rerun until PASS


## Output contract

### `output/ARGUMENT_SELFLOOP_TODO.md`

Must exist and start with:
- `- Status: PASS|FAIL`

Recommended structure (keep it short and debuggable):
- `## Failures (blocking)`
- `## Fix plan (actionable edits)` (per file)
- `## Premise drift watchlist (non-blocking)`


### `output/SECTION_ARGUMENT_SUMMARIES.jsonl`

JSONL (one record per section/subsection).

Required fields per record:
- `kind`: `h3` | `front_matter` | `discussion` | `conclusion` (minimal set)
- `id`: for H3 use the subsection id (e.g., `"3.2"`)
- `title`
- `section_id`, `section_title` (for H3)
- `section_role`: what this unit does in the paper (e.g., `mechanism`, `evaluation_lens`, `risk_lens`, `synthesis`)
- `depends_on`: list of premises/definitions it assumes
- `adds`: list of premises/definitions/conclusions it introduces
- `paragraphs`: list of objects, each with:
  - `i` (1-based paragraph index)
  - `moves` (non-empty list; pick from: `claim`, `definition_setup`, `justification`, `contrast`, `boundary_failure`, `local_conclusion`)
  - `output` (one sentence: what this paragraph produces)

Notes:
- This is an intermediate ledger: short, structural, no prose restatement.
- Do not paste long sentences from the draft. Use short summaries.


### `output/ARGUMENT_SKELETON.md`

A compact narrative/dependency map (not a retelling of the paper).

It should include:
- each H2/H3’s **necessity** (what gap it fills)
- explicit **dependencies** (premises consumed, outputs produced)
- a global **consistency contract**: terms/protocol assumptions that must not drift

Keep it "writer-facing": no reader signposting, no “in this section we…”.


## Routing rules (avoid polishing around missing substance)

- If a section cannot produce a justified claim without new evidence: STOP and route to `evidence-selfloop`.
- If a section fails due to template voice / missing citations / out-of-scope keys: route to `writer-selfloop` / `citation-*` first.
- This skill is for argument continuity and premise hygiene, not for adding new facts.


## Script (validator-only)

This skill includes a validator script so the pipeline can block on missing ledgers.
It does not write prose; it only checks that the required artifacts exist and that the ledger covers all H3s.

### Quick Start

- `python .codex/skills/argument-selfloop/scripts/run.py --workspace workspaces/<ws>`

### All Options

- `--workspace <dir>`
- `--unit-id <U###>`
- `--inputs <semicolon-separated>`
- `--outputs <semicolon-separated>`
- `--checkpoint <C#>`

### Examples

- Validate the ledgers exist + are PASS + cover all H3:
  - `python .codex/skills/argument-selfloop/scripts/run.py --workspace workspaces/<ws>`
