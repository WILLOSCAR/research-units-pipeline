---
name: latex-compile-qa
description: Compile a LaTeX project and run basic QA (missing refs, bib errors, broken citations), producing a PDF and a short build report. Use when a LaTeX scaffold exists and you need to ensure it compiles.
---

# LaTeX Compile + QA

Compile the LaTeX project and produce a PDF (when the toolchain is available), plus a short build report.

This step is deterministic; if compilation fails, record actionable diagnostics rather than guessing.

## Inputs

- `latex/main.tex`
- `citations/ref.bib`

## Outputs

- `latex/main.pdf` (if compilation succeeds)
- `output/LATEX_BUILD_REPORT.md` (recommended)

## Workflow

1. Run a LaTeX build (e.g., `latexmk`) if available.
2. Fix missing packages, missing bib entries, and unresolved references.
3. Record remaining issues in a build report.

## Quality checklist

- [ ] Either `latex/main.pdf` exists, or `output/LATEX_BUILD_REPORT.md` explains why compilation failed.

## Script

- `python .codex/skills/latex-compile-qa/scripts/run.py --workspace <workspace_dir>`
  - Uses `latexmk -xelatex -bibtex` when available and writes `output/LATEX_BUILD_REPORT.md`.
