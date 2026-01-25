from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_MOVES = {
    "claim",
    "definition_setup",
    "justification",
    "contrast",
    "boundary_failure",
    "local_conclusion",
}


def _iter_outline_h3_ids(outline: Any) -> list[str]:
    out: list[str] = []
    if not isinstance(outline, list):
        return out
    for sec in outline:
        if not isinstance(sec, dict):
            continue
        for sub in sec.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            sid = str(sub.get("id") or "").strip()
            title = str(sub.get("title") or "").strip()
            if sid and title:
                out.append(sid)
    return out


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    recs: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return recs
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if isinstance(obj, dict):
            recs.append(obj)
    return recs


def _parse_status(md: str) -> str:
    m = re.search(r"(?im)^\s*-\s*Status\s*:\s*(PASS|FAIL)\b", md or "")
    return (m.group(1) if m else "").strip().upper()


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

    from tooling.common import atomic_write_text, ensure_dir, load_yaml, parse_semicolon_list
    from tooling.quality_gate import QualityIssue, check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or "U10055").strip() or "U10055"

    inputs = parse_semicolon_list(args.inputs) or ["outline/outline.yml"]
    outputs = parse_semicolon_list(args.outputs) or [
        "output/ARGUMENT_SELFLOOP_TODO.md",
        "output/SECTION_ARGUMENT_SUMMARIES.jsonl",
        "output/ARGUMENT_SKELETON.md",
    ]

    outline_rel = next((p for p in inputs if p.endswith("outline.yml")), "outline/outline.yml")
    todo_rel = next((p for p in outputs if p.endswith("ARGUMENT_SELFLOOP_TODO.md")), "output/ARGUMENT_SELFLOOP_TODO.md")
    summaries_rel = next(
        (p for p in outputs if p.endswith("SECTION_ARGUMENT_SUMMARIES.jsonl")),
        "output/SECTION_ARGUMENT_SUMMARIES.jsonl",
    )
    skeleton_rel = next((p for p in outputs if p.endswith("ARGUMENT_SKELETON.md")), "output/ARGUMENT_SKELETON.md")

    outline_path = workspace / outline_rel
    todo_path = workspace / todo_rel
    summaries_path = workspace / summaries_rel
    skeleton_path = workspace / skeleton_rel

    ensure_dir(todo_path.parent)

    issues: list[QualityIssue] = []

    if not outline_path.exists() or outline_path.stat().st_size <= 0:
        issues.append(QualityIssue(code="missing_outline", message=f"Missing `{outline_rel}`"))

    missing_outputs: list[str] = []
    for rel, p in [(todo_rel, todo_path), (summaries_rel, summaries_path), (skeleton_rel, skeleton_path)]:
        if not p.exists() or p.stat().st_size <= 0:
            missing_outputs.append(rel)

    if missing_outputs:
        msg = "Missing outputs: " + ", ".join(missing_outputs)
        # Write a debuggable report-class file even when blocked.
        atomic_write_text(
            todo_path,
            "\n".join(
                [
                    "# Argument self-loop report",
                    "",
                    "- Status: FAIL",
                    f"- Reason: {msg}",
                    "",
                    "## Next action",
                    "- Produce the argument ledger artifacts (LLM-first):",
                    f"  - `{summaries_rel}` (per-section paragraph-move summaries)",
                    f"  - `{skeleton_rel}` (global argument skeleton)",
                    "- Then rerun this unit.",
                    "",
                ]
            ).rstrip()
            + "\n",
        )
        issues.append(QualityIssue(code="missing_outputs", message=msg))
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="argument-selfloop", issues=issues)
        return 2

    status = _parse_status(todo_path.read_text(encoding="utf-8", errors="ignore"))
    if status != "PASS":
        issues.append(QualityIssue(code="argument_selfloop_not_pass", message=f"`{todo_rel}` is not PASS"))

    expected_h3: list[str] = []
    if outline_path.exists() and outline_path.stat().st_size > 0:
        outline = load_yaml(outline_path)
        expected_h3 = _iter_outline_h3_ids(outline)

    recs = _load_jsonl(summaries_path)
    got_h3: set[str] = set()

    # Validate minimal schema and paragraph moves.
    bad_records = 0
    bad_paras = 0
    for rec in recs:
        kind = str(rec.get("kind") or "").strip()
        sid = str(rec.get("id") or "").strip()
        title = str(rec.get("title") or "").strip()
        if kind == "h3" and sid:
            got_h3.add(sid)

        if not sid or not title or not kind:
            bad_records += 1
            continue

        paras = rec.get("paragraphs")
        if not isinstance(paras, list) or not paras:
            bad_paras += 1
            continue

        for p in paras:
            if not isinstance(p, dict):
                bad_paras += 1
                continue
            moves = p.get("moves")
            if not isinstance(moves, list) or not moves:
                bad_paras += 1
                continue
            # Require at least one canonical move token (allow extra tags).
            if not any(str(m).strip() in ALLOWED_MOVES for m in moves):
                bad_paras += 1

    missing_h3 = [sid for sid in expected_h3 if sid not in got_h3]
    if missing_h3:
        issues.append(
            QualityIssue(
                code="argument_ledger_missing_h3",
                message=f"`{summaries_rel}` missing H3 records: {', '.join(missing_h3[:10])}",
            )
        )

    if bad_records:
        issues.append(
            QualityIssue(
                code="argument_ledger_bad_records",
                message=f"`{summaries_rel}` has malformed records (missing kind/id/title): {bad_records}",
            )
        )

    if bad_paras:
        issues.append(
            QualityIssue(
                code="argument_ledger_bad_paragraphs",
                message=f"`{summaries_rel}` has paragraphs without valid move labels: {bad_paras}",
            )
        )

    # Basic sanity: skeleton should not be empty.
    if not skeleton_path.exists() or skeleton_path.stat().st_size <= 0:
        issues.append(QualityIssue(code="missing_argument_skeleton", message=f"Missing `{skeleton_rel}`"))

    # Also run the generic output checks (placeholders/ellipsis).
    for rel in [todo_rel, summaries_rel, skeleton_rel]:
        issues.extend(check_unit_outputs(skill="argument-selfloop", workspace=workspace, outputs=[rel]))

    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="argument-selfloop", issues=issues)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

