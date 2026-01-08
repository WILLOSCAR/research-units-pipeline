---
name: survey-visuals
description: |
  Draft non-prose visuals artifacts (tables, timeline, figure specs) for a survey, grounded in evidence and using citation keys from `citations/ref.bib`.
  **Trigger**: survey visuals, tables, timeline, figures, visuals, 图表, 时间线, figure spec.
  **Use when**: survey 的 C4（NO PROSE），已有 outline + claim/evidence + citations，需要先把对比表/演化时间线/图规格落盘。
  **Skip if**: 缺少 `citations/ref.bib`（或 evidence 还没整理到位，导致表格只能写空洞模板）。
  **Network**: none.
  **Guardrail**: NO PROSE；表格/时间线/图规格必须具体且可核对（含 citations），禁止遗留 TODO/SCAFFOLD。
---

# Survey Visuals (NO PROSE)

Create non-prose “visual thinking” artifacts that make the actual writing stage less template-y:

- comparison tables (method + evaluation)
- timeline / evolution bullets
- figure specs (what to draw, why it matters, what papers support it)

## Inputs

- `outline/outline.yml`
- `outline/claim_evidence_matrix.md`
- `papers/paper_notes.jsonl`
- `citations/ref.bib`

## Outputs

- `outline/tables.md`
- `outline/timeline.md`
- `outline/figures.md`

## Workflow (heuristic)
Uses: `outline/outline.yml`, `outline/claim_evidence_matrix.md`.


1. Read the outline + claim–evidence matrix and pick the **comparison axes** that recur across sections:
   - control loop / planner-executor split
   - tool interface & orchestration
   - memory / retrieval / reflection
   - environments & benchmarks
   - safety / security / alignment surfaces
2. Tables (`outline/tables.md`):
   - Write **≥2 Markdown tables** with real entries and citations.
   - Prefer one “method matrix” and one “evaluation/benchmark matrix”.
3. Timeline (`outline/timeline.md`):
   - Write year → key milestone bullets (aim for breadth and citations).
4. Figures (`outline/figures.md`):
   - Write 2–4 figure specs that a human could draw:
     - purpose (“what insight this figure communicates”)
     - required elements (boxes/arrows/axes)
     - what papers support each element (cite keys)
5. Use only citation keys present in `citations/ref.bib`.

## Quality checklist

- [ ] No `TODO` and no `<!-- SCAFFOLD ... -->` markers remain in the outputs.
- [ ] `outline/tables.md` contains ≥2 Markdown tables with real content and citations.
- [ ] `outline/timeline.md` contains ≥8 year bullets and each bullet has ≥1 citation marker `[@...]`.
- [ ] `outline/figures.md` contains ≥2 figure specs and each mentions at least one supporting citation.

## Helper script (optional)

### Quick Start

- `python .codex/skills/survey-visuals/scripts/run.py --help`
- `python .codex/skills/survey-visuals/scripts/run.py --workspace <workspace_dir>`

### All Options

- See `--help` (this helper is intentionally minimal)

### Examples

- Generate baseline visuals, then refine manually:
  - Run the helper once, then refine `outline/tables.md`, `outline/timeline.md`, `outline/figures.md` for better coverage/accuracy (without leaving placeholders).

### Notes

- The helper generates baseline visuals and never overwrites non-placeholder artifacts.
- If `papers/paper_notes.jsonl` exists it will prefill candidate rows/bullets with `paper_id` + `bibkey` citation markers.
- In `pipeline.py --strict` it will be blocked only if placeholder markers remain (and if minimum table/timeline/figure requirements are not met).

## Troubleshooting

### Common Issues

#### Issue: Visuals are still scaffolds (`TODO`/template)

**Symptom**:
- Quality gate blocks `survey-visuals` outputs.

**Causes**:
- Helper script generated scaffolds, but tables/timeline/figures were not rewritten.

**Solutions**:
- Fill `outline/tables.md` with ≥2 real comparison tables (include citations in rows).
- Fill `outline/timeline.md` with ≥8 dated milestones (each with citations).
- Fill `outline/figures.md` with ≥2 figure specs (purpose/elements/citations).

#### Issue: Missing citation keys

**Symptom**:
- You can’t cite in visuals (no `[@Key]`).

**Causes**:
- `citations/ref.bib` not generated yet, or notes have no `bibkey`.

**Solutions**:
- Run `citation-verifier` and ensure `papers/paper_notes.jsonl` includes `bibkey`.

### Recovery Checklist

- [ ] No `TODO`/scaffold markers remain in visuals artifacts.
- [ ] Tables/timeline/figures contain citations from `citations/ref.bib`.
