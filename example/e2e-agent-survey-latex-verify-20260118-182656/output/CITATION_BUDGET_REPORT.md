# Citation budget report

- Draft: `output/DRAFT.md`
- Bib entries: 220
- Draft unique citations: 57
- Draft profile: `lite`

- Global target (pipeline-auditor): >= 66
- Gap: 9

## Per-H3 suggestions (unused global keys, in-scope)

| H3 | title | unique cites | unused in selected | unused in mapped | suggested keys (add 3–6) |
|---|---|---:|---:|---:|---|
| 3.1 | Agent loop and action spaces | 10 | 0 | 8 | `Li2025From`, `Ghose2025Orfs`, `Song2026Envscaler`, `Wu2025Meta`, `You2025Datawiseagent`, `Xu2025Exemplar` |
| 3.2 | Tool interfaces and orchestration | 8 | 0 | 6 | `Cheng2025Your`, `Ghose2025Orfs`, `Xuan2026Confidence`, `Li2024Personal`, `Li2024Stride`, `Xian2025Measuring` |
| 4.1 | Planning and reasoning loops | 10 | 0 | 8 | `Silva2025Agents`, `Hatalis2025Review`, `Lu2025Pilotrl`, `Huang2025Surgical`, `Hu2025Evaluating`, `Yang2025Coarse` |
| 4.2 | Memory and retrieval (RAG) | 8 | 0 | 10 | `Hu2025Evaluating`, `Yu2026Agentic`, `Xia2025From`, `Zhang2025Large`, `Wu2025Meta`, `Ye2025Taska` |
| 5.1 | Self-improvement and adaptation | 10 | 0 | 7 | `Xia2025Sand`, `Sarukkai2025Context`, `Chen2025Grounded`, `He2025Enabling`, `Schneider2025Learning`, `Wang2025Ragen` |
| 5.2 | Multi-agent coordination | 9 | 0 | 9 | `Papadakis2025Atlas`, `Wu2025Agents`, `Chang2025Alas`, `Zhang2025Cognitive`, `Hassouna2024Agent`, `Li2025Draft` |
| 6.1 | Benchmarks and evaluation protocols | 9 | 0 | 9 | `Ji2025Taxonomy`, `Li2024Personal`, `Zhan2025Sentinel`, `Dagan2024Plancraft`, `Zhu2025Where`, `Lidayan2025Abbel` |
| 6.2 | Safety, security, and governance | 8 | 0 | 9 | `Gasmi2025Bridging`, `Hadeliya2025When`, `Luo2025Agrail`, `Sha2025Agent`, `An2025Ipiguard`, `Liu2026Agents` |

## How to apply (NO NEW FACTS)

- Prefer adding cite-embedding sentences that do not change claims:
  - `Representative systems include X [@a], Y [@b], and Z [@c].`
  - `Recent work spans A [@a] and B [@b], with further variants in C [@c].`
- Keep additions inside the same H3 (no cross-subsection citation drift).
- After editing citations, rerun: `section-merger` → `draft-polisher` → `global-reviewer` → `pipeline-auditor`.
