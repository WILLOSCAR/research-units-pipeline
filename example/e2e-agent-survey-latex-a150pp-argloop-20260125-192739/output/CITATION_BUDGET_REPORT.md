# Citation budget report

- Status: FAIL
- Draft: `output/DRAFT.md`
- Bib entries: 300
- Draft unique citations: 95
- Draft profile: `survey`

- Global target (hard; blocking): >= 150 (struct=147, hard_frac=150, bib=300)
- Gap: 55
- Global recommended target (non-blocking): >= 165 (rec_frac=165, bib=300)
- Gap to recommended: 70
- Suggested keys per H3 (sizing): 9

## Per-H3 suggestions (unused global keys, in-scope)

| H3 | title | unique cites | unused in selected | unused in mapped | suggested keys (add 6-9) |
|---|---|---:|---:|---:|---|
| 3.1 | Agent loop and action spaces | 12 | 2 | 6 | `Nusrat2025Automated`, `Li2025What`, `Kulkarni2025Agent`, `Maranto2024Llmsat`, `Yu2023Finmem`, `Wu2025Meta`, `Liu2025Aligning`, `Lindenbauer2025Complexity`, `Li2024Personal` |
| 3.2 | Tool interfaces and orchestration | 14 | 1 | 5 | `Wang2024Mllm`, `Yin2025Infobid`, `Zhu2024Menti`, `Zhou2024Archer`, `Wang2024Learning`, `Li2024Personal`, `Kulkarni2025Agent`, `Li2025What`, `Lindenbauer2025Complexity` |
| 4.1 | Planning and reasoning loops | 14 | 4 | 6 | `Shi2024Ehragent`, `Huang2025Surgical`, `Zhou2023Navgpt`, `Hatalis2025Review`, `Lu2025Pilotrl`, `Motwani2024Malt`, `Bai2024Twostep`, `Kiruluta2025Novel`, `Zhao2024Lightva` |
| 4.2 | Memory and retrieval (RAG) | 12 | 8 | 7 | `Verma2026Active`, `Yu2026Agentic`, `Liu2025Echo`, `Ye2025Task`, `Li2025Graphcodeagent`, `Liu2023Reason`, `Chiang2024Llamp`, `Lu2025Youtu`, `Zhang2024Survey` |
| 5.1 | Self-improvement and adaptation | 12 | 10 | 6 | `Xia2025Sand`, `Samaei2025Epidemiqs`, `Liu2025Powered`, `Chen2025Grounded`, `Belle2025Agents`, `Wu2024Federated`, `Bharadwaj2025Omnireflect`, `Mou2024From`, `Zhang2024Affective` |
| 5.2 | Multi-agent coordination | 12 | 8 | 5 | `Xu2025Autonomous`, `Ye2025Cognipair`, `Xu2023Magic`, `Rouzrokh2025Lattereview`, `Zahedifar2025Agent`, `Xu2023Towards`, `Trirat2024Automl`, `Chen2024Solving`, `Wu2025Multi` |
| 6.1 | Benchmarks and evaluation protocols | 16 | 7 | 3 | `Kim2026Beyond`, `Chen2025Towards`, `Rahman2025Hallucination`, `Zhang2024Large`, `Qi2024Large`, `Tang2025Empowering`, `Zhu2025Evolutionary`, `Wu2025Lessons`, `Agrawal2025Language` |
| 6.2 | Safety, security, and governance | 12 | 7 | 6 | `Marandi2025Complex`, `Kang2025Acon`, `VarangotReille2025Doing`, `Wang2025Comprehensive`, `Henke2025Autopentest`, `Hadeliya2025When`, `Rosario2025Architecting`, `Sun2024Survey`, `Liu2025Secure` |

## How to apply (NO NEW FACTS)

- Prefer cite-embedding edits that do not change claims (paraphrase; avoid repeated stems):
  - Axis-anchored exemplars: `... as seen in X [@a] and Y [@b] ...; Z [@c] illustrates a contrasting design point.`
  - Parenthetical grounding (low risk): `... (e.g., X [@a], Y [@b], Z [@c]).`
  - Contrast pointer: `While some systems emphasize <A> (X [@a]; Y [@b]), others emphasize <B> (Z [@c]).`
- Avoid budget-dump voice (high-signal automation tells): `Representative systems include ...`, `Notable lines of work include ...`.
- Keep additions inside the same H3 (no cross-subsection citation drift).
- Apply via `citation-injector` (LLM-first) and then rerun: `draft-polisher` → `global-reviewer` → `pipeline-auditor`.
