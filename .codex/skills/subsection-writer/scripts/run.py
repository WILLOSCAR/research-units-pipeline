from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


def _sha1_text(text: str) -> str:
    return hashlib.sha1((text or "").encode("utf-8", errors="ignore")).hexdigest()


def _slug_unit_id(unit_id: str) -> str:
    raw = str(unit_id or "").strip()
    out: list[str] = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        else:
            out.append("_")
    safe = "".join(out).strip("_")
    return f"S{safe}" if safe else "S"


def _extract_citation_keys(text: str) -> list[str]:
    cited: set[str] = set()
    for m in re.finditer(r"\[@([^\]]+)\]", text or ""):
        inside = (m.group(1) or "").strip()
        for k in re.findall(r"[A-Za-z0-9:_-]+", inside):
            if k:
                cited.add(k)
    return sorted(cited)


def _iter_outline_units(outline: Any) -> list[dict[str, str]]:
    units: list[dict[str, str]] = []
    if not isinstance(outline, list):
        return units

    for sec in outline:
        if not isinstance(sec, dict):
            continue
        sec_id = str(sec.get("id") or "").strip()
        sec_title = str(sec.get("title") or "").strip()
        subs = sec.get("subsections") or []
        if subs and isinstance(subs, list):
            for sub in subs:
                if not isinstance(sub, dict):
                    continue
                sub_id = str(sub.get("id") or "").strip()
                sub_title = str(sub.get("title") or "").strip()
                if sub_id and sub_title:
                    units.append(
                        {
                            "kind": "h3",
                            "id": sub_id,
                            "title": sub_title,
                            "section_id": sec_id,
                            "section_title": sec_title,
                        }
                    )
        else:
            if sec_id and sec_title:
                units.append(
                    {
                        "kind": "h2",
                        "id": sec_id,
                        "title": sec_title,
                        "section_id": sec_id,
                        "section_title": sec_title,
                    }
                )
    return units


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
        atomic_write_text,
        decisions_has_approval,
        ensure_dir,
        load_yaml,
        now_iso_seconds,
        parse_semicolon_list,
        upsert_checkpoint_block,
    )
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or "U100").strip() or "U100"

    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs) or ["sections/sections_manifest.jsonl"]

    out_rel = outputs[0] if outputs else "sections/sections_manifest.jsonl"
    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    # Approval gate (survey policy): prose after C2.
    decisions_rel = "DECISIONS.md"
    for rel in inputs:
        if str(rel or "").strip().endswith("DECISIONS.md"):
            decisions_rel = str(rel).strip()
            break
    decisions_path = workspace / decisions_rel
    if not decisions_has_approval(decisions_path, "C2"):
        block = "\n".join(
            [
                "## C5 section writing request",
                "",
                "- This unit writes prose into per-section files under `sections/`.",
                "- Please tick `Approve C2` (scope + outline) in the approvals checklist above.",
                "- Then rerun this unit.",
                "",
            ]
        )
        upsert_checkpoint_block(decisions_path, "C5", block)
        return 2

    outline_rel = "outline/outline.yml"
    for rel in inputs:
        rel = str(rel or "").strip()
        if rel.endswith("outline/outline.yml") or rel.endswith("outline.yml"):
            outline_rel = rel
            break

    outline = load_yaml(workspace / outline_rel) if (workspace / outline_rel).exists() else []
    units = _iter_outline_units(outline)

    # Build expected files under `sections/`.
    sections_dir = out_path.parent
    global_files = [
        {"kind": "global", "id": "abstract", "title": "Abstract", "path": str((sections_dir / "abstract.md").relative_to(workspace))},
        {"kind": "global", "id": "evidence_note", "title": "Evidence note", "path": str((sections_dir / "evidence_note.md").relative_to(workspace))},
        {
            "kind": "global",
            "id": "open_problems",
            "title": "Open Problems & Future Directions",
            "path": str((sections_dir / "open_problems.md").relative_to(workspace)),
        },
        {"kind": "global", "id": "conclusion", "title": "Conclusion", "path": str((sections_dir / "conclusion.md").relative_to(workspace))},
    ]

    records: list[dict[str, Any]] = []
    generated_at = now_iso_seconds()

    def _add_record(rec: dict[str, Any]) -> None:
        p = workspace / str(rec.get("path") or "")
        exists = p.exists() and p.is_file() and p.stat().st_size > 0
        rec["exists"] = bool(exists)
        if exists:
            text = p.read_text(encoding="utf-8", errors="ignore")
            rec["sha1"] = _sha1_text(text)
            rec["bytes"] = int(p.stat().st_size)
            rec["citations"] = _extract_citation_keys(text)
        records.append(rec)

    for gf in global_files:
        _add_record({**gf, "generated_at": generated_at})

    for u in units:
        uid = str(u.get("id") or "").strip()
        rel = (sections_dir / f"{_slug_unit_id(uid)}.md").relative_to(workspace)
        rec = {
            "kind": u.get("kind"),
            "id": uid,
            "title": u.get("title"),
            "section_id": u.get("section_id"),
            "section_title": u.get("section_title"),
            "path": str(rel),
            "generated_at": generated_at,
        }
        _add_record(rec)

    # Write manifest (JSONL).
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    atomic_write_text(out_path, "\n".join(lines).rstrip() + "\n")

    issues = []

    # Hard prereq sanity (so the quality report points upstream if needed).
    for prereq_skill, prereq_outs in [
        ("outline-builder", [outline_rel]),
        ("subsection-briefs", ["outline/subsection_briefs.jsonl"]),
        ("evidence-draft", ["outline/evidence_drafts.jsonl"]),
        ("citation-verifier", ["citations/ref.bib"]),
        ("evidence-binder", ["outline/evidence_bindings.jsonl"]),
    ]:
        issues.extend(check_unit_outputs(skill=prereq_skill, workspace=workspace, outputs=prereq_outs))

    # Main checks for this skill.
    issues.extend(check_unit_outputs(skill="subsection-writer", workspace=workspace, outputs=[out_rel]))

    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="subsection-writer", issues=issues)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
