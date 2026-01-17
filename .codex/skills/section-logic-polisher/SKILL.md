---
name: section-logic-polisher
description: |
  Logic coherence pass for per-H3 section files: enforce an explicit thesis statement + inter-paragraph logical connectors before merging.
  **Trigger**: logic polisher, section logic, thesis statement, connectors, 段落逻辑, 连接词, 论证主线, 润色逻辑.
  **Use when**: `sections/S*.md` exist but read like paragraph islands; you want a targeted, debuggable self-loop before `section-merger`.
  **Skip if**: sections are missing/thin (fix `subsection-writer` first) or evidence packs/briefs are scaffolded (fix C3/C4 first).
  **Network**: none.
  **Guardrail**: do not add new citations; do not invent facts; do not change citation keys; do not move citations across subsections.
---

# Section Logic Polisher (thesis + connectors)

Purpose: close the main “paper feel” gap that remains even when a subsection is long and citation-dense:
- missing/weak **thesis** (no central claim)
- weak **inter-paragraph flow** (paragraph islands; few logical connectors)

This is a **local, per-H3** polish step that happens after drafting and before merging.

## Inputs

- `sections/` (expects H3 body files like S<sec>_<sub>.md)
- `outline/subsection_briefs.jsonl` (uses `thesis` + `paragraph_plan[].connector_phrase`)
- Optional: `outline/writer_context_packs.jsonl` (preferred; has trimmed anchors/comparisons + `must_use`)

## Outputs

- `output/SECTION_LOGIC_REPORT.md` (PASS/FAIL report for thesis + connector density)

Manual / LLM-first (in place):
- Update the H3 files under `sections/` to fix thesis/connectors (no new citations; keep keys stable)

## Workflow (self-loop)

1. Run the checker script to surface the exact failing files and why.
2. For each failing H3 file:
   - **Thesis**: ensure the first paragraph ends with a clear thesis sentence.
     - Prefer: `This subsection argues/shows/surveys that ...` (commitment level must match evidence; be conservative under abstract-only evidence).
     - Use the brief’s `thesis` as the source of truth (from `outline/subsection_briefs.jsonl`; paraphrase is OK, same meaning).
   - **Flow**: ensure paragraph 2..N start with a logical connector phrase.
     - Prefer the brief’s `paragraph_plan[].connector_phrase` (from `outline/subsection_briefs.jsonl`; adapt for grammar, keep meaning).
     - If available, prefer the merged pack (`outline/writer_context_packs.jsonl`) so your edits stay aligned with `must_use` (anchors/comparisons/limitations).
     - Aim to include causal + contrast + extension connectors across the subsection.
   - **Guardrails**: do not add/remove citation keys; do not introduce new factual claims.
3. Re-run the checker until `output/SECTION_LOGIC_REPORT.md` is PASS, then proceed to `transition-weaver` and `section-merger`.

## Done criteria

- `output/SECTION_LOGIC_REPORT.md` shows `- Status: PASS`
- No section file contains placeholders (`TODO`/`…`/`...`) or outline meta markers (`Intent:`/`RQ:`/`Evidence needs:`)
- Thesis + connector checks pass for all H3 files

## Script

### Quick Start

- `python .codex/skills/section-logic-polisher/scripts/run.py --help`
- `python .codex/skills/section-logic-polisher/scripts/run.py --workspace workspaces/<ws>`

### All Options

- `--workspace <dir>`
- `--unit-id <U###>`
- `--inputs <semicolon-separated>`
- `--outputs <semicolon-separated>`
- `--checkpoint <C#>`

### Examples

- Default IO:
  - `python .codex/skills/section-logic-polisher/scripts/run.py --workspace workspaces/<ws>`
- Explicit output path:
  - `python .codex/skills/section-logic-polisher/scripts/run.py --workspace workspaces/<ws> --outputs "output/SECTION_LOGIC_REPORT.md"`

## Troubleshooting

### Issue: report says thesis missing but the subsection has an intro sentence

Fix:
- The checker looks for an explicit thesis signal (e.g., `This subsection argues that ...`) in the first paragraph.
- Add a single thesis sentence at the end of paragraph 1 (copy from briefs; do not add new facts/citations).

### Issue: connector density fails but the prose reads fine

Fix:
- Expand connector vocabulary (causal/contrast/extension/implication) and ensure some appear explicitly.
- Prefer short connector stems; don’t add long filler sentences.
