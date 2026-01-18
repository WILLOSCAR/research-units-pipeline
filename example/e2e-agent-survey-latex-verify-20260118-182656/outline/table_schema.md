# Table schema (evidence-first)

- Policy: schema-first; tables are verifiable artifacts (not prose).
- Cell style: short phrases; avoid paragraph cells; prefer 1–2 clauses per cell.
- Citation rule: every row must include at least one citation marker `[@BibKey]` in a dedicated column.

- Goal (from `GOAL.md`): LLM agents survey (tool-use, planning, memory, multi-agent)
- Subsections (H3) detected: 8
- Evidence packs: 8
- Briefs: 8

## Table 1: Subsection comparison map (axes + representative works)
- Question: For each H3, what are the concrete comparison axes and which representative works ground them?
- Row unit: H3 subsection (`sub_id`).
- Columns:
  - Subsection (id + title)
  - Axes (3–5 short phrases)
  - Representative works (3–5 cite keys)
- Evidence mapping:
  - Axes: `outline/subsection_briefs.jsonl:axes`
  - Representative works: cite keys from evidence pack blocks (snippets/claims/comparisons/limitations)

## Table 2: Evidence readiness + verification needs
- Question: For each H3, what is the evidence level and what fields must be verified before strong conclusions?
- Row unit: H3 subsection (`sub_id`).
- Columns:
  - Subsection (id + title)
  - Evidence levels (fulltext/abstract/title counts)
  - Verify fields (short checklist; no prose)
  - Representative works (3–5 cite keys)
- Evidence mapping:
  - Evidence levels: `outline/evidence_drafts.jsonl:evidence_level_summary`
  - Verify fields: `outline/evidence_drafts.jsonl:verify_fields`

## Constraints (for table-filler)
- Minimum tables: >=2.
- No placeholders or instruction-like fragments (e.g., 'enumerate 2-4 items').
- No long prose cells: keep each cell <= ~160 characters when possible.
