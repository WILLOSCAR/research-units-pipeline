from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--min-freq", type=int, default=2)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import candidate_keywords, dump_yaml, parse_semicolon_list, read_jsonl, tokenize

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["papers/papers_dedup.jsonl"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/taxonomy.yml"]

    in_path = workspace / inputs[0]
    out_path = workspace / outputs[0]

    records = read_jsonl(in_path)
    if not records:
        raise SystemExit(f"No deduped papers found: {in_path}")

    survey_like = []
    for rec in records:
        title = str(rec.get("title") or "").lower()
        abstract = str(rec.get("abstract") or "").lower()
        if "survey" in title or "review" in title or "survey" in abstract or "review" in abstract:
            survey_like.append(rec)

    seed_records = survey_like or records
    titles = [str(r.get("title") or "").strip() for r in seed_records if str(r.get("title") or "").strip()]

    top_topics = candidate_keywords(titles, top_k=int(args.top_k), min_freq=int(args.min_freq))
    if not top_topics:
        top_topics = ["methods", "evaluation", "applications"]

    taxonomy = []
    for token in top_topics[:6]:
        subset = [t for t in titles if token in set(tokenize(t))]
        sub = candidate_keywords(subset, top_k=5, min_freq=1)
        if not sub:
            sub = ["overview", "representative-approaches", "benchmarks", "open-problems"]
        taxonomy.append(
            {
                "name": _pretty(token),
                "description": f"Seeded from survey/review signals for '{token}'.",
                "children": [{"name": _pretty(st), "description": f"Seed topic '{st}' under '{token}'."} for st in sub[:6]],
            }
        )

    dump_yaml(out_path, taxonomy)
    return 0


def _pretty(token: str) -> str:
    token = token.replace("_", " ").replace("-", " ").strip()
    return " ".join([w[:1].upper() + w[1:] for w in token.split() if w])


if __name__ == "__main__":
    raise SystemExit(main())

