---
name: paper-notes
description: Write structured notes for each paper in the core set (summary bullets, method, results, limitations) into `papers/paper_notes.jsonl`. Use after mapping to prepare evidence without writing prose.
---

# Paper Notes

Produce consistent, searchable paper notes that later steps (claims, visuals, writing) can reliably synthesize.

This is still **NO PROSE**: keep notes as bullets / short fields, not narrative paragraphs.

## When to use

- After you have a core set (and ideally a mapping) and need evidence-ready notes.
- Before writing a survey draft.

## Inputs

- `papers/core_set.csv`
- Optional: `outline/mapping.tsv` (to prioritize)
- Optional: `papers/fulltext_index.jsonl` + `papers/fulltext/*.txt` (if running in fulltext mode)

## Output

- `papers/paper_notes.jsonl` (JSONL; one record per paper)

## Decision: evidence depth

- If you have extracted text (`papers/fulltext/*.txt`) → enrich key papers using fulltext snippets and set `evidence_level: "fulltext"`.
- If you only have abstracts (default) → keep long-tail notes abstract-level, but still fully enrich **high-priority** papers (see below).

## Workflow (heuristic)

1. Ensure **coverage**: every `paper_id` in `papers/core_set.csv` must have one JSONL record.
2. Use mapping to choose **high-priority papers**:
   - heavily reused across subsections
   - pinned classics (ReAct/Toolformer/Reflexion… if in scope)
3. For high-priority papers, capture:
   - 3–6 summary bullets (what’s new, what problem setting, what’s the loop)
   - `method` (mechanism / architecture; what differs from baselines)
   - `key_results` (benchmarks/metrics; include numbers if available)
   - `limitations` (specific assumptions/failure modes; avoid generic boilerplate)
4. For long-tail papers:
   - keep summary bullets short (abstract-derived is OK)
   - still include at least one limitation, but make it specific when possible
5. Assign a stable `bibkey` for each paper for citation generation.

## Quality checklist

- [ ] Coverage: every `paper_id` in `papers/core_set.csv` appears in `papers/paper_notes.jsonl`.
- [ ] High-priority papers have non-`TODO` method/results/limitations.
- [ ] Limitations are not copy-pasted across many papers.
- [ ] `evidence_level` is set correctly (`abstract` vs `fulltext`).

## Helper script (optional)

Bootstrap scaffold only:
- Run `python .codex/skills/paper-notes/scripts/run.py --help` first.
- Then: `python .codex/skills/paper-notes/scripts/run.py --workspace <workspace_dir>`

The helper writes deterministic metadata + abstract scaffolds, and marks high-priority papers with `TODO` fields. In `pipeline.py --strict` it will be blocked until you enrich those high-priority notes and remove TODOs.
