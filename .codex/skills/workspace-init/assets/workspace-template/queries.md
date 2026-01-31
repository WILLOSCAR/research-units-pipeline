# Queries

> 写检索式（关键词/时间窗/排除词），并记录每次检索的变体与原因。

## Primary query
- keywords:
  - ""
  - ""
- exclude:
  - ""

# Retrieval + scaling knobs
- max_results: "1800"        # retrieval cap per query bucket (A150++ default; raise if you have many buckets)
- core_size: "300"           # dedupe-rank will select this many papers into papers/core_set.csv (A150++ default)
- per_subsection: "28"       # section-mapper target papers per H3 (A150++ default; ensures wide in-scope cite pools)

# Citation-scope flexibility
- global_citation_min_subsections: "4"  # treat citations mapped to >=N subsections as globally allowed (tighten when per_subsection is high)

# Writing contract
- draft_profile: survey      # survey | deep (default: survey deliverable; hard>=150, rec>=165 when core_size=300)

# Global citation target policy
- citation_target: "recommended"  # recommended | hard (A150++ default: recommended; forces injection to close the rec gap)

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
