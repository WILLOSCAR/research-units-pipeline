from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import dump_yaml, load_yaml, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["outline/taxonomy.yml"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/outline.yml"]

    taxonomy_path = workspace / inputs[0]
    out_path = workspace / outputs[0]

    taxonomy = load_yaml(taxonomy_path) if taxonomy_path.exists() else None
    if not isinstance(taxonomy, list) or not taxonomy:
        raise SystemExit(f"Invalid taxonomy in {taxonomy_path}")

    # Never overwrite non-placeholder user work.
    if out_path.exists() and out_path.stat().st_size > 0:
        existing = out_path.read_text(encoding="utf-8", errors="ignore")
        if not _is_placeholder(existing):
            return 0

    outline: list[dict[str, Any]] = [
        {
            "id": "1",
            "title": "Introduction",
            "bullets": [
                "TODO: motivation + problem setting (why now)",
                "TODO: definitions + scope/non-goals (per DECISIONS.md)",
                "TODO: coverage note (data sources/time window/inclusion)",
                "TODO: high-level taxonomy + how to read this survey",
                "TODO: contributions + key open problems (high-level)",
            ],
        }
    ]

    section_no = 2
    for topic in taxonomy:
        if not isinstance(topic, dict):
            continue
        name = str(topic.get("name") or "").strip() or f"Topic {section_no}"
        children = topic.get("children") or []
        section_id = str(section_no)
        section: dict[str, Any] = {"id": section_id, "title": name, "subsections": []}

        subsection_no = 1
        for child in children if isinstance(children, list) else []:
            if not isinstance(child, dict):
                continue
            child_name = str(child.get("name") or "").strip() or f"Subtopic {section_id}.{subsection_no}"
            subsection_id = f"{section_id}.{subsection_no}"
            section["subsections"].append(
                {
                    "id": subsection_id,
                    "title": child_name,
                    "bullets": [
                        f"TODO: define terminology/problem setting for {child_name}",
                        f"TODO: identify 2–4 representative mechanisms/design choices for {child_name}",
                        f"TODO: list evaluation setups/benchmarks/metrics used for {child_name}",
                        f"TODO: failure modes/limitations/open problems specific to {child_name}",
                    ],
                }
            )
            subsection_no += 1

        outline.append(section)
        section_no += 1

    dump_yaml(out_path, outline)
    return 0


def _is_placeholder(text: str) -> bool:
    text = (text or "").strip().lower()
    if not text:
        return True
    if "(placeholder)" in text:
        return True
    if "todo" in text:
        return True
    if re.search(r"(?m)^\s*#\s*outline\s*\(placeholder\)", text):
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
