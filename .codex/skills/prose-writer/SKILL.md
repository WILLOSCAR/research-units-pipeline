---
name: prose-writer
description: |
  Write `output/DRAFT.md` or `output/SNAPSHOT.md` from approved outline and evidence, using only verified citation keys from `citations/ref.bib`.
  **Trigger**: write draft, prose writer, snapshot, survey writing, 写综述, 生成草稿.
  **Use when**: outline + evidence 已就绪且 HITL 审批已记录在 `DECISIONS.md`（survey 默认：C2 通过后）。
  **Skip if**: 缺少必要审批（`DECISIONS.md` 未勾选 Approve C*）或证据/引用尚未准备好。
  **Network**: none.
  **Guardrail**: 在审批前禁止写长 prose（可做 bullets-only artifacts）；只使用 `citations/ref.bib` 中存在的 citation keys。
---

# Prose Writer

Write a survey draft (or short snapshot) that reads like a real paper: motivation → structure → cross-paper synthesis → limitations/future work → conclusion.

This skill is where “human-like iteration” matters: outline + evidence first, then section writing, then a polish pass to remove repetition.

## Non-negotiables

- **No prose without approval**: check `DECISIONS.md` (survey default requires `Approve C2`).
- **No invented citations**: only use keys that exist in `citations/ref.bib`.

## Inputs

- `outline/outline.yml`
- Optional: `outline/claim_evidence_matrix.md`
- Optional: `outline/tables.md`, `outline/timeline.md`, `outline/figures.md` (from `survey-visuals`)
- Optional: `papers/core_set.csv`
- `citations/ref.bib` (when using citations)
- `DECISIONS.md` (must authorize prose when required)

## Outputs

- `output/DRAFT.md` and/or `output/SNAPSHOT.md`

## Decision: snapshot vs draft

- Snapshot: bullets-first, ~1 page, “what exists + what’s missing”.
- Draft: section-by-section prose with tables/timeline and subsection-specific synthesis.

## Workflow (heuristic)
Uses: `outline/outline.yml`, `outline/figures.md`, `papers/core_set.csv`.


1. Gate check: confirm writing is approved in `DECISIONS.md`.
   - If not approved, write a short request (what you plan to write, and what evidence you will rely on) and stop.
2. Pre-write pass (2–5 minutes):
   - skim `outline/claim_evidence_matrix.md` + `outline/tables.md` + `outline/timeline.md`
   - decide the “through-line” of the paper (what story ties sections together)
3. Write the draft in a paper-like order:
   - Abstract
   - Introduction (motivation, scope, contributions, positioning vs prior surveys)
   - Background / problem setup (only as needed)
   - Body sections per outline with **cross-paper comparisons**
   - Timeline/Evolution section (milestones + citations)
   - Open Problems & Future Directions (make them subsection-specific and concrete)
   - Conclusion
4. Synthesis style (avoid per-paper lists):
   - compare 2–4 approaches in one paragraph
   - name the trade-off and the evidence (benchmarks, settings, failure modes)
   - mention limitations with citations when possible
   - **rule of thumb**: each subsection should contain at least one paragraph that cites ≥2 works (so it reads like synthesis, not a paper-by-paper list)
5. Tables/figures:
   - include ≥2 tables directly in the draft (the tables can be copied from `outline/tables.md`)
   - reference figure specs (you can include them as “Figure X (spec)” until real figures are drawn)
6. Polish pass:
   - remove repeated template phrasing (“本小节聚焦…”, identical open-problems lines, identical takeaways)
   - ensure each subsection has at least one citation
   - ensure language/style is consistent (choose Chinese-first or English-first)

## Quality checklist

- [ ] If targeting PDF (e.g., `arxiv-survey-latex`): draft length is sufficient to compile into >= 8 pages (checked at `latex-compile-qa`).
- [ ] Writing respects checkpoint policy (no prose without approval).
- [ ] All citation keys referenced exist in `citations/ref.bib`.
- [ ] Draft includes: Introduction, Timeline/Evolution, Open Problems & Future Directions, Conclusion.
- [ ] Draft includes ≥2 comparison tables and avoids repeated boilerplate across subsections.
- [ ] Most subsections include at least one “multi-citation” paragraph (≥2 citations in the same paragraph) to enforce cross-paper comparisons.

## Helper script (optional)

### Quick Start

- `python .codex/skills/prose-writer/scripts/run.py --help`
- `python .codex/skills/prose-writer/scripts/run.py --workspace <workspace_dir>`

### All Options

- See `--help` (the helper writes a first-pass draft and enforces approvals)

### Examples

- Generate a first-pass draft after approval:
  - Tick `Approve C2` in `DECISIONS.md` (or run `python scripts/pipeline.py approve --workspace <ws> --checkpoint C2`), then run the script.

### Notes

- The helper writes a first-pass draft if missing and never overwrites an existing refined draft.
- If `outline/mapping.tsv` + `papers/paper_notes.jsonl` exist it will include starter mapped paper IDs + citation keys.
- In `pipeline.py --strict` the quality gate will block template-y drafts.

## Troubleshooting

### Common Issues

#### Issue: Script refuses to write (missing approval)

**Symptom**:
- Unit is `BLOCKED` and `DECISIONS.md` asks for `Approve C2`.

**Causes**:
- Survey policy: prose is allowed only after HUMAN approves C2.

**Solutions**:
- Tick `Approve C2` in `DECISIONS.md` (or run `python scripts/pipeline.py approve --workspace <ws> --checkpoint C2`).

#### Issue: Quality gate blocks template-y draft

**Symptom**:
- `output/QUALITY_GATE.md` reports draft looks like scaffolding/template.

**Causes**:
- Draft still contains repeated `TODO` blocks or generic paragraphs.

**Solutions**:
- Rewrite section-by-section using `outline/claim_evidence_matrix.md` and `outline/tables.md`/`timeline.md`/`figures.md`.
- Add cross-paper comparisons and concrete trade-offs.

### Recovery Checklist

- [ ] `DECISIONS.md` has `Approve C2` ticked (survey).
- [ ] `citations/ref.bib` exists if you plan to cite; use only existing keys.
- [ ] Remove all scaffold markers / repeated boilerplate.
