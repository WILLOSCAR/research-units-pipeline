---
name: citation-verifier
description: Generate and verify BibTeX entries from paper notes, writing `citations/ref.bib` and `citations/verified.jsonl` with url/date/title for every entry. Use when preparing citations before prose/LaTeX writing; requires network or explicit human verification.
---

# Citation Verifier

Generate `citations/ref.bib` and ensure every entry has a traceable verification record in `citations/verified.jsonl`.

When network access is restricted, prefer a “record now, verify later” workflow: keep URLs/titles consistent and leave a clear verification note.

## Input

- `papers/paper_notes.jsonl`

## Outputs

- `citations/ref.bib`
- `citations/verified.jsonl`

## Workflow (heuristic)

1. Collect `bibkey`, `title`, `url`, `year`, `authors` from `papers/paper_notes.jsonl`.
2. Write/refresh `citations/ref.bib`:
   - Prefer arXiv-style fields when `arxiv_id` / `primary_category` exist (`eprint`, `archivePrefix`, `primaryClass`).
3. Write one verification record per BibTeX entry to `citations/verified.jsonl` with at least:
   - `bibkey`, `title`, `url`, `date`
4. If you cannot verify via network, record a clear `notes` field (e.g., “auto-generated; needs manual verification”) and/or request human confirmation depending on your policy.

## Quality checklist

- [ ] Every BibTeX entry has a corresponding `verified.jsonl` record.
- [ ] No missing `url`/`date`/`title` in verification records.

## Script

- `python .codex/skills/citation-verifier/scripts/run.py --workspace <workspace_dir>`
