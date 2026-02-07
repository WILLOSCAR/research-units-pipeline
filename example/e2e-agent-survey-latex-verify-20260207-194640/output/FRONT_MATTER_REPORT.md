# Front matter report

- Status: PASS
- Draft profile: `survey`
- Evidence mode: `abstract`

## Outputs

- `sections/abstract.md` (has `## Abstract`)
- `sections/S1.md` (Introduction; body-only)
- `sections/S2.md` (Related Work; body-only)
- `sections/discussion.md` (has `## Discussion`)
- `sections/conclusion.md` (has `## Conclusion`)

## Checks (gate-aligned)

- Introduction (`sections/S1.md`)
  - unique citations: 35 (min=35)
  - substantive paragraphs (>=200 chars, non-bullets): 10 (min=8)
  - length after removing citations: 6184 chars (min=3200)
- Related Work (`sections/S2.md`)
  - unique citations: 52 (min=50)
  - substantive paragraphs (>=200 chars, non-bullets): 12 (min=10)
  - length after removing citations: 7133 chars (min=3800)

## Methodology note

- Location: Introduction (`sections/S1.md`)
- Content: candidate pool size (1,800), core set size (300), evidence level (abstract/metadata)
- Duplication: not repeated in Related Work

