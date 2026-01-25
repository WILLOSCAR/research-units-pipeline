# Queries

> 写检索式（关键词/时间窗/排除词），并记录每次检索的变体与原因。

## Primary query
- keywords:
  # Prefer broader, arXiv-native boolean queries for A150++ pool size.
  # (The pipeline output format is LaTeX; do not search for the word "latex".)
  - 'all:agent AND (all:LLM OR all:"large language model" OR all:"language model")'
  - 'all:agent AND (all:tool OR all:"function calling" OR all:"tool use" OR all:"tool-using")'
  - 'all:"large language model" AND (all:tool OR all:"function calling")'
  - 'all:agent AND (all:planning OR all:memory OR all:reasoning)'
  # Add canonical anchors / named lines of work (helps ranking + later positioning).
  - "LLM agent"
  - "language model agent"
  - "tool-using agent"
  - "ReAct"
  - "Toolformer"
  - "Reflexion"
  - "AutoGPT"
  - "Voyager"
  - "Tree of Thoughts"
- exclude:
  - "agent-based modeling"
  - "react hooks"
  - "perovskite"
  - "banach"
  - "coxeter"

# Retrieval + scaling knobs
- max_results: "1800"        # retrieval cap per query bucket (A150++ default; raise if you have many buckets)
- core_size: "300"           # dedupe-rank will select this many papers into papers/core_set.csv (A150++ default)
- per_subsection: "28"       # section-mapper target papers per H3 (A150++ default; ensures wide in-scope cite pools)

# Citation-scope flexibility
- global_citation_min_subsections: "4"  # treat citations mapped to >=N subsections as globally allowed (tighten when per_subsection is high)

# Writing contract
- draft_profile: survey      # survey | deep (default: survey deliverable; global unique cites target >=150)

# Metadata enrichment
- enrich_metadata: ""        # true|false; optional arXiv id_list backfill for offline imports (needs network)

# Evidence strength
- evidence_mode: "abstract"  # abstract | fulltext (A150++ default: abstract-only; fulltext is optional and heavier)
- fulltext_max_papers: ""
- fulltext_max_pages: ""
- fulltext_min_chars: ""

# Optional time window
- time window:
  - from: ""
  - to: ""

## Notes
- (fill) scope decisions / dataset constraints
