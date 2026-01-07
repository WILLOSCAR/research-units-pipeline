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

    from tooling.common import ensure_dir, parse_semicolon_list, read_jsonl

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["outline/tables.md", "outline/timeline.md", "outline/figures.md"]
    out_tables = workspace / outputs[0]
    out_timeline = workspace / outputs[1] if len(outputs) >= 2 else workspace / "outline" / "timeline.md"
    out_figures = workspace / outputs[2] if len(outputs) >= 3 else workspace / "outline" / "figures.md"

    ensure_dir(out_tables.parent)
    ensure_dir(out_timeline.parent)
    ensure_dir(out_figures.parent)

    notes_path = workspace / "papers" / "paper_notes.jsonl"
    notes = read_jsonl(notes_path) if notes_path.exists() else []

    _maybe_write(out_tables, _tables_scaffold(notes=notes))
    _maybe_write(out_timeline, _timeline_scaffold(notes=notes))
    _maybe_write(out_figures, _figures_scaffold(notes=notes))
    return 0


def _maybe_write(path: Path, content: str) -> None:
    if path.exists() and path.stat().st_size > 0:
        existing = path.read_text(encoding="utf-8", errors="ignore")
        if not _is_placeholder(existing):
            return
    from tooling.common import atomic_write_text
    atomic_write_text(path, content)


def _tables_scaffold(*, notes: list[Any]) -> str:
    candidates = _pick_notes(notes, k=10, prefer_high=True)
    lines: list[str] = [
        "# Tables",
        "",
        "<!-- SCAFFOLD: survey-visuals (replace with real content + real citation keys) -->",
        "",
        "## Table 1: Method comparison (agents)",
        "",
        "| Work | Core loop / planner | Tools | Memory | Environment | Evaluation | Key takeaway |",
        "|---|---|---|---|---|---|---|",
    ]
    if candidates:
        for note in candidates[:8]:
            pid = str(note.get("paper_id") or "").strip()
            title = _short_title(str(note.get("title") or "").strip())
            bibkey = str(note.get("bibkey") or "").strip()
            cite = f" [@{bibkey}]" if bibkey else ""
            label = f"{pid} {title}".strip() if pid else title
            lines.append(f"| {label}{cite} | TODO | TODO | TODO | TODO | TODO | TODO |")
    else:
        lines.append("| TODO [@Key1] | TODO | TODO | TODO | TODO | TODO | TODO |")

    lines.extend(
        [
            "",
            "## Table 2: Benchmarks / evaluation suites",
            "",
            "| Benchmark | Tasks | Interface | Metrics | Notes |",
            "|---|---|---|---|---|",
        ]
    )
    benches = _pick_benchmark_notes(notes, k=8)
    if benches:
        for note in benches[:6]:
            pid = str(note.get("paper_id") or "").strip()
            title = _short_title(str(note.get("title") or "").strip())
            bibkey = str(note.get("bibkey") or "").strip()
            cite = f" [@{bibkey}]" if bibkey else ""
            label = f"{pid} {title}".strip() if pid else title
            lines.append(f"| {label}{cite} | TODO | TODO | TODO | TODO |")
    else:
        lines.append("| TODO [@Key2] | TODO | TODO | TODO | TODO |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _timeline_scaffold(*, notes: list[Any]) -> str:
    candidates = _pick_notes(notes, k=30, prefer_high=True)
    lines: list[str] = [
        "# Timeline / Evolution",
        "",
        "<!-- SCAFFOLD: survey-visuals timeline (year -> key milestones; cite keys from ref.bib) -->",
        "",
    ]
    bullets = _timeline_bullets(candidates, target=8)
    if bullets:
        lines.extend(bullets)
    else:
        lines.extend(
            [
                "- 2022: TODO [@Key1]",
                "- 2023: TODO [@Key2]",
                "- 2024: TODO [@Key3]",
                "- 2025: TODO [@Key4]",
            ]
        )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _figures_scaffold(*, notes: list[Any]) -> str:
    candidates = _pick_notes(notes, k=10, prefer_high=True)
    cite_keys: list[str] = []
    for note in candidates[:6]:
        bibkey = str(note.get("bibkey") or "").strip()
        if bibkey and bibkey not in cite_keys:
            cite_keys.append(bibkey)
    cite = f"[@{'; @'.join(cite_keys[:4])}]" if cite_keys else "[@Key1; @Key2]"

    lines: list[str] = [
        "# Figure specs (no prose)",
        "",
        "<!-- SCAFFOLD: survey-visuals figures (specs only; no narrative paragraphs) -->",
        "",
        "- Figure 1 (system view): TODO",
        "  - Purpose: TODO",
        "  - Elements: planner / tool interface / memory / verifier / environment (adapt to outline)",
        f"  - Supported by: TODO {cite}",
        "",
        "- Figure 2 (taxonomy view): TODO",
        "  - Purpose: TODO",
        "  - Elements: 2–3 levels of taxonomy with representative works per node",
        f"  - Supported by: TODO {cite}",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _is_placeholder(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return True
    if "<!-- SCAFFOLD" in text:
        return True
    if "TODO" in text:
        return True
    if re.search(r"\[@(?:Key|KEY)\d+", text):
        return True
    return False


def _pick_notes(notes: list[Any], *, k: int, prefer_high: bool) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = [n for n in notes if isinstance(n, dict)]
    if prefer_high:
        high = [n for n in items if str(n.get("priority") or "").strip().lower() == "high"]
        if high:
            items = high
    items.sort(key=lambda n: (-_year_int(n.get("year")), str(n.get("paper_id") or ""), str(n.get("title") or "")))
    return items[: max(0, int(k))]


def _pick_benchmark_notes(notes: list[Any], *, k: int) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = [n for n in notes if isinstance(n, dict)]
    signals = ("benchmark", "evaluation", "eval", "suite", "arena", "agentbench", "bench")
    picked = [n for n in items if any(s in str(n.get("title") or "").lower() for s in signals)]
    picked.sort(key=lambda n: (-_year_int(n.get("year")), str(n.get("paper_id") or ""), str(n.get("title") or "")))
    if picked:
        return picked[: max(0, int(k))]
    return _pick_notes(notes, k=k, prefer_high=True)


def _timeline_bullets(notes: list[dict[str, Any]], *, target: int) -> list[str]:
    by_year: dict[int, list[dict[str, Any]]] = {}
    for note in notes:
        y = _year_int(note.get("year"))
        if y <= 0:
            continue
        by_year.setdefault(y, []).append(note)
    bullets: list[str] = []
    for y in sorted(by_year.keys()):
        by_year[y].sort(key=lambda n: (str(n.get("paper_id") or ""), str(n.get("title") or "")))
        for note in by_year[y]:
            pid = str(note.get("paper_id") or "").strip()
            title = _short_title(str(note.get("title") or "").strip(), max_len=72)
            bibkey = str(note.get("bibkey") or "").strip()
            cite = f" [@{bibkey}]" if bibkey else ""
            label = f"{pid} {title}".strip() if pid else title
            bullets.append(f"- {y}: {label} — TODO: milestone summary{cite}")
            if len(bullets) >= int(target):
                return bullets
    return bullets


def _short_title(title: str, *, max_len: int = 64) -> str:
    title = (title or "").strip()
    if len(title) <= max_len:
        return title
    return title[: max_len - 1].rstrip() + "…"


def _year_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
