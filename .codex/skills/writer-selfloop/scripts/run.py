from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def _extract_paths(msg: str) -> list[str]:
    # Prefer backticked paths, then fall back to a loose pattern.
    paths: list[str] = []
    for m in re.finditer(r"`(sections/[^`]+?\\.md)`", msg or ""):
        paths.append(m.group(1))
    if paths:
        return paths
    for m in re.finditer(r"\\b(sections/[A-Za-z0-9_.-]+\\.md)\\b", msg or ""):
        paths.append(m.group(1))
    return paths


def _trim(text: str, *, max_len: int) -> str:
    s = str(text or "").strip()
    if len(s) <= int(max_len):
        return s
    # Trim without ellipsis to avoid placeholder-like markers in report-class outputs.
    return s[: int(max_len)].rstrip()


def _slug_unit_id(unit_id: str) -> str:
    raw = str(unit_id or "").strip()
    out: list[str] = []
    for ch in raw:
        out.append(ch if ch.isalnum() else "_")
    safe = "".join(out).strip("_")
    return f"S{safe}" if safe else "S"


def _expected_paths_from_outline(outline: Any) -> set[str]:
    expected = {"sections/abstract.md", "sections/discussion.md", "sections/conclusion.md"}
    if not isinstance(outline, list):
        return expected

    for sec in outline:
        if not isinstance(sec, dict):
            continue
        sec_id = str(sec.get("id") or "").strip()
        subs = sec.get("subsections") or []
        if isinstance(subs, list) and subs:
            if sec_id:
                expected.add(f"sections/{_slug_unit_id(sec_id)}_lead.md")
            for sub in subs:
                if not isinstance(sub, dict):
                    continue
                sub_id = str(sub.get("id") or "").strip()
                if sub_id:
                    expected.add(f"sections/{_slug_unit_id(sub_id)}.md")
        else:
            if sec_id:
                expected.add(f"sections/{_slug_unit_id(sec_id)}.md")

    return expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import ensure_dir, load_yaml, parse_semicolon_list
    from tooling.quality_gate import QualityIssue, _check_sections_manifest, write_quality_report

    unit_id = str(args.unit_id or "U1005").strip() or "U1005"

    inputs = parse_semicolon_list(args.inputs) or [
        "sections/sections_manifest.jsonl",
        "outline/subsection_briefs.jsonl",
        "outline/chapter_briefs.jsonl",
        "outline/writer_context_packs.jsonl",
    ]
    outputs = parse_semicolon_list(args.outputs) or ["output/WRITER_SELFLOOP_TODO.md"]

    manifest_rel = next(
        (rel for rel in inputs if str(rel or "").strip().endswith("sections_manifest.jsonl")),
        "sections/sections_manifest.jsonl",
    )
    out_rel = outputs[0] if outputs else "output/WRITER_SELFLOOP_TODO.md"

    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    # Canonical writing gate: reuse the strict sections check.
    section_issues = _check_sections_manifest(workspace, [manifest_rel])
    issue_pairs: list[tuple[str, str]] = [(it.code, it.message) for it in section_issues]
    issue_codes = {code for code, _ in issue_pairs}

    now = datetime.now().replace(microsecond=0).isoformat()
    status = "PASS" if not section_issues else "FAIL"

    lines: list[str] = [
        "# Writer self-loop",
        "",
        f"- Timestamp: `{now}`",
        f"- Status: {status}",
        "",
    ]

    if not section_issues:
        lines.extend(
            [
                "## Summary",
                "",
                "- No section-level quality issues detected.",
                "- Proceed to `section-logic-polisher` -> `transition-weaver` -> `section-merger`.",
                "",
            ]
        )
        out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return 0

    # Load optional context packs (best-effort; missing files are OK).
    manifest = _read_jsonl(workspace / manifest_rel)
    manifest_by_path: dict[str, dict[str, Any]] = {}
    for rec in manifest:
        rel = str(rec.get("path") or "").strip()
        if rel:
            manifest_by_path[rel] = rec

    briefs_by_sub: dict[str, dict[str, Any]] = {}
    for rec in _read_jsonl(workspace / "outline" / "subsection_briefs.jsonl"):
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            briefs_by_sub[sid] = rec

    briefs_by_sec: dict[str, dict[str, Any]] = {}
    for rec in _read_jsonl(workspace / "outline" / "chapter_briefs.jsonl"):
        sid = str(rec.get("section_id") or "").strip()
        if sid:
            briefs_by_sec[sid] = rec

    context_by_sub: dict[str, dict[str, Any]] = {}
    for rec in _read_jsonl(workspace / "outline" / "writer_context_packs.jsonl"):
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            context_by_sub[sid] = rec

    # Group issues by file when possible.
    by_file: dict[str, list[tuple[str, str]]] = {}
    orphan: list[tuple[str, str]] = []

    outline_path = workspace / "outline" / "outline.yml"
    outline = load_yaml(outline_path) if outline_path.exists() else []
    expected = sorted(_expected_paths_from_outline(outline))

    # When the gate is `sections_missing_files`, the issue message is truncated.
    # Compute missing files from the outline + filesystem (do not rely on stale manifest `exists` flags).
    if "sections_missing_files" in issue_codes:
        for rel in expected:
            p = workspace / rel
            if not p.exists() or p.stat().st_size <= 0:
                by_file.setdefault(rel, []).append(("sections_missing_files", "Missing or empty per-section file."))

    for code, msg in issue_pairs:
        paths = _extract_paths(msg)
        if not paths:
            orphan.append((code, msg))
            continue
        for p in paths:
            by_file.setdefault(p, []).append((code, msg))

    # Deduplicate per-file issues.
    by_file_dedup: dict[str, list[tuple[str, str]]] = {}
    for rel, items in by_file.items():
        seen: set[tuple[str, str]] = set()
        out_items: list[tuple[str, str]] = []
        for code, msg in items:
            key = (str(code), str(msg))
            if key in seen:
                continue
            seen.add(key)
            out_items.append((code, msg))
        by_file_dedup[rel] = out_items
    by_file = by_file_dedup

    lines.extend(["## Failing files", ""])

    if not by_file:
        lines.append("- (No per-file paths detected; see Orphan issues below.)")

    for rel in sorted(by_file.keys()):
        lines.append(f"- `{rel}`")

        rec = manifest_by_path.get(rel) or {}
        kind = str(rec.get("kind") or "").strip()
        sid = str(rec.get("id") or "").strip()
        title = str(rec.get("title") or "").strip()

        if kind or sid or title:
            lines.append(
                f"  - kind: `{kind or 'unknown'}` id: `{sid or 'unknown'}` title: {title or '(unknown)'}"
            )

        if kind == "h3" and sid:
            brief = briefs_by_sub.get(sid) or {}
            rq = str(brief.get("rq") or "").strip()
            axes = brief.get("axes") or []
            if rq:
                lines.append(f"  - rq: {rq}")
            if isinstance(axes, list) and axes:
                axes_txt = ", ".join(str(a) for a in axes[:6] if str(a).strip())
                if axes_txt:
                    lines.append(f"  - axes: {axes_txt}")

            ctx = context_by_sub.get(sid) or {}
            if isinstance(ctx, dict) and ctx:
                plan = ctx.get("paragraph_plan") or []
                if isinstance(plan, list) and plan:
                    lines.append(f"  - paragraph_plan: {len(plan)} (intent sketch)")
                    for p in plan[:8]:
                        if not isinstance(p, dict):
                            continue
                        num = p.get("para")
                        intent = _trim(p.get("intent") or "", max_len=160)
                        if not intent:
                            continue
                        prefix = f"p{num}" if str(num).strip() else "p?"
                        lines.append(f"    - {prefix}: {intent}")

                must_use = ctx.get("must_use") or {}
                if isinstance(must_use, dict) and must_use:
                    ma = must_use.get("min_anchor_facts")
                    mc = must_use.get("min_comparison_cards")
                    ml = must_use.get("min_limitation_hooks")
                    lines.append(f"  - must_use: anchors>={ma} comparisons>={mc} limitations>={ml}")

                pack_stats = ctx.get("pack_stats") or {}
                if isinstance(pack_stats, dict) and pack_stats:
                    a_kept = (pack_stats.get("anchors") or {}).get("kept")
                    c_kept = (pack_stats.get("comparisons") or {}).get("kept")
                    e_kept = (pack_stats.get("evaluation_protocol") or {}).get("kept")
                    l_kept = (pack_stats.get("limitation_hooks") or {}).get("kept")
                    lines.append(
                        f"  - pack_stats: anchors_kept={a_kept} comparisons_kept={c_kept} eval_kept={e_kept} limitation_kept={l_kept}"
                    )

                pack_warnings = ctx.get("pack_warnings") or []
                if isinstance(pack_warnings, list) and pack_warnings:
                    lines.append("  - pack_warnings:")
                    for w in pack_warnings[:4]:
                        w = str(w or "").strip()
                        if w:
                            lines.append(f"    - {w}")

        if kind == "h2_lead" and sid:
            brief = briefs_by_sec.get(sid) or {}
            through = brief.get("throughline") or []
            key_contrasts = brief.get("key_contrasts") or []
            if isinstance(through, list) and through:
                through_txt = ", ".join(str(x) for x in through[:6] if str(x).strip())
                if through_txt:
                    lines.append(f"  - throughline: {through_txt}")
            if isinstance(key_contrasts, list) and key_contrasts:
                kc_txt = ", ".join(str(x) for x in key_contrasts[:6] if str(x).strip())
                if kc_txt:
                    lines.append(f"  - key_contrasts: {kc_txt}")

        allowed_sel = rec.get("allowed_bibkeys_selected") or []
        allowed_map = rec.get("allowed_bibkeys_mapped") or []
        allowed_chapter = rec.get("allowed_bibkeys_chapter") or []
        allowed_global = rec.get("allowed_bibkeys_global") or []
        evidence_ids = rec.get("evidence_ids") or []
        anchors = rec.get("anchor_facts") or []

        if isinstance(allowed_sel, list) and any(str(k).strip() for k in allowed_sel):
            sel = [str(k).strip() for k in allowed_sel if str(k).strip()]
            sample = ", ".join(sel[:12])
            suffix = "..." if len(sel) > 12 else ""
            lines.append(f"  - allowed_bibkeys_selected: {sample}{suffix}")
        if isinstance(allowed_map, list) and any(str(k).strip() for k in allowed_map):
            lines.append(f"  - allowed_bibkeys_mapped: {len([k for k in allowed_map if str(k).strip()])}")
        if isinstance(allowed_chapter, list) and any(str(k).strip() for k in allowed_chapter):
            lines.append(f"  - allowed_bibkeys_chapter: {len([k for k in allowed_chapter if str(k).strip()])}")
        if isinstance(allowed_global, list) and any(str(k).strip() for k in allowed_global):
            lines.append(f"  - allowed_bibkeys_global: {len([k for k in allowed_global if str(k).strip()])}")
        if isinstance(evidence_ids, list) and any(str(e).strip() for e in evidence_ids):
            lines.append(f"  - evidence_ids: {len([e for e in evidence_ids if str(e).strip()])}")
        if isinstance(anchors, list) and any(isinstance(a, dict) and str(a.get('text') or '').strip() for a in anchors):
            examples = [a for a in anchors if isinstance(a, dict)]
            lines.append(f"  - anchor_facts: {len(examples)} (examples)")
            for a in examples[:2]:
                hook = str(a.get("hook_type") or "").strip()
                txt = _trim(a.get("text") or "", max_len=220)
                cites = a.get("citations") or []
                cite_str = ", ".join(str(c).lstrip("@").strip() for c in cites if str(c).strip())
                if cite_str:
                    lines.append(f"    - {hook}: {txt} (cites: {cite_str})")
                else:
                    lines.append(f"    - {hook}: {txt}")

        for code, msg in by_file.get(rel, []):
            lines.append(f"  - `{code}`: {msg}")

    if orphan:
        lines.extend(["", "## Orphan issues (no sections/*.md path detected)", ""])
        for code, msg in orphan:
            lines.append(f"- `{code}`: {msg}")

    lines.extend(
        [
            "",
            "## Loop",
            "",
            "1) Fix only the failing `sections/*.md` files above (follow `.codex/skills/writer-selfloop/SKILL.md`).",
            "2) Recheck:",
            "",
            "```bash",
            f"python .codex/skills/writer-selfloop/scripts/run.py --workspace {workspace.as_posix()}",
            "```",
            "",
            "Optional: after large edits, rerun `subsection-writer` to refresh `sections/sections_manifest.jsonl` for auditability.",
            "",
        ]
    )

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    # Persist failure details in the standard quality-gate sink (append-only) so
    # the workspace is debuggable without reruns.
    write_quality_report(
        workspace=workspace,
        unit_id=unit_id,
        skill="writer-selfloop",
        issues=[QualityIssue(code=c, message=m) for c, m in issue_pairs],
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
