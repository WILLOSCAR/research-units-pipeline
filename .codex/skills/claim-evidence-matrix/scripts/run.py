from __future__ import annotations

import argparse
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

    from tooling.common import load_yaml, parse_semicolon_list, read_jsonl, read_tsv, atomic_write_text, tokenize

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["outline/outline.yml", "papers/paper_notes.jsonl"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/claim_evidence_matrix.md"]

    outline_path = workspace / inputs[0]
    notes_path = workspace / inputs[1]
    mapping_path = workspace / "outline/mapping.tsv"
    out_path = workspace / outputs[0]

    # Bootstrap-only behavior: if a human/LLM already refined the matrix, do not overwrite.
    # Delete `outline/claim_evidence_matrix.md` to force regeneration.
    if _looks_refined_matrix(out_path):
        return 0

    outline = load_yaml(outline_path) or []
    notes = read_jsonl(notes_path)
    mappings = read_tsv(mapping_path) if mapping_path.exists() else []

    papers_by_id = {str(n.get("paper_id") or ""): n for n in notes}
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
        "<!-- SCAFFOLD: claim-evidence-matrix (LLM should rewrite claims into specific, falsifiable statements) -->",
        "",
    ]
    for subsection in _iter_subsections(outline):
        sid = subsection["id"]
        title = subsection["title"]
        pids = mapped_by_section.get(sid, [])
        uniq = []
        for pid in pids:
            if pid in papers_by_id and pid not in uniq:
                uniq.append(pid)
        if len(uniq) < 2 and paper_ids_fallback:
            for cand in paper_ids_fallback:
                if cand not in uniq:
                    uniq.append(cand)
                if len(uniq) >= 2:
                    break

        parts.append(f"## {sid} {title}")
        parts.append("")
        axes = [str(b).strip() for b in (subsection.get("bullets") or []) if str(b).strip()]
        themes = _top_terms([str(papers_by_id.get(pid, {}).get("title") or "") for pid in uniq], tokenize=tokenize)
        parts.append(
            "- Claim: TODO（写成可证伪的主张：机制/假设/结果/对比结论；避免“围绕/主要在…维度上存在差异”的模板句）"
        )
        if axes:
            parts.append(f"  - Axes (from outline): {'；'.join(axes[:5])}")
        if themes:
            parts.append(f"  - Candidate themes (from mapped titles): {'、'.join(themes[:5])}")
        for pid in uniq[:6]:
            note = papers_by_id.get(pid, {})
            tagline = _tagline(note)
            bibkey = str(note.get("bibkey") or "").strip()
            cite = f" [@{bibkey}]" if bibkey else ""
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
    if "TODO" in text:
        return False
    # Basic signal: contains some claim lines and looks non-empty.
    if "- Claim:" in text and len(text.strip()) > 200:
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


def _top_terms(titles: list[str], *, tokenize) -> list[str]:
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
        "agent",
        "agents",
        "llm",
        "language",
        "models",
    }
    counts: dict[str, int] = {}
    for title in titles:
        for t in tokenize(title or ""):
            if len(t) < 4:
                continue
            if t in stop or t in generic:
                continue
            counts[t] = counts.get(t, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [t for t, _ in ranked[:6]]


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
