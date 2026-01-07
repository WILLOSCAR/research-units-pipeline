---
name: outline-builder
description: Convert a taxonomy (`outline/taxonomy.yml`) into a bullet-only outline (`outline/outline.yml`) with sections/subsections and at least 3 bullets per subsection. Use when preparing structure (NO PROSE) before mapping papers or writing.
---

# Outline Builder

Convert a taxonomy into a **checkable, mappable outline** (bullets only).

Bullets should describe *what the section must cover*, not draft prose.

## When to use

- You have a taxonomy and need an outline for mapping papers and building evidence.
- You want each subsection to have concrete “coverage requirements” (axes, comparisons, evaluation).

## When not to use

- You already have an approved outline (don’t rewrite for style).

## Input

- `outline/taxonomy.yml`

## Output

- `outline/outline.yml`

## Workflow (heuristic)

1. Translate taxonomy nodes into section headings that read like a survey structure.
2. For each subsection, write **≥3 bullets** that are:
   - topic-specific (names of mechanisms, tasks, benchmarks, failure modes)
   - checkable (someone can verify whether the subsection covered it)
   - useful for mapping (papers can be assigned to each bullet/axis)
3. Prefer bullets that force synthesis later:
   - “Compare X vs Y along axes A/B/C”
   - “What evaluation setups are standard, and what they miss”
   - “Where methods fail (latency, tool errors, jailbreaks, reward hacking…)”

## Quality checklist

- [ ] `outline/outline.yml` exists and is bullets-only (no paragraphs).
- [ ] Every subsection has ≥3 non-generic bullets.
- [ ] Bullets are not copy-pasted templates across subsections.

## Common failure modes (and fixes)

- **Template bullets everywhere** → replace with domain terms + evaluation axes specific to that subsection.
- **Bullets too vague** (“Discuss limitations”) → name *which* limitations and *how to test* them.
- **Outline too flat/too deep** → aim for sections a reader can navigate (usually 6–10 sections, 2–5 subsections each).

## Helper script (optional)

Bootstrap scaffold only:
- Run `python .codex/skills/outline-builder/scripts/run.py --help` first.
- Then: `python .codex/skills/outline-builder/scripts/run.py --workspace <workspace_dir>`

The script creates `TODO` bullets and never overwrites non-placeholder work; in `pipeline.py --strict` it will be blocked until `TODO`s are replaced with topic-specific bullets.
