from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def _sha1(text: str) -> str:
    return hashlib.sha1((text or "").encode("utf-8", errors="ignore")).hexdigest()


def _extract_cites(text: str) -> list[str]:
    keys: set[str] = set()
    for m in re.finditer(r"\[@([^\]]+)\]", text or ""):
        inside = (m.group(1) or "").strip()
        for k in re.findall(r"[A-Za-z0-9:_-]+", inside):
            if k:
                keys.add(k)
    return sorted(keys)


def _h3_citation_sets(md: str) -> dict[str, set[str]]:
    cur_title = ""
    cur_lines: list[str] = []
    out: dict[str, set[str]] = {}

    def _flush() -> None:
        nonlocal cur_title, cur_lines
        if not cur_title:
            return
        body = "\n".join(cur_lines).strip()
        out[cur_title] = set(_extract_cites(body))

    for raw in (md or "").splitlines():
        if raw.startswith("### "):
            _flush()
            cur_title = raw[4:].strip()
            cur_lines = []
            continue
        if raw.startswith("## "):
            # End any H3 block on new H2.
            _flush()
            cur_title = ""
            cur_lines = []
            continue
        if cur_title:
            cur_lines.append(raw)

    _flush()
    return out


def _merge_is_pass(workspace: Path) -> bool:
    report_path = workspace / "output" / "MERGE_REPORT.md"
    if not report_path.exists() or report_path.stat().st_size <= 0:
        return False
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    return "- Status: PASS" in text


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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or "U110").strip() or "U110"

    outputs = parse_semicolon_list(args.outputs) or ["output/DRAFT.md"]
    out_rel = outputs[0] if outputs else "output/DRAFT.md"

    draft_path = workspace / out_rel

    # Citation anchoring baseline: capture *only* after merge is complete.
    # This prevents freezing an incomplete draft (e.g., `TODO: MISSING ...`) as the baseline.
    baseline_rel = "output/citation_anchors.prepolish.jsonl"
    baseline_path = workspace / baseline_rel
    if draft_path.exists() and draft_path.stat().st_size > 0 and not baseline_path.exists():
        draft = draft_path.read_text(encoding="utf-8", errors="ignore")
        if _merge_is_pass(workspace) and not re.search(r"(?m)^TODO:\s+MISSING\s+`", draft):
            ensure_dir(baseline_path.parent)
            sets = _h3_citation_sets(draft)
            records = []
            for title, keys in sorted(sets.items(), key=lambda kv: kv[0].lower()):
                records.append(
                    {
                        "kind": "h3",
                        "title": title,
                        "cite_keys": sorted(keys),
                    }
                )
            header = {
                "kind": "meta",
                "draft_rel": out_rel,
                "draft_sha1": _sha1(draft),
                "h3_count": len(sets),
            }
            lines = [json.dumps(header, ensure_ascii=False)] + [json.dumps(r, ensure_ascii=False) for r in records]
            atomic_write_text(baseline_path, "\n".join(lines).rstrip() + "\n")

    issues = check_unit_outputs(skill="draft-polisher", workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="draft-polisher", issues=issues)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
