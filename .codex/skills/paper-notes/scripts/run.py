from __future__ import annotations

import argparse
import csv
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

    from tooling.common import parse_semicolon_list, read_jsonl, read_tsv, write_jsonl

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["papers/core_set.csv"]
    outputs = parse_semicolon_list(args.outputs) or ["papers/paper_notes.jsonl"]

    core_path = workspace / inputs[0]
    fulltext_index_path = workspace / "papers" / "fulltext_index.jsonl"
    mapping_path = workspace / "outline" / "mapping.tsv"
    dedup_path = workspace / "papers" / "papers_dedup.jsonl"
    out_path = workspace / outputs[0]

    core_rows = _load_core_set(core_path)
    if not core_rows:
        raise SystemExit(f"No rows found in {core_path}")

    metadata = read_jsonl(dedup_path) if dedup_path.exists() else []
    fulltext_by_id = _load_fulltext_index(fulltext_index_path, workspace=workspace)
    mapping_info = _load_mapping(mapping_path) if mapping_path.exists() else {}

    priority_set = _select_priority_papers(core_rows, mapping_info=mapping_info)

    existing_notes_by_id: dict[str, dict[str, Any]] = {}
    if out_path.exists():
        for rec in read_jsonl(out_path):
            if not isinstance(rec, dict):
                continue
            pid = str(rec.get("paper_id") or "").strip()
            if pid:
                existing_notes_by_id[pid] = rec

    used_bibkeys: set[str] = set()
    for rec in existing_notes_by_id.values():
        bibkey = str(rec.get("bibkey") or "").strip()
        if bibkey:
            used_bibkeys.add(bibkey)

    notes: list[dict[str, Any]] = []
    for row in core_rows:
        paper_id = row["paper_id"]
        existing = existing_notes_by_id.get(paper_id)
        if existing:
            notes.append(
                _backfill_note(
                    existing,
                    row=row,
                    meta=_match_metadata(metadata, title=row["title"], year=row.get("year") or "", url=row.get("url") or ""),
                    fulltext_by_id=fulltext_by_id,
                    mapping_info=mapping_info,
                    priority_set=priority_set,
                    workspace=workspace,
                )
            )
            continue

        meta = _match_metadata(metadata, title=row["title"], year=row.get("year") or "", url=row.get("url") or "")
        authors = meta.get("authors") or []
        abstract = str(meta.get("abstract") or "").strip()
        categories = meta.get("categories") or []
        primary_category = str(meta.get("primary_category") or "").strip()

        arxiv_id = str(row.get("arxiv_id") or "").strip() or str(meta.get("arxiv_id") or "").strip()
        pdf_url = str(row.get("pdf_url") or "").strip() or str(meta.get("pdf_url") or "").strip()

        fulltext_path = fulltext_by_id.get(paper_id)
        fulltext_ok = bool(fulltext_path and fulltext_path.exists() and fulltext_path.stat().st_size > 0)
        evidence_level = "fulltext" if fulltext_ok else "abstract"

        priority = "high" if paper_id in priority_set else "normal"
        mapped_sections = sorted(mapping_info.get(paper_id, {}).get("sections", set()))

        bibkey = _make_bibkey(authors=authors, year=str(row.get("year") or ""), title=row["title"], used=used_bibkeys)

        if priority == "high":
            summary_bullets = [
                "TODO: 1–2 sentence summary of the contribution (be specific).",
                "TODO: method/mechanism (what is new vs baselines).",
                "TODO: key results (benchmarks/metrics; include numbers if stated).",
            ]
            method = "TODO: one-sentence method summary."
            key_results = ["TODO: key result (numbers/benchmarks if available)."]
            limitations = ["TODO: concrete limitations/assumptions/failure modes."]
        else:
            summary_bullets = _abstract_to_bullets(abstract)
            method = ""
            key_results = []
            limitations = [f"Evidence level: abstract ({len(abstract)} chars). Validate with full text if used as key evidence."]

        notes.append(
            {
                "paper_id": paper_id,
                "title": row["title"],
                "year": int(row["year"]) if str(row.get("year") or "").isdigit() else str(row.get("year") or ""),
                "url": row.get("url") or "",
                "arxiv_id": arxiv_id,
                "primary_category": primary_category,
                "categories": categories,
                "pdf_url": pdf_url,
                "priority": priority,
                "mapped_sections": mapped_sections,
                "evidence_level": evidence_level,
                "fulltext_path": str(fulltext_path.relative_to(workspace)) if fulltext_ok and fulltext_path else "",
                "authors": authors,
                "abstract": abstract,
                "summary_bullets": summary_bullets,
                "method": method,
                "key_results": key_results,
                "limitations": limitations,
                "bibkey": bibkey,
            }
        )

    write_jsonl(out_path, notes)
    return 0


