# Citation budget report

- Draft: `output/DRAFT.md`
- Bib entries: 220
- Draft unique citations: 76
- Draft profile: `lite`

- Global target (pipeline-auditor): >= 66
- Gap: 0

## Per-H3 suggestions (unused global keys, in-scope)

| H3 | title | unique cites | unused in selected | unused in mapped | suggested keys (add 3–6) |
|---|---|---:|---:|---:|---|
| 3.1 | Agent loop and action spaces | 12 | 2 | 2 | `Feng2025Group`, `Lin2026Froav`, `Wu2025Meta`, `Nusrat2025Automated`, `Bulusu2024Mathviz`, `Chen2025Agentguard` |
| 3.2 | Tool interfaces and orchestration | 9 | 1 | 5 | `Bulusu2024Mathviz`, `Chen2025Agentguard`, `Cheng2025Your`, `Jia2025Autotool`, `Cui2025Toward`, `Fu2024Imprompter` |
| 4.1 | Planning and reasoning loops | 8 | 3 | 5 | `Wang2025Automated`, `Zhou2025Reasoning`, `Nusrat2025Automated`, `Hong2025Planning`, `Hatalis2025Review`, `Kiruluta2025Novel` |
| 4.2 | Memory and retrieval (RAG) | 8 | 4 | 5 | `Zhang2024Large`, `Zhang2025Large`, `Lin2026Froav`, `Ye2025Task`, `Wu2025Meta`, `Xu2025Agentic` |
| 5.1 | Self-improvement and adaptation | 8 | 3 | 5 | `Sarukkai2025Context`, `Shao2025Towards`, `Xia2025Sand`, `Belle2025Agents`, `Xi2025Agentprm`, `Zhou2024Archer` |
| 5.2 | Multi-agent coordination | 8 | 2 | 4 | `Cui2025Toward`, `Chang2025Alas`, `Hao2025Multi`, `Li2025What`, `Yim2024Evaluating`, `Wang2023Voyager` |
| 6.1 | Benchmarks and evaluation protocols | 10 | 2 | 4 | `Ma2023Large`, `Guo2025Cryptobench`, `Dagan2024Plancraft`, `Zhang2025Buildbench`, `Liang2026Large`, `Liu2025Secure` |
| 6.2 | Safety, security, and governance | 10 | 1 | 7 | `Shao2025Towards`, `Fang2025Should`, `Luo2025Agrail`, `Li2024Personal`, `Hadeliya2025When`, `Sha2025Agent` |

## How to apply (NO NEW FACTS)

- Prefer adding cite-embedding sentences that do not change claims:
  - `Representative systems include X [@a], Y [@b], and Z [@c].`
  - `Recent work spans A [@a] and B [@b], with further variants in C [@c].`
- Keep additions inside the same H3 (no cross-subsection citation drift).
- After editing citations, rerun: `section-merger` → `draft-polisher` → `global-reviewer` → `pipeline-auditor`.
