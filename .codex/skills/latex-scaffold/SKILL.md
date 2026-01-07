---
name: latex-scaffold
description: Scaffold a LaTeX project (main.tex, bibliography wiring, structure) from an existing markdown draft and bib file. Use when the pipeline needs a LaTeX deliverable after writing is approved.
---

# LaTeX Scaffold

Convert the approved Markdown draft into a minimal, buildable LaTeX project.

This is a deterministic conversion step; prose quality should already be addressed in `output/DRAFT.md`.

## Inputs

- `output/DRAFT.md` (or another approved draft)
- `citations/ref.bib`

## Outputs

- `latex/main.tex` (and any required LaTeX support files)

## Workflow

1. Create `latex/` directory if missing.
2. Create `latex/main.tex` with sections matching the outline.
3. Wire bibliography to `citations/ref.bib`.

## Quality checklist

- [ ] `latex/main.tex` exists and references `citations/ref.bib`.

## Script

- `python .codex/skills/latex-scaffold/scripts/run.py --workspace <workspace_dir>`
  - Converts `output/DRAFT.md` to `latex/main.tex`:
    - Headings `##/###/####` → `\\section/\\subsection/\\subsubsection` (strips leading numeric prefixes like `1.2`).
    - `## Abstract` → `abstract` environment.
    - `[@Key]` or `[@Key1; @Key2]` → `\\citep{Key}` / `\\citep{Key1,Key2}`.
    - Inline markdown `**bold**` / `*italic*` / `` `code` `` → `\\textbf{}` / `\\emph{}` / `\\texttt{}`.
