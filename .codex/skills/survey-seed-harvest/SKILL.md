---
name: survey-seed-harvest
description: Identify survey/review papers in a retrieved set and extract taxonomy seeds (topics, subtopics, standard terminology) into `outline/taxonomy.yml`. Use when bootstrapping a survey taxonomy from existing surveys/reviews.
---

# Survey Seed Harvest

Bootstrap taxonomy *seeds* from existing survey/review papers inside your retrieved set.

This is an accelerator for the early structure stage: it should make `taxonomy-builder` easier, not replace it.

## Inputs

- `papers/papers_dedup.jsonl` (deduped paper metadata with titles/abstracts)

## Outputs

- `outline/taxonomy.yml` (seed taxonomy; expected to be refined)

## Workflow (heuristic)

1. Find likely survey/review papers:
   - title/abstract contains “survey”, “review”, “systematic”, “meta-analysis”
2. Extract candidate topic terms and group them into:
   - ~4–10 top-level nodes (“chapters”)
   - 2–6 children per node (mappable leaves)
3. Write short, *actionable* descriptions:
   - what belongs here / what does not
   - (optional) list 2–5 representative titles as seeds
4. Treat the result as a starting point:
   - pass it to `taxonomy-builder` for domain-meaningful rewriting and scope alignment.

## Quality checklist

- [ ] `outline/taxonomy.yml` exists and is valid YAML.
- [ ] Taxonomy has at least 2 levels (`children` used) and every node has a description.
- [ ] Avoid generic placeholder nodes like “Overview/Benchmarks/Open Problems” unless they are truly content-based for your domain.

## Script (optional helper)

- Run `python .codex/skills/survey-seed-harvest/scripts/run.py --help` first.
- Then: `python .codex/skills/survey-seed-harvest/scripts/run.py --workspace <workspace_dir>`

This script is keyword-based and best treated as a seed generator; expect to refine the taxonomy with `taxonomy-builder`, especially in `pipeline.py --strict` mode.