def _load_core_set(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing core set: {path}")
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            paper_id = str(row.get("paper_id") or "").strip()
            title = str(row.get("title") or "").strip()
            if not paper_id or not title:
                continue
            rows.append(
                {
                    "paper_id": paper_id,
                    "title": title,
                    "year": str(row.get("year") or "").strip(),
                    "url": str(row.get("url") or "").strip(),
                    "arxiv_id": str(row.get("arxiv_id") or "").strip(),
                    "pdf_url": str(row.get("pdf_url") or "").strip(),
                    "reason": str(row.get("reason") or "").strip(),
                }
            )
    return rows


def _load_fulltext_index(path: Path, *, workspace: Path) -> dict[str, Path]:
    from tooling.common import read_jsonl

    out: dict[str, Path] = {}
    if not path.exists():
        return out
    for rec in read_jsonl(path):
        if not isinstance(rec, dict):
            continue
        pid = str(rec.get("paper_id") or "").strip()
        rel = str(rec.get("text_path") or "").strip()
        status = str(rec.get("status") or "").strip()
        if not pid or not rel:
            continue
        if not status.startswith("ok"):
            continue
        p = workspace / rel
        out[pid] = p
    return out


def _load_mapping(path: Path) -> dict[str, dict[str, Any]]:
    by_pid: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return by_pid
    from tooling.common import read_tsv

    for row in read_tsv(path):
        pid = str(row.get("paper_id") or "").strip()
        sid = str(row.get("section_id") or "").strip()
        if not pid or not sid:
            continue
        rec = by_pid.setdefault(pid, {"sections": set(), "count": 0})
        rec["sections"].add(sid)
        rec["count"] += 1
    return by_pid


def _select_priority_papers(core_rows: list[dict[str, str]], *, mapping_info: dict[str, dict[str, Any]]) -> set[str]:
    pinned = {r["paper_id"] for r in core_rows if "pinned_classic" in (r.get("reason") or "")}
    scored: list[tuple[int, str]] = []
    for row in core_rows:
        pid = row["paper_id"]
        count = int(mapping_info.get(pid, {}).get("count") or 0)
        scored.append((count, pid))
    scored.sort(key=lambda t: (-t[0], t[1]))

    core_n = len(core_rows)
    target_n = min(15, max(10, core_n // 4))  # 50 -> 12
    top = {pid for _, pid in scored[:target_n]}
    return set(pinned) | set(top)


def _match_metadata(records: list[dict[str, Any]], *, title: str, year: str, url: str) -> dict[str, Any]:
    from tooling.common import normalize_title_for_dedupe

    if not records:
        return {}
    if url:
        for rec in records:
            if str(rec.get("url") or rec.get("id") or "").strip() == url:
                return rec
    key = f"{normalize_title_for_dedupe(title)}::{year}"
    for rec in records:
        rtitle = str(rec.get("title") or "").strip()
        ryear = str(rec.get("year") or "").strip()
        if f"{normalize_title_for_dedupe(rtitle)}::{ryear}" == key:
            return rec
    return {}


def _make_bibkey(*, authors: list[Any], year: str, title: str, used: set[str]) -> str:
    from tooling.common import tokenize

    last = "Anon"
    if authors and isinstance(authors, list):
        first = str(authors[0]).strip()
        if first:
            last = first.split()[-1]
    keyword = "Work"
    for token in tokenize(title):
        if len(token) >= 4:
            keyword = token
            break
    base = f"{_slug(last)}{year}{_slug(keyword).title()}"
    bibkey = base
    suffix = ord("a")
    while bibkey in used:
        bibkey = f"{base}{chr(suffix)}"
        suffix += 1
    used.add(bibkey)
    return bibkey


def _slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "", text)
    return text or "X"


def _abstract_to_bullets(abstract: str) -> list[str]:
    abstract = (abstract or "").strip()
    if not abstract:
        return []
    # Deterministic scaffold: use first few sentences as bullets (LLM should refine for priority papers).
    parts = re.split(r"(?<=[.!?])\\s+", re.sub(r"\\s+", " ", abstract))
    bullets: list[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        bullets.append(p)
        if len(bullets) >= 3:
            break
    if not bullets:
        bullets = [abstract[:240].strip()]
    return bullets


def _backfill_note(
    existing: dict[str, Any],
    *,
    row: dict[str, str],
    meta: dict[str, Any],
    fulltext_by_id: dict[str, Path],
    mapping_info: dict[str, dict[str, Any]],
    priority_set: set[str],
    workspace: Path,
) -> dict[str, Any]:
    note = dict(existing)
    pid = str(note.get("paper_id") or row.get("paper_id") or "").strip()
    if not pid:
        return note

    note.setdefault("paper_id", pid)
    note.setdefault("title", row.get("title") or "")
    note.setdefault("year", int(row["year"]) if str(row.get("year") or "").isdigit() else str(row.get("year") or ""))
    note.setdefault("url", row.get("url") or "")

    arxiv_id = str(note.get("arxiv_id") or "").strip() or str(row.get("arxiv_id") or "").strip() or str(meta.get("arxiv_id") or "").strip()
    note["arxiv_id"] = arxiv_id
    note.setdefault("primary_category", str(meta.get("primary_category") or "").strip())
    note.setdefault("categories", meta.get("categories") or [])

    pdf_url = str(note.get("pdf_url") or "").strip() or str(row.get("pdf_url") or "").strip() or str(meta.get("pdf_url") or "").strip()
    note["pdf_url"] = pdf_url

    mapped_sections = sorted(mapping_info.get(pid, {}).get("sections", set()))
    note.setdefault("mapped_sections", mapped_sections)
    note["priority"] = "high" if pid in priority_set else str(note.get("priority") or "normal")

    fulltext_path = fulltext_by_id.get(pid)
    fulltext_ok = bool(fulltext_path and fulltext_path.exists() and fulltext_path.stat().st_size > 0)
    note["evidence_level"] = "fulltext" if fulltext_ok else str(note.get("evidence_level") or "abstract")
    if fulltext_ok and fulltext_path:
        note.setdefault("fulltext_path", str(fulltext_path.relative_to(workspace)))
    else:
        note.setdefault("fulltext_path", "")

    note.setdefault("authors", meta.get("authors") or [])
    note.setdefault("abstract", str(meta.get("abstract") or "").strip())

    # Ensure bibkey exists (never overwrite).
    used: set[str] = set()
    bibkey = str(note.get("bibkey") or "").strip()
    if bibkey:
        used.add(bibkey)
    note.setdefault("bibkey", _make_bibkey(authors=note.get("authors") or [], year=str(row.get("year") or ""), title=row.get("title") or "", used=used))
    return note


if __name__ == "__main__":
    raise SystemExit(main())

