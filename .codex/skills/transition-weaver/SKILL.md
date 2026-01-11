---
name: transition-weaver
description: |
  Generate lightweight section/subsection transitions (NO NEW FACTS) to prevent “island” subsections; outputs a transition map that merging/writing can weave in.
  **Trigger**: transition weaver, weave transitions, coherence, 过渡句, 承接句, 章节连贯性.
  **Use when**: `outline/subsection_briefs.jsonl` exists and you want coherent flow before/after drafting (typically Stage C5).
  **Skip if**: `outline/transitions.md` exists and is refined (no placeholders).
  **Network**: none.
  **Guardrail**: do not add new factual claims or citations; transitions may only refer to titles/RQs/bridge terms already present in briefs.
---

# Transition Weaver

Purpose: produce a small, low-risk “transition map” so adjacent subsections do not read like islands.

Transitions should answer:
- what the previous subsection established
- what gap/tension remains
- why the next subsection follows

## Inputs

- `outline/outline.yml`
- `outline/subsection_briefs.jsonl` (expects `rq` + `bridge_terms` + `contrast_hook` when available)

## Outputs

- `outline/transitions.md`

## Roles (recommended)

- **Linker**: writes the transition logic using titles/RQs (no new facts).
- **Skeptic**: deletes any empty/templated transition and forces subsection-specific wording.

## Non-negotiables

- No new facts.
- No citations.
- No placeholders (`TODO`, `…`, `<!-- SCAFFOLD -->`).

## Helper script

- `python .codex/skills/transition-weaver/scripts/run.py --workspace <ws>`

## Troubleshooting

### Issue: transitions read like templates

**Symptom**:
- Many transitions share the same long sentence.

**Fix**:
- Ensure subsection briefs include `bridge_terms` + `contrast_hook` (regenerate `subsection-briefs`).
- Rerun transition weaving; quality gate blocks high repetition.
