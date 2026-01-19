from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


_CITE_TOKEN_RE = re.compile(r"[A-Za-z0-9:_-]+")


def _load_jsonl_strict(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Load JSONL and return (records, errors).

    Schema normalization must not silently proceed on corrupted artifacts.
    """

    records: list[dict[str, Any]] = []
    errors: list[str] = []

    if not path.exists() or path.stat().st_size <= 0:
        errors.append(f"missing_or_empty: {path}")
        return records, errors

    for i, raw in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception as exc:
            errors.append(f"json_error: {path}:{i}: {type(exc).__name__}: {exc}")
            continue
        if not isinstance(rec, dict):
            errors.append(f"non_object: {path}:{i}: {type(rec).__name__}")
            continue
        records.append(rec)

    return records, errors


def _normalize_bibkey(key: str) -> str:
    k = str(key or "").strip()
    if not k:
        return ""
    if k.startswith("[@") and k.endswith("]"):
        k = k[2:-1].strip()
    if k.startswith("@"):
        k = k[1:].strip()
    k = k.strip("[](){}")
    return k


def _normalize_citations_list(val: Any, *, bib_keys: set[str]) -> tuple[list[str], int, int]:
    """Return (normalized_keys, changed_count, unknown_count)."""

    if not isinstance(val, list):
        return [], 0, 0

    out: list[str] = []
    changed = 0
    unknown = 0

    for it in val:
        raw = str(it or "").strip()
        if not raw:
            continue

        # Extract candidate keys.
        cleaned = raw.replace("@", " " )
        if cleaned.startswith("[") and cleaned.endswith("]"):
            cleaned = cleaned[1:-1]
        toks = [t for t in _CITE_TOKEN_RE.findall(cleaned) if t]

        # If we have ref.bib keys, keep only those (prevents accidental word capture).
        if bib_keys:
            toks = [t for t in toks if t in bib_keys]

        # If nothing matched but this looks like a single key, keep it best-effort.
        if not toks:
            single = _normalize_bibkey(raw)
            if single and (not bib_keys or single in bib_keys):
                toks = [single]

        if not toks:
            unknown += 1
            changed += 1
            continue

        for t in toks:
            k = _normalize_bibkey(t)
            if not k:
                continue
            if bib_keys and k not in bib_keys:
                unknown += 1
            if k not in out:
                out.append(k)

        # Best-effort change tracking.
        if _normalize_bibkey(raw) != _normalize_bibkey(toks[0] if len(toks) == 1 else ";".join(toks)):
            changed += 1

    return out, changed, unknown


def _normalize_obj(obj: Any, *, bib_keys: set[str]) -> tuple[Any, dict[str, int]]:
    """Normalize citation-key formats recursively.

    - citations: list[str] -> raw BibTeX keys (no @ prefix)
    - bibkey: string -> strip leading @
    - bibkeys/mapped_bibkeys/allowed_bibkeys_*: list[str] -> strip leading @
    """

    stats = {
        "citations_lists_seen": 0,
        "citations_elements_changed": 0,
        "citations_unknown": 0,
        "bibkey_strings_normalized": 0,
        "bibkeys_lists_normalized": 0,
    }

    def walk(x: Any) -> Any:
        if isinstance(x, dict):
            out: dict[str, Any] = {}
            for k, v in x.items():
                key = str(k)

                if key == "citations":
                    stats["citations_lists_seen"] += 1
                    norm, changed, unknown = _normalize_citations_list(v, bib_keys=bib_keys)
                    stats["citations_elements_changed"] += changed
                    stats["citations_unknown"] += unknown
                    out[key] = norm
                    continue

                if key == "bibkey":
                    before = str(v or "")
                    after = _normalize_bibkey(before)
                    if after != before:
                        stats["bibkey_strings_normalized"] += 1
                    out[key] = after
                    continue

                if key in {
                    "bibkeys",
                    "mapped_bibkeys",
                    "allowed_bibkeys_selected",
                    "allowed_bibkeys_mapped",
                    "allowed_bibkeys_chapter",
                    "allowed_bibkeys_global",
                }:
                    if isinstance(v, list):
                        norm_list: list[str] = []
                        for it in v:
                            nk = _normalize_bibkey(str(it or ""))
                            if nk:
                                norm_list.append(nk)
                        if norm_list != v:
                            stats["bibkeys_lists_normalized"] += 1
                        out[key] = norm_list
                    else:
                        out[key] = walk(v)
                    continue

                out[key] = walk(v)
            return out

        if isinstance(x, list):
            return [walk(v) for v in x]

        return x

    return walk(obj), stats


def _parse_outline(outline: Any) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Return (h2_title_by_id, h3_title_by_id, h3_to_h2)."""

    h2_title_by_id: dict[str, str] = {}
    h3_title_by_id: dict[str, str] = {}
    h3_to_h2: dict[str, str] = {}

    if not isinstance(outline, list):
        return h2_title_by_id, h3_title_by_id, h3_to_h2

    for sec in outline:
        if not isinstance(sec, dict):
            continue
        sec_id = str(sec.get("id") or "").strip()
        sec_title = str(sec.get("title") or "").strip()
        if sec_id and sec_title:
            h2_title_by_id[sec_id] = sec_title

        subs = sec.get("subsections") or []
        if not isinstance(subs, list):
            continue
        for sub in subs:
            if not isinstance(sub, dict):
                continue
            sub_id = str(sub.get("id") or "").strip()
            sub_title = str(sub.get("title") or "").strip()
            if sub_id and sub_title:
                h3_title_by_id[sub_id] = sub_title
            if sub_id and sec_id:
                h3_to_h2[sub_id] = sec_id

    return h2_title_by_id, h3_title_by_id, h3_to_h2


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

    from tooling.common import backup_existing, ensure_dir, load_yaml, now_iso_seconds, parse_semicolon_list, write_jsonl

    workspace = Path(args.workspace).resolve()

    inputs = parse_semicolon_list(args.inputs)
    outputs = parse_semicolon_list(args.outputs) or ["output/SCHEMA_NORMALIZATION_REPORT.md"]

    def first(suffixes: tuple[str, ...], default: str) -> str:
        for raw in inputs:
            rel = str(raw or "").strip()
            if not rel:
                continue
            for suf in suffixes:
                if rel.endswith(suf):
                    return rel
        return default

    outline_rel = first(("outline/outline.yml", "outline.yml"), "outline/outline.yml")
    bib_rel = first(("citations/ref.bib", "ref.bib"), "citations/ref.bib")

    default_jsonl = [
        "outline/subsection_briefs.jsonl",
        "outline/chapter_briefs.jsonl",
        "outline/evidence_bindings.jsonl",
        "outline/evidence_drafts.jsonl",
        "outline/anchor_sheet.jsonl",
    ]

    jsonl_rels = [rel for rel in inputs if str(rel).strip().endswith(".jsonl")]
    if not jsonl_rels:
        jsonl_rels = default_jsonl

    out_rel = outputs[0] if outputs else "output/SCHEMA_NORMALIZATION_REPORT.md"
    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    outline_path = workspace / outline_rel
    stamp = now_iso_seconds()
    if not outline_path.exists() or outline_path.stat().st_size <= 0:
        out_path.write_text(
            "\n".join(
                [
                    "# Schema normalization report",                    "",                    f"- Generated at: `{stamp}`",                    "- Status: FAIL",                    "",                    f"Missing required outline: `{outline_rel}`",                    "",                ]
            ),
            encoding="utf-8",
        )
        return 2

    outline = load_yaml(outline_path)
    h2_title_by_id, h3_title_by_id, h3_to_h2 = _parse_outline(outline)

    bib_keys: set[str] = set()
    bib_path = workspace / bib_rel
    if bib_path.exists() and bib_path.stat().st_size > 0:
        bib_text = bib_path.read_text(encoding="utf-8", errors="ignore")
        bib_keys = set(re.findall(r"(?im)^@\w+\s*\{\s*([^,\s]+)\s*,", bib_text))

    status = "PASS"
    report_lines: list[str] = [
        "# Schema normalization report",        "",        f"- Generated at: `{stamp}`",        f"- Outline: `{outline_rel}`",    ]
    if bib_keys:
        report_lines.append(f"- BibTeX: `{bib_rel}` ({len(bib_keys)} keys loaded)")
    else:
        report_lines.append(f"- BibTeX: `{bib_rel}` (missing/empty; skip key validation)")
    report_lines.append("")

    total_changed = 0
    total_errors = 0

    for rel in jsonl_rels:
        rel = str(rel or "").strip()
        if not rel:
            continue
        path = workspace / rel

        records, errors = _load_jsonl_strict(path)
        if errors:
            status = "FAIL"
            total_errors += len(errors)
            report_lines.append(f"## {rel}")
            report_lines.append("")
            report_lines.append(f"- Status: FAIL ({len(errors)} errors)")
            for e in errors[:12]:
                report_lines.append(f"- {e}")
            if len(errors) > 12:
                report_lines.append(f"- ... ({len(errors) - 12} more)")
            report_lines.append("")
            continue

        changed_records = 0
        fields_filled = 0
        citations_lists_seen = 0
        citations_elements_changed = 0
        citations_unknown = 0
        bibkey_strings_normalized = 0
        bibkeys_lists_normalized = 0

        normalized: list[dict[str, Any]] = []

        for rec in records:
            before = json.dumps(rec, sort_keys=True, ensure_ascii=True)

            sub_id = str(rec.get("sub_id") or "").strip()
            sec_id = str(rec.get("section_id") or "").strip()

            if sub_id:
                if not sec_id:
                    sec_id = h3_to_h2.get(sub_id) or str(sub_id.split(".")[0]).strip()
                    if sec_id:
                        rec["section_id"] = sec_id
                        fields_filled += 1

                if not str(rec.get("title") or "").strip():
                    t = h3_title_by_id.get(sub_id) or ""
                    if t:
                        rec["title"] = t
                        fields_filled += 1

                if not str(rec.get("section_title") or "").strip() and sec_id:
                    st = h2_title_by_id.get(sec_id) or ""
                    if st:
                        rec["section_title"] = st
                        fields_filled += 1

            if sec_id and not str(rec.get("section_title") or "").strip():
                st = h2_title_by_id.get(sec_id) or ""
                if st:
                    rec["section_title"] = st
                    fields_filled += 1

            rec_norm, stats = _normalize_obj(rec, bib_keys=bib_keys)
            rec = rec_norm

            citations_lists_seen += stats["citations_lists_seen"]
            citations_elements_changed += stats["citations_elements_changed"]
            citations_unknown += stats["citations_unknown"]
            bibkey_strings_normalized += stats["bibkey_strings_normalized"]
            bibkeys_lists_normalized += stats["bibkeys_lists_normalized"]

            after = json.dumps(rec, sort_keys=True, ensure_ascii=True)
            if after != before:
                changed_records += 1

            normalized.append(rec)

        if changed_records:
            total_changed += changed_records
            backup_existing(path)
            write_jsonl(path, normalized)

        report_lines.append(f"## {rel}")
        report_lines.append("")
        report_lines.append("- Status: PASS")
        report_lines.append(f"- Records: {len(records)}")
        report_lines.append(f"- Records changed: {changed_records}")
        report_lines.append(f"- Fields filled (ids/titles): {fields_filled}")
        report_lines.append(f"- Citations lists seen: {citations_lists_seen}")
        report_lines.append(f"- Citation elements changed: {citations_elements_changed}")
        if bib_keys:
            report_lines.append(f"- Citation keys not in ref.bib (count, best-effort): {citations_unknown}")
        report_lines.append(f"- bibkey strings normalized: {bibkey_strings_normalized}")
        report_lines.append(f"- bibkeys lists normalized: {bibkeys_lists_normalized}")
        report_lines.append("")

    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- Status: {status}")
    report_lines.append(f"- Files processed: {len([r for r in jsonl_rels if str(r or '').strip()])}")
    report_lines.append(f"- Total records changed: {total_changed}")
    report_lines.append(f"- Total parse errors: {total_errors}")

    out_path.write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
