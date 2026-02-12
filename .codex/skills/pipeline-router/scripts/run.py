from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--checkpoint", default="C0")
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import ensure_decisions_approval_checklist, seed_queries_from_topic, upsert_checkpoint_block

    workspace = Path(args.workspace).resolve()
    checkpoint = str(args.checkpoint).strip() or "C0"

    goal = _read_goal(workspace)
    pipeline = _read_pipeline_lock(workspace)

    decisions_path = workspace / "DECISIONS.md"
    ensure_decisions_approval_checklist(decisions_path)

    if checkpoint == "C0":
        _kickoff(decisions_path, goal=goal, pipeline=pipeline, workspace=workspace)
        seed_queries_from_topic(workspace / "queries.md", goal)
        return 0

    if checkpoint == "C2":
        block = _c2_review_block(workspace, pipeline=pipeline)
        upsert_checkpoint_block(decisions_path, "C2", block)
        return 0

    upsert_checkpoint_block(
        decisions_path,
        checkpoint,
        f"## {checkpoint} checkpoint\n\n- Please review artifacts and tick `Approve {checkpoint}` above.\n",
    )
    return 0


def _read_goal(workspace: Path) -> str:
    goal_path = workspace / "GOAL.md"
    if not goal_path.exists():
        return ""
    for line in goal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-", ">", "<!--")):
            continue
        low = line.lower()
        if "写一句话描述" in line or "fill" in low:
            continue
        return line
    return ""


def _read_pipeline_lock(workspace: Path) -> str:
    lock_path = workspace / "PIPELINE.lock.md"
    if not lock_path.exists():
        return ""
    for line in lock_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("pipeline:"):
            return line.split("pipeline:", 1)[1].strip()
    return ""


def _kickoff(decisions_path: Path, *, goal: str, pipeline: str, workspace: Path) -> None:
    from tooling.common import upsert_checkpoint_block

    ws_rel = _workspace_hint(workspace)
    goal_line = goal or "(fill your topic/goal in GOAL.md)"
    pipeline_line = pipeline or "(unknown pipeline; check PIPELINE.lock.md)"

    block = "\n".join(
        [
            f"## Kickoff — {goal_line}",
            "",
            f"- Pipeline: `{pipeline_line}`",
            f"- Workspace: `{ws_rel}`",
            f"- Workspace name: `{workspace.name}`",
            "",
            "Optional: confirm constraints (or reply \"你自己决定\" and we will proceed with best-effort defaults):",
            "- Deliverable: language (中文/英文), target length, audience, format (Markdown/LaTeX/PDF).",
            "- Evidence mode: `abstract` (no PDF download) vs `fulltext` (download+extract snippets).",
            "- Scope:",
            "  - In-scope.",
            "  - Out-of-scope.",
            "- Time window: from/to year (or no limit).",
            "- Search constraints: must-include systems/papers/keywords; hard excludes.",
            "- Human sign-off: who will approve required checkpoints in this file.",
            "",
            "Note:",
            "- The pipeline will pause at HUMAN checkpoints (see the Approvals checklist) and resume after approval.",
            "",
        ]
    )
    upsert_checkpoint_block(decisions_path, "C0", block)


def _workspace_hint(workspace: Path) -> str:
    repo_root = Path(__file__).resolve().parents[4]
    try:
        return str(workspace.relative_to(repo_root))
    except Exception:
        return str(workspace)


def _c2_review_block(workspace: Path, *, pipeline: str) -> str:
    # If this is ideation, C2 is "focus selection" (taxonomy-as-map), not survey outline approval.
    if "idea-finder" in (pipeline or ""):
        return _c2_idea_focus_block(workspace)

    taxonomy_path = workspace / "outline" / "taxonomy.yml"
    outline_path = workspace / "outline" / "outline.yml"
    mapping_path = workspace / "outline" / "mapping.tsv"

    taxonomy_summary = _summarize_taxonomy(taxonomy_path)
    outline_summary = _summarize_outline(outline_path)
    mapping_summary = _summarize_mapping(mapping_path)

    return "\n".join(
        [
            "## C2 review — scope + outline (NO PROSE)",
            "",
            taxonomy_summary,
            outline_summary,
            mapping_summary,
            "",
            "Decision:",
            "- Tick `Approve C2` in the approvals checklist above to proceed (evidence → citations → draft).",
            "",
        ]
    )


