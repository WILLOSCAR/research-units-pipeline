from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def _choose_synthesis_mode(*, sec_id: str, sec_title: str, axes: list[str]) -> tuple[str, list[str]]:
    """Pick a synthesis mode to avoid repeating the same chapter-ending template everywhere (NO NEW FACTS)."""
    title_low = (sec_title or "").lower()
    axes_low = " ".join([str(a or "").lower() for a in (axes or [])])

    if any(k in title_low for k in ["evaluation", "benchmark", "metrics", "measurement"]) or any(k in axes_low for k in ["evaluation", "benchmark", "metrics"]):
        return (
            "tradeoff_matrix",
            [
                "Synthesize by comparing approaches along a small trade-off matrix (axes + evaluation protocol), not by listing papers.",
                "Keep contrasts decision-relevant (reliability/cost/safety) and reuse consistent evaluation anchors across H3s.",
            ],
        )
    if any(k in title_low for k in ["history", "evolution", "timeline", "trend"]):
        return (
            "timeline",
            [
                "Synthesize via a lightweight evolution story (what changed in assumptions/interfaces/evaluation over time).",
                "Use the timeline to motivate why later H3s focus on different constraints.",
            ],
        )
    if any(k in title_low for k in ["security", "safety", "attack", "defense", "risk", "robust"]) or any(k in axes_low for k in ["safety", "security", "risk"]):
        return (
            "tension_resolution",
            [
                "Synthesize as a tension-resolution arc (capability vs safety/reliability) and how approaches resolve or shift that tension.",
                "Make the failure modes concrete and connect them to evaluation protocols and mitigations.",
            ],
        )

    # Deterministic fallback: cycle a couple of modes to increase diversity across chapters.
    try:
        idx = int(str(sec_id or "0").strip())
    except Exception:
        idx = 0
    if idx % 3 == 0:
        return (
            "case_study",
            [
                "Synthesize by anchoring the chapter around 1–2 representative system case studies and using H3s as axes of analysis.",
                "Ensure the case studies only use papers already mapped to this chapter (no new citations).",
            ],
        )
    return (
        "clusters",
        [
            "Synthesize by contrasting 2–3 clusters of approaches and making the trade-offs explicit (not a per-paper summary).",
            "Use explicit connectors (however/therefore/building on) to keep paragraphs from becoming islands.",
        ],
    )


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

    from tooling.common import (
        ensure_dir,
        load_yaml,
        now_iso_seconds,
        parse_semicolon_list,
        read_jsonl,
        write_jsonl,
    )

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or [
        "outline/outline.yml",
        "outline/subsection_briefs.jsonl",
        "GOAL.md",
    ]
    outputs = parse_semicolon_list(args.outputs) or ["outline/chapter_briefs.jsonl"]

    outline_path = workspace / inputs[0]
    briefs_path = workspace / inputs[1]
    goal_path = workspace / (inputs[2] if len(inputs) >= 3 else "GOAL.md")
    out_path = workspace / outputs[0]

    freeze_marker = out_path.parent / "chapter_briefs.refined.ok"
    if out_path.exists() and out_path.stat().st_size > 0 and freeze_marker.exists():
        return 0

    outline = load_yaml(outline_path) if outline_path.exists() else None
    if not isinstance(outline, list) or not outline:
        raise SystemExit(f"Invalid outline: {outline_path}")

    briefs = read_jsonl(briefs_path)
    if not briefs:
        raise SystemExit(f"Missing or empty subsection briefs: {briefs_path}")

    briefs_by_sub: dict[str, dict[str, Any]] = {}
    for rec in briefs:
        if not isinstance(rec, dict):
            continue
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            briefs_by_sub[sid] = rec

    goal = _read_goal(goal_path)

    records: list[dict[str, Any]] = []
    for sec in outline:
        if not isinstance(sec, dict):
            continue
        sec_id = str(sec.get("id") or "").strip()
        sec_title = str(sec.get("title") or "").strip()
        subs = sec.get("subsections") or []
        if not (sec_id and sec_title and isinstance(subs, list) and subs):
            continue

        sub_list: list[dict[str, str]] = []
        bridge_terms: list[str] = []
        contrast_hooks: list[str] = []
        axes: list[str] = []

        for sub in subs:
            if not isinstance(sub, dict):
                continue
            sub_id = str(sub.get("id") or "").strip()
            sub_title = str(sub.get("title") or "").strip()
            if not sub_id or not sub_title:
                continue
            sub_list.append({"sub_id": sub_id, "title": sub_title})

            brief = briefs_by_sub.get(sub_id) or {}
            for t in brief.get("bridge_terms") or []:
                t = str(t or "").strip()
                if t and t not in bridge_terms:
                    bridge_terms.append(t)
            hook = str(brief.get("contrast_hook") or "").strip()
            if hook and hook not in contrast_hooks:
                contrast_hooks.append(hook)
            for a in brief.get("axes") or []:
                a = str(a or "").strip()
                if a and a not in axes:
                    axes.append(a)

        throughline: list[str] = []
        if axes:
            for a in axes[:6]:
                throughline.append(f"Compare approaches along: {a}.")
        else:
            throughline.append("Define the chapter’s organizing comparisons (mechanism / evaluation / limitations).")

        if goal:
            throughline.insert(0, f"Pin scope to goal: {goal}.")

        key_contrasts = [c for c in contrast_hooks if c]
        if not key_contrasts:
            key_contrasts = ["Pick 2–4 cross-subsection contrasts (A vs B) grounded in mapped papers."]

        synthesis_mode, synthesis_preview = _choose_synthesis_mode(sec_id=sec_id, sec_title=sec_title, axes=axes)

        lead_plan = [
            "Para 1: state the chapter’s role and the decision-relevant comparison axes (no new facts).",
            "Para 2: preview the H3 subsections and how they decompose the chapter question.",
            "Para 3 (optional): highlight evaluation anchors + recurrent limitations that will recur across H3s.",
        ]

        records.append(
            {
                "section_id": sec_id,
                "section_title": sec_title,
                "subsections": sub_list,
                "synthesis_mode": synthesis_mode,
                "synthesis_preview": synthesis_preview[:2],
                "throughline": throughline[:6],
                "key_contrasts": key_contrasts[:6],
                "lead_paragraph_plan": lead_plan,
                "bridge_terms": bridge_terms[:12],
                "generated_at": now_iso_seconds(),
            }
        )

    ensure_dir(out_path.parent)
    _check_no_placeholders(records)
    write_jsonl(out_path, records)
    return 0


def _read_goal(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-", ">", "<!--")):
            continue
        low = line.lower()
        if "写一句话" in line or "fill" in low:
            continue
        return line
    return ""


def _check_no_placeholders(records: list[dict[str, Any]]) -> None:
    raw = json.dumps(records, ensure_ascii=False)
    low = raw.lower()
    if "…" in raw:
        raise SystemExit("chapter_briefs contains ellipsis placeholder")
    if "(placeholder)" in low:
        raise SystemExit("chapter_briefs contains placeholder markers")
    if re.search(r"(?i)\b(?:todo|tbd|fixme)\b", raw):
        raise SystemExit("chapter_briefs contains TODO/TBD/FIXME")


if __name__ == "__main__":
    raise SystemExit(main())
