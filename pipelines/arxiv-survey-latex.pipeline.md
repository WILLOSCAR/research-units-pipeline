---
name: arxiv-survey-latex
version: 1.1
target_artifacts:
  - outline/taxonomy.yml
  - outline/outline.yml
  - outline/mapping.tsv
  - papers/fulltext_index.jsonl
  - papers/paper_notes.jsonl
  - outline/claim_evidence_matrix.md
  - outline/tables.md
  - outline/timeline.md
  - outline/figures.md
  - citations/ref.bib
  - citations/verified.jsonl
  - output/DRAFT.md
  - latex/main.tex
  - latex/main.pdf
  - output/LATEX_BUILD_REPORT.md
default_checkpoints: [C0,C1,C2,C3]
units_template: templates/UNITS.arxiv-survey-latex.csv
---

# Pipeline: arXiv survey / review (MD-first + LaTeX/PDF)

Same as `arxiv-survey`, but includes the optional LaTeX scaffold + compile units so the default deliverable is a compiled PDF.

## Stage 0 - Init (C0)
required_skills:
- workspace-init
produces:
- STATUS.md
- UNITS.csv
- CHECKPOINTS.md
- DECISIONS.md

## Stage 1 - Retrieval & core set (C1)
required_skills:
- arxiv-search
- dedupe-rank
optional_skills:
- keyword-expansion
- survey-seed-harvest
produces:
- papers/papers_raw.jsonl
- papers/papers_dedup.jsonl
- papers/core_set.csv

Notes:
- `queries.md` may specify `max_results` and a year `time window`; `arxiv-search` will paginate and attach arXiv metadata (categories, arxiv_id, etc.) when online.
- If you import an offline export but later have network, you can set `enrich_metadata: true` in `queries.md` (or run `arxiv-search --enrich-metadata`) to backfill missing abstracts/authors/categories via arXiv `id_list`.

## Stage 2 - Structure (C2) [NO PROSE]
required_skills:
- taxonomy-builder
- outline-builder
- section-mapper
produces:
- outline/taxonomy.yml
- outline/outline.yml
- outline/mapping.tsv
human_checkpoint:
- approve: scope + outline
- write_to: DECISIONS.md

## Stage 3 - Evidence → Draft → PDF (C3) [NO PROSE until C2 approved]
required_skills:
- pdf-text-extractor
- paper-notes
- claim-evidence-matrix
- citation-verifier
- survey-visuals
- prose-writer
- latex-scaffold
- latex-compile-qa
produces:
- papers/fulltext_index.jsonl
- papers/paper_notes.jsonl
- outline/claim_evidence_matrix.md
- citations/ref.bib
- citations/verified.jsonl
- outline/tables.md
- outline/timeline.md
- outline/figures.md
- output/DRAFT.md
- latex/main.tex
- latex/main.pdf
- output/LATEX_BUILD_REPORT.md

Notes:
- `queries.md` can set `evidence_mode: "abstract"|"fulltext"` (default template uses `abstract`).
- If `evidence_mode: "fulltext"`, `pdf-text-extractor` can be tuned via `fulltext_max_papers`, `fulltext_max_pages`, `fulltext_min_chars`, and `--local-pdfs-only`.
- In strict mode, the pipeline should block if the PDF is too short (<8 pages) or if citations are undefined (even if LaTeX technically compiles).