def _c2_idea_focus_block(workspace: Path) -> str:
    taxonomy_path = workspace / "outline" / "taxonomy.yml"
    brief_path = workspace / "output" / "IDEA_BRIEF.md"

    taxonomy_summary = _summarize_taxonomy(taxonomy_path)
    cluster_list = _list_taxonomy_clusters(taxonomy_path)

    brief_hint = "- Brief: (missing) `output/IDEA_BRIEF.md`" if not brief_path.exists() else "- Brief: `output/IDEA_BRIEF.md` (update focus + excludes if needed)"

    return "\n".join(
        [
            "## C2 focus — pick idea map clusters (NO PROSE)",
            "",
            taxonomy_summary,
            brief_hint,
            "",
            "### Candidate clusters (top-level)",
            cluster_list,
            "",
            "Decision:",
            "- Choose 1-2 focus clusters (by name) and 2-5 hard excludes.",
            "- Optionally update `output/IDEA_BRIEF.md` to reflect the chosen focus.",
            "- Tick `Approve C2` above to proceed (notes → idea pool → shortlist).",
            "",
        ]
    )


def _summarize_taxonomy(path: Path) -> str:
    if not path.exists():
        return "- taxonomy: (missing) `outline/taxonomy.yml`"
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except Exception as exc:
        return f"- taxonomy: (unreadable) {exc}"

    top = len(data) if isinstance(data, list) else 0
    leaves = 0
    if isinstance(data, list):
        for node in data:
            children = node.get("children") if isinstance(node, dict) else None
            if isinstance(children, list):
                leaves += len(children)
    return f"- taxonomy: top-level={top}, leaf-nodes={leaves}"


def _list_taxonomy_clusters(path: Path) -> str:
    if not path.exists():
        return "- (missing taxonomy)"
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except Exception as exc:
        return f"- (unreadable taxonomy) {exc}"

    if not isinstance(data, list) or not data:
        return "- (empty taxonomy)"

    lines: list[str] = []
    for node in data[:12]:
        if not isinstance(node, dict):
            continue
        name = str(node.get("name") or "").strip() or "(unnamed)"
        children = node.get("children") if isinstance(node.get("children"), list) else []
        n_children = len(children) if isinstance(children, list) else 0
        lines.append(f"- {name} (children={n_children})")
    if not lines:
        return "- (no readable clusters)"
    return "\n".join(lines)


def _summarize_outline(path: Path) -> str:
    if not path.exists():
        return "- outline: (missing) `outline/outline.yml`"
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except Exception as exc:
        return f"- outline: (unreadable) {exc}"

    sections = 0
    subsections = 0
    if isinstance(data, list):
        sections = len(data)
        for section in data:
            if isinstance(section, dict):
                subs = section.get("subsections") or []
                if isinstance(subs, list):
                    subsections += len(subs)
    return f"- outline: sections={sections}, subsections={subsections}"


def _summarize_mapping(path: Path) -> str:
    if not path.exists():
        return "- mapping: (missing) `outline/mapping.tsv`"
    try:
        import csv

        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            rows = [row for row in reader]
    except Exception as exc:
        return f"- mapping: (unreadable) {exc}"

    by_section: dict[str, int] = {}
    for row in rows:
        sid = (row.get("section_id") or "").strip()
        if not sid:
            continue
        by_section[sid] = by_section.get(sid, 0) + 1

    covered = sum(1 for _, n in by_section.items() if n >= 3)
    total = len(by_section)
    return f"- mapping: subsections_with_>=3_papers={covered}/{total}"


if __name__ == "__main__":
    raise SystemExit(main())
