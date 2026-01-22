---
name: style-harmonizer
description: |
  De-slot and harmonize paper voice across `sections/*.md` without changing meaning or citation keys.
  **Trigger**: style harmonizer, de-template stems, remove slot phrases, discourse stems, 写作风格统一, 去槽位句式, 去生成器味.
  **Use when**: `writer-selfloop` is PASS but `output/WRITER_SELFLOOP_TODO.md` flags Style Smells (e.g., repeated count-based openers), or the draft reads like many sections share the same rhythm.
  **Skip if**: you need new evidence/citations (route to C3/C4), or you are pre-C2 (NO PROSE).
  **Network**: none.
  **Guardrail**: do not invent facts; do not add/remove/move citation keys; do not move citations across subsections; keep claim->evidence anchoring intact.
---

# Style Harmonizer (de-slot editor)

Purpose: remove subtle generator-voice signals that can survive structural gates.

This skill is not a full rewrite. It is a targeted rewrite queue:
- only touch the specific `sections/*.md` files flagged under `## Style Smells (non-blocking)`
- keep facts and citation keys unchanged

## Inputs

Required:
- `output/WRITER_SELFLOOP_TODO.md` (Style Smells section)
- the referenced `sections/*.md` files

Optional (helps you stay in-scope while rewriting):
- `outline/writer_context_packs.jsonl` (allowed citations + opener_mode hints)

## Output

- Updated `sections/*.md` files (same filenames; still body-only; no headings)
- Re-running `writer-selfloop` is the audit trail (Style Smells should shrink).
- Optional (pipeline signal): create `sections/style_harmonized.refined.ok` (empty file) when you are done.

## Role cards (use explicitly)

### Style Harmonizer (editor)

Mission: remove slot phrases and stem repetition while keeping meaning unchanged.

Do:
- rewrite the surface form (opener/closer/cadence), not the claim
- keep each paragraph content-bearing (argument bridge, not navigation)
- prefer small local edits over global style refactors

Avoid:
- adding new factual claims or new citations
- moving citations to different paragraphs or different subsections
- rewriting a thin section instead of routing upstream for more evidence

### Evidence Steward (skeptic)

Mission: prevent style work from becoming content drift.

Do:
- after each rewrite, spot-check that every cited claim still matches the same sentence
- if you feel forced to add new material to make prose sound better, stop and route upstream

## Common style smells and how to fix them

### 1) Count-based opener slots (Two limitations..., Three takeaways...)

Why it is high-signal: it creates a reusable sentence slot that repeats across H3s.

Rewrite moves (choose one):
- Integrate the caveat into a contrast paragraph (last sentence): state the boundary that changes interpretation.
- Use a single caveat sentence opener (no counting): "A caveat is that ..." / "These results hinge on ..." / "Evidence is thin when ...".
- If enumeration is truly needed, hide the count: use two coordinated clauses in one sentence, or vary the syntax (do not repeat across sections).

Mini example (paraphrase only):
- Bad: `Two limitations stand out. First, ...`
- Better: `A caveat is that ...; this matters because it changes how results transfer across protocols.`

### 2) Reused discourse stems (The key point is that ...)

Rewrite moves:
- Replace with one of: "A practical implication is that ...", "One takeaway is that ...", "A useful way to read these results is ...".
- Change cadence: split into a short claim sentence plus a follow-up sentence with the condition/why.

### 3) Same opener cadence across many H3s

Rewrite moves:
- Switch opener mode for the section (tension-first / decision-first / protocol-first / contrast-first).
- Replace generic connectors (Additionally/Moreover) with content-bearing pivots ("At the protocol level, ...", "Under budget constraints, ...").

### 4) Overview / narration openers ("This section provides an overview ...")

Why it is high-signal: it reads like a generated ToC narration rather than a paper argument.

Rewrite moves:
- Replace "overview" narration with a content-bearing lens: tension/decision/failure/protocol/contrast.
- Keep the first sentence falsifiable: name the constraint and why it matters (not what you are about to do).

Mini example (paraphrase only):
- Bad: `This section provides an overview of tool interfaces for agents.`
- Better: `Tool interfaces define what actions are executable; interface contracts therefore determine which evaluation claims transfer across environments.`

## Workflow (minimal)

1) Read `output/WRITER_SELFLOOP_TODO.md`
- Find `## Style Smells (non-blocking)` and the file list.

2) Rewrite only the flagged files
- Make small edits: opener/closer stems, sentence shape, connector variety.
- If needed, consult `outline/writer_context_packs.jsonl` for `opener_mode` hints and to stay citation-scope safe while rewriting.
- Do not touch citation keys.

3) Re-run `writer-selfloop`
- Expect: PASS remains PASS.
- Expect: Style Smells section is shorter (or disappears).

## Done checklist

- [ ] The same slot phrase does not repeat across multiple H3s (especially count-based openers).
- [ ] No citation keys were added/removed/moved.
- [ ] `writer-selfloop` still reports PASS, and Style Smells shrinks.
