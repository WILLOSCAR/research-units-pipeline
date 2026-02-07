# Citation budget report

- Status: FAIL
- Draft: `output/DRAFT.md`
- Bib entries: 300
- Draft unique citations: 123
- Draft profile: `survey`
- Citation target policy: `recommended`

- Global target (policy; blocking): >= 165 (struct=147, hard_frac=150, bib=300)
- Gap: 42
- Global hard minimum: >= 150 (struct=147, hard_frac=150, bib=300)
- Global recommended target: >= 165 (rec_frac=165, bib=300)
- Gap to recommended: 42
- Suggested keys per H3 (sizing): 6

## Per-H3 suggestions (unused global keys, in-scope)

| H3 | title | unique cites | unused in selected | unused in mapped | suggested keys (add 6-6) |
|---|---|---:|---:|---:|---|
| 3.1 | Agent loop and action spaces | 16 | 4 | 4 | `Zhuang2025Hephaestus`, `Zhu2025Agent`, `Yang2025Proagent`, `Miyamoto2026Agent`, `Kulkarni2025Agent`, `Tawosi2025Almas` |
| 3.2 | Tool interfaces and orchestration | 18 | 7 | 2 | `Fu2024Imprompter`, `Jeon2025Based`, `Gupta2024Codenav`, `Hao2026From`, `Wu2024Avatar`, `Yin2025Magnet` |
| 4.1 | Planning and reasoning loops | 21 | 5 | 2 | `Hu2025Training`, `Rawat2025Multi`, `Shi2024Ehragent`, `Zhang2025Multimind`, `Koubaa2025Agentic`, `Zhao2025Autonomous` |
| 4.2 | Memory and retrieval (RAG) | 21 | 4 | 1 | `Zhu2025Where`, `Wang2025Dsmentor`, `Zhang2024Large`, `Li2025Graphcodeagent`, `Wu2025Meta`, `Li2025Encouraging` |
| 5.1 | Self-improvement and adaptation | 21 | 6 | 1 | `Yu2025Infiagent`, `GendreauDistler2025Automating`, `Yang2025Bioverge`, `Samaei2025Epidemiqs`, `Yano2025Lamdagent`, `Zhang2024Autocoderover` |
| 5.2 | Multi-agent coordination | 16 | 6 | 1 | `Luo2025Large`, `Chen2025Remsa`, `Shi2025Youtu`, `Ji2025Tree`, `Du2024Text2Bim`, `Yu2025Infiagent` |
| 6.1 | Benchmarks and evaluation protocols | 18 | 5 | 3 | `Chen2025Towards`, `Liu2026Agents`, `Tao2025Code`, `V2026Agentic`, `Almeida2025Ticket`, `Zhang2025Detective` |
| 6.2 | Safety, security, and governance | 20 | 4 | 2 | `Zhang2024Agent`, `Sha2025Agent`, `Russo2025Deep`, `Luo2025Agrail`, `He2024Emerged`, `Hong2025Natural` |

## How to apply (NO NEW FACTS)

- Prefer cite-embedding edits that do not change claims (paraphrase; avoid repeated stems):
  - Axis-anchored exemplars: `... as seen in X [@a] and Y [@b] ...; Z [@c] illustrates a contrasting design point.`
  - Parenthetical grounding (low risk): `... (e.g., X [@a], Y [@b], Z [@c]).`
  - Contrast pointer: `While some systems emphasize <A> (X [@a]; Y [@b]), others emphasize <B> (Z [@c]).`
- Avoid budget-dump voice (high-signal automation tells): `Representative systems include ...`, `Notable lines of work include ...`.
- Keep additions inside the same H3 (no cross-subsection citation drift).
- Apply via `citation-injector` (LLM-first) and then rerun: `draft-polisher` → `global-reviewer` → `pipeline-auditor`.
