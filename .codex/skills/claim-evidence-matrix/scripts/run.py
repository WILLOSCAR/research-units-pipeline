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

    from tooling.common import atomic_write_text, load_yaml, parse_semicolon_list, read_jsonl, read_tsv, tokenize

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["outline/outline.yml", "papers/paper_notes.jsonl"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/claim_evidence_matrix.md"]

    outline_path = workspace / inputs[0]
    notes_path = workspace / inputs[1]
    mapping_path = workspace / "outline" / "mapping.tsv"
    out_path = workspace / outputs[0]

    # Bootstrap-only behavior: if a human/LLM already refined the matrix, do not overwrite.
    if _looks_refined_matrix(out_path):
        return 0

    outline = load_yaml(outline_path) or []
    notes = read_jsonl(notes_path)
    mappings = read_tsv(mapping_path) if mapping_path.exists() else []

    papers_by_id = {str(n.get("paper_id") or ""): n for n in notes if isinstance(n, dict)}
    paper_ids_fallback = [pid for pid in papers_by_id.keys() if pid]

    mapped_by_section: dict[str, list[str]] = {}
    for row in mappings:
        sid = str(row.get("section_id") or "").strip()
        pid = str(row.get("paper_id") or "").strip()
        if not sid or not pid:
            continue
        mapped_by_section.setdefault(sid, []).append(pid)

    parts: list[str] = [
        "# Claim–Evidence matrix",
        "",
        "This artifact is bullets-only and is meant to make evidence explicit before writing.",
        "",
    ]

    for subsection in _iter_subsections(outline):
        sid = subsection["id"]
        title = subsection["title"]
        axes = [str(b).strip() for b in (subsection.get("bullets") or []) if str(b).strip()]

        pids = mapped_by_section.get(sid, [])
        uniq: list[str] = []
        for pid in pids:
            if pid in papers_by_id and pid not in uniq:
                uniq.append(pid)
        if len(uniq) < 2 and paper_ids_fallback:
            for cand in paper_ids_fallback:
                if cand not in uniq:
                    uniq.append(cand)
                if len(uniq) >= 2:
                    break

        themes = _top_terms(
            [
                str(papers_by_id.get(pid, {}).get("title") or "")
                + " "
                + str(papers_by_id.get(pid, {}).get("abstract") or "")
                for pid in uniq
            ],
            tokenize=tokenize,
        )

        parts.append(f"## {sid} {title}")
        parts.append("")

        claim = _make_claim(title=title, axes=axes, themes=themes)
        parts.append(f"- Claim: {claim}")
        if axes:
            parts.append(f"  - Axes: {'; '.join(axes[:6])}")
        if themes:
            parts.append(f"  - Themes: {', '.join(themes[:6])}")

        for pid in uniq[:6]:
            note = papers_by_id.get(pid, {})
            bibkey = str(note.get("bibkey") or "").strip()
            cite = f" [@{bibkey}]" if bibkey else ""
            tagline = _tagline(note)
            if tagline:
                parts.append(f"  - Evidence: `{pid}`{cite} — {tagline}")
            else:
                parts.append(f"  - Evidence: `{pid}`{cite}")

        parts.append("")

    atomic_write_text(out_path, "\n".join(parts).rstrip() + "\n")
    return 0


def _looks_refined_matrix(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "<!-- SCAFFOLD" in text:
        return False
    if re.search(r"(?i)\b(?:TODO|TBD|FIXME)\b", text):
        return False
    if "- Claim:" in text and len(text.strip()) > 400:
        return True
    return False


def _iter_subsections(outline: list) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for section in outline:
        if not isinstance(section, dict):
            continue
        for subsection in section.get("subsections") or []:
            if not isinstance(subsection, dict):
                continue
            sid = str(subsection.get("id") or "").strip()
            title = str(subsection.get("title") or "").strip()
            if sid and title:
                items.append(
                    {
                        "id": sid,
                        "title": title,
                        "bullets": subsection.get("bullets") or [],
                    }
                )
    return items


def _top_terms(texts: list[str], *, tokenize) -> list[str]:
    stop = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "with",
        "via",
        "using",
        "use",
        "based",
        "new",
        "toward",
        "towards",
    }
    generic = {
        "survey",
        "review",
        "framework",
        "frameworks",
        "system",
        "systems",
        "model",
        "models",
        "approach",
        "approaches",
        "method",
        "methods",
    }
    counts: dict[str, int] = {}
    for text in texts:
        for t in tokenize(text or ""):
            if len(t) < 4:
                continue
            if t in stop or t in generic:
                continue
            counts[t] = counts.get(t, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [t for t, _ in ranked[:8]]


def _make_claim(*, title: str, axes: list[str], themes: list[str]) -> str:
    title = (title or "this subsection").strip()
    axes_hint = " / ".join([_short_axis(a) for a in axes[:2] if a])
    themes_hint = ", ".join([t for t in themes[:3] if t])

    if themes_hint and axes_hint:
        return (
            f"Work in {title} clusters around recurring themes (e.g., {themes_hint}), and the most practical trade-offs tend to show up along {axes_hint}."
        )
    if themes_hint:
        return f"Work in {title} clusters around a small number of recurring themes (e.g., {themes_hint}); comparing them clarifies trade-offs and failure modes."
    if axes_hint:
        return f"For {title}, the key comparisons can be organized along {axes_hint}; these axes explain why methods succeed or fail in different settings."
    return f"For {title}, organizing the literature into a few recurring design patterns makes evaluation and limitations comparable across papers."


def _short_axis(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= 44:
        return text
    return text[:43].rstrip() + "…"


def _tagline(note: dict[str, Any]) -> str:
    method = str(note.get("method") or "").strip()
    if method:
        return method
    bullets = note.get("summary_bullets") or []
    if isinstance(bullets, list):
        for b in bullets:
            b = str(b).strip()
            if b:
                return b
    abstract = str(note.get("abstract") or "").strip()
    if abstract:
        return abstract.splitlines()[0].strip()
    return ""


if __name__ == "__main__":
    raise SystemExit(main())
