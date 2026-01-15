---
name: writer-context-pack
description: |
  Build per-H3 writer context packs (NO PROSE): merge briefs + evidence packs + anchor facts + allowed citations into a single deterministic JSONL, so drafting is less hollow and less brittle.
  **Trigger**: writer context pack, context pack, drafting pack, paragraph plan pack, 写作上下文包.
  **Use when**: `outline/subsection_briefs.jsonl` + `outline/evidence_drafts.jsonl` + `outline/anchor_sheet.jsonl` exist and you want to make C5 drafting easier/more consistent.
  **Skip if**: upstream evidence is missing or scaffolded (fix `paper-notes` / `evidence-binder` / `evidence-draft` / `anchor-sheet` first).
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent facts/citations; only use citation keys present in `citations/ref.bib`.
---

# Writer Context Pack (C4→C5 bridge) [NO PROSE]

Purpose: reduce C5 “hollow writing” by giving the writer a **single, per-subsection context pack**:
- the exact RQ/axes + paragraph plan (`subsection_briefs`)
- concrete comparison cards + evaluation protocol + limitations (`evidence_drafts`)
- numeric/eval/limitation anchors (`anchor_sheet`)
- allowed citation scope (subsection + chapter union) from `evidence_bindings`

## Inputs

- `outline/outline.yml`
- `outline/subsection_briefs.jsonl`
- `outline/chapter_briefs.jsonl`
- `outline/evidence_drafts.jsonl`
- `outline/anchor_sheet.jsonl`
- `outline/evidence_bindings.jsonl`
- `citations/ref.bib`

## Outputs

- `outline/writer_context_packs.jsonl`

## Output format (`outline/writer_context_packs.jsonl`)

JSONL, one object per H3 subsection.

Required keys:
- `sub_id`, `title`, `section_id`, `section_title`
- `rq`, `axes`, `paragraph_plan`
- `allowed_bibkeys_{selected,mapped,chapter}`
- `anchor_facts` (trimmed)
- `comparison_cards` (trimmed)

## Writer contract (how C5 should use this pack)

Treat each pack as an executable checklist, not optional context:

- **Plan compliance**: follow `paragraph_plan` (don’t skip planned paragraphs; merge only if you keep the same contrasts/anchors).
- **Anchors are must-use**: include at least one `anchor_facts` item that matches your paragraph’s claim type (eval / numeric / limitation), when present.
- **Comparisons are must-use**: reuse `comparison_cards` to write explicit A-vs-B contrast sentences (avoid “A then B” separate summaries).
- **Micro-structure**: if prose starts drifting into flat summaries, apply `grad-paragraph` repeatedly (tension → contrast → evaluation anchor → limitation).
- **Citation scope**: prefer `allowed_bibkeys_selected`; use `allowed_bibkeys_chapter` only for intra-chapter background, and keep >=2 subsection-specific citations per H3.

## Script

### Quick Start

- `python .codex/skills/writer-context-pack/scripts/run.py --help`
- `python .codex/skills/writer-context-pack/scripts/run.py --workspace workspaces/<ws>`

### All Options

- `--workspace <dir>`
- `--unit-id <U###>`
- `--inputs <semicolon-separated>`
- `--outputs <semicolon-separated>`
- `--checkpoint <C#>`

### Examples

- Default IO:
  - `python .codex/skills/writer-context-pack/scripts/run.py --workspace workspaces/<ws>`
- Explicit IO:
  - `python .codex/skills/writer-context-pack/scripts/run.py --workspace workspaces/<ws> --inputs "outline/outline.yml;outline/subsection_briefs.jsonl;outline/chapter_briefs.jsonl;outline/evidence_drafts.jsonl;outline/anchor_sheet.jsonl;outline/evidence_bindings.jsonl;citations/ref.bib" --outputs "outline/writer_context_packs.jsonl"`

Freeze policy:
- Create `outline/writer_context_packs.refined.ok` to prevent regeneration.
