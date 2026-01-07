---
name: taxonomy-builder
description: Build a 2+ level taxonomy (`outline/taxonomy.yml`) from a core paper set and scope constraints, with short descriptions per node. Use when structuring a survey/snapshot before any prose is written.
---

# Taxonomy Builder

Turn a core paper set into a **2+ level, mappable taxonomy** that will drive the outline and paper-to-section mapping.

This is *structure*, not writing: avoid prose paragraphs and avoid “generic placeholder” buckets.

## When to use

- You have a `papers/core_set.csv` and need a stable structure for a survey/snapshot.
- You want categories that are meaningful to readers (not just keyword clusters).

## When not to use

- You already have an approved taxonomy that maps well to your target narrative (don’t churn it).

## Inputs

- `papers/core_set.csv` (required)
- Optional: `papers/papers_dedup.jsonl` (to peek at abstracts/metadata)
- Optional: `DECISIONS.md` (scope constraints)

## Output

- `outline/taxonomy.yml`

## Workflow (heuristic)

1. Skim the core set and cluster by **reader-relevant axes**, not by surface keywords.
   - For LLM agents, common axes: control loop/architecture, tool use, planning & reasoning, memory/RAG, multi-agent coordination, evaluation/benchmarks, safety/security, applications.
2. Choose ~4–10 top-level nodes that feel like “chapters in a survey”.
3. For each top-level node, create 2–6 subtopics with **clear inclusion cues** (what belongs here, what doesn’t).
4. Write a short description for every node:
   - define what the bucket covers
   - name 2–5 representative paper IDs (or recognizable lines of work) that belong here
5. Sanity check:
   - leaves aren’t too tiny (ideally ≥3 papers per leaf)
   - names are mutually exclusive *enough* (some overlap is OK, confusion is not)

## Quality checklist

- [ ] `outline/taxonomy.yml` has ≥2 levels.
- [ ] Every node has a `description` with concrete meaning (not “Papers and ideas centered on …” boilerplate).
- [ ] Leaf nodes look mappable (not overly broad like “Misc/Other”).

## Common failure modes (and fixes)

- **Generic buckets** (“Overview/Benchmarks/Open Problems”) → rename to content-based subtopics.
- **Keyword clustering** → reframe as design/evaluation questions a reader would ask.
- **Too much overlap** → tighten inclusion cues; split a bucket by mechanism vs evaluation vs safety.

## Helper script (optional)

Bootstrap scaffold only:
- Run `python .codex/skills/taxonomy-builder/scripts/run.py --help` first.
- Then: `python .codex/skills/taxonomy-builder/scripts/run.py --workspace <workspace_dir>`

The script only creates a `TODO` scaffold and never overwrites non-placeholder work; in `pipeline.py --strict` it will be blocked until you replace all `TODO`s with real taxonomy definitions.
