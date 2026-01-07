from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--min-freq", type=int, default=3)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import candidate_keywords, dump_yaml, parse_semicolon_list, tokenize

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["papers/core_set.csv"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/taxonomy.yml"]

    core_path = workspace / inputs[0]
    out_path = workspace / outputs[0]

    if not core_path.exists():
        raise SystemExit(f"Missing core set: {core_path}")

    # Never overwrite non-placeholder user work.
    if out_path.exists() and out_path.stat().st_size > 0:
        existing = out_path.read_text(encoding="utf-8", errors="ignore")
        if not _is_placeholder(existing):
            return 0

    if _looks_like_llm_agent_topic(workspace):
        dump_yaml(out_path, _llm_agent_taxonomy_scaffold())
        return 0

    titles: list[str] = []
    with core_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            title = str(row.get("title") or "").strip()
            if title:
                titles.append(title)

    top_topics = candidate_keywords(titles, top_k=int(args.top_k), min_freq=int(args.min_freq))
    if not top_topics:
        top_topics = ["methods", "evaluation", "applications"]

    taxonomy: list[dict[str, Any]] = []
    for token in top_topics[:8]:
        subset = [t for t in titles if token in set(tokenize(t))]
        sub = candidate_keywords(subset, top_k=6, min_freq=1)
        sub = [s for s in sub if s not in {"overview", "benchmarks", "open", "problems"}]
        if not sub:
            sub = ["problem setting", "representative approaches", "evaluation", "failure modes"]
        taxonomy.append(
            {
                "name": _pretty(token),
                "description": f"TODO: define this category (seed token: {token}).",
                "children": [{"name": _pretty(st), "description": f"TODO: define subtopic (seed token: {st})."} for st in sub[:6]],
            }
        )

    if all(not item.get("children") for item in taxonomy):
        raise SystemExit("Failed to build a 2-level taxonomy scaffold")

    dump_yaml(out_path, taxonomy)
    return 0


def _pretty(token: str) -> str:
    token = token.replace("_", " ").replace("-", " ").strip()
    return " ".join([w[:1].upper() + w[1:] for w in token.split() if w])


def _looks_like_llm_agent_topic(workspace: Path) -> bool:
    queries_path = workspace / "queries.md"
    goal_path = workspace / "GOAL.md"
    text = ""
    if queries_path.exists():
        text += "\n" + queries_path.read_text(encoding="utf-8", errors="ignore")
    if goal_path.exists():
        text += "\n" + goal_path.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()
    return ("agent" in low or "agents" in low) and ("llm" in low or "language model" in low)


def _llm_agent_taxonomy_scaffold() -> list[dict[str, Any]]:
    return [
        {
            "name": "Agent Design & Architectures",
            "description": "TODO: define what belongs here (agent loop, tool calls, memory, control flow).",
            "children": [
                {"name": "ReAct and planning", "description": "TODO: scope + mechanisms + representative works."},
                {"name": "Tool use and orchestration", "description": "TODO: tool interface + routing/execution + safety."},
                {"name": "Memory and retrieval (RAG)", "description": "TODO: memory types + retrieval + context policies."},
                {"name": "Long-horizon control flow", "description": "TODO: hierarchical control + branching + reliability."},
                {"name": "Multi-agent systems", "description": "TODO: coordination + communication + role specialization."},
            ],
        },
        {
            "name": "Learning & Adaptation",
            "description": "TODO: how agents are trained/adapted (SFT/RL/prompt optimization/reflection).",
            "children": [
                {"name": "Agent tuning and alignment", "description": "TODO: tuning targets + data + constraints."},
                {"name": "Reinforcement learning for agents", "description": "TODO: RL setups + environments + stability concerns."},
                {"name": "Prompt optimization", "description": "TODO: search/optimization methods + evaluation."},
                {"name": "Reflection and self-improvement", "description": "TODO: reflection loops + memory/rules + failure modes."},
            ],
        },
        {
            "name": "Evaluation & Benchmarks",
            "description": "TODO: benchmark families + metrics + common pitfalls/leakage.",
            "children": [
                {"name": "Agent benchmarks", "description": "TODO: long-horizon/task suites + metrics."},
                {"name": "Tool-use benchmarks", "description": "TODO: interfaces + chain eval + recovery metrics."},
                {"name": "Web/enterprise tasks", "description": "TODO: environments + constraints + reproducibility."},
            ],
        },
        {
            "name": "Safety, Security & Governance",
            "description": "TODO: threat models + defenses + governance considerations.",
            "children": [
                {"name": "Vulnerabilities and attacks", "description": "TODO: attacks + surfaces + evaluation."},
                {"name": "Guardrails and mitigations", "description": "TODO: guardrails + trade-offs + failure cases."},
                {"name": "Secure tool orchestration", "description": "TODO: permission models + isolation + monitoring."},
            ],
        },
        {
            "name": "Applications & Case Studies",
            "description": "TODO: key application families and what qualifies as an agent system.",
            "children": [
                {"name": "Software engineering agents", "description": "TODO: workflows + tooling + metrics."},
                {"name": "Data/analysis agents", "description": "TODO: data tools + evaluation."},
                {"name": "Cybersecurity agents", "description": "TODO: dual-use risks + constraints + eval."},
            ],
        },
    ]


def _is_placeholder(text: str) -> bool:
    text = (text or "").strip().lower()
    if not text:
        return True
    if "(placeholder)" in text:
        return True
    if "todo" in text:
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())

