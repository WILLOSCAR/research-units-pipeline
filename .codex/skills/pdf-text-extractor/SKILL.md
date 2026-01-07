---
name: pdf-text-extractor
description: Download PDFs (when available) and extract plain text to support full-text evidence, writing `papers/fulltext_index.jsonl` and per-paper text files under `papers/fulltext/`.
---

# PDF Text Extractor

Optionally collect **full-text snippets** to deepen evidence beyond abstracts.

This skill is intentionally conservative: in many survey runs, **abstract/snippet mode is enough** and avoids heavy downloads.

## Inputs

- `papers/core_set.csv` (expects `paper_id`, `title`, and ideally `pdf_url`/`arxiv_id`/`url`)
- Optional: `outline/mapping.tsv` (to prioritize mapped papers)

## Outputs

- `papers/fulltext_index.jsonl` (one record per attempted paper)
- Side artifacts:
  - `papers/pdfs/<paper_id>.pdf` (cached downloads)
  - `papers/fulltext/<paper_id>.txt` (extracted text)

## Decision: evidence mode

- `queries.md` can set `evidence_mode: "abstract" | "fulltext"`.
  - `abstract` (default template): **do not download**; write an index that clearly records skipping.
  - `fulltext`: download PDFs (when possible) and extract text to `papers/fulltext/`.

## Workflow (heuristic)

1. Read `papers/core_set.csv`.
2. If `outline/mapping.tsv` exists, prioritize mapped papers first.
3. For each selected paper (fulltext mode):
   - resolve `pdf_url` (use `pdf_url`, else derive from `arxiv_id`/`url` when possible)
   - download to `papers/pdfs/<paper_id>.pdf` if missing
   - extract a reasonable prefix of text to `papers/fulltext/<paper_id>.txt`
   - append/update a JSONL record in `papers/fulltext_index.jsonl` with status + stats
4. Never overwrite existing extracted text unless explicitly requested (delete the `.txt` to re-extract).

## Quality checklist

- [ ] `papers/fulltext_index.jsonl` exists and is non-empty.
- [ ] If `evidence_mode: "fulltext"`: at least a small but non-trivial subset has extracted text (strict mode blocks if extraction coverage is near-zero).
- [ ] If `evidence_mode: "abstract"`: the index records clearly reflect skip status (no downloads attempted).

## Script

This is a deterministic helper; run `--help` first:
- `python .codex/skills/pdf-text-extractor/scripts/run.py --help`
- `python .codex/skills/pdf-text-extractor/scripts/run.py --workspace <workspace_dir>`
