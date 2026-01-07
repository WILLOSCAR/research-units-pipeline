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
    parser.add_argument("--verification-note", default="auto-generated; verify manually if needed")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import ensure_dir, parse_semicolon_list, read_jsonl, today_iso, write_jsonl, atomic_write_text

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or ["papers/paper_notes.jsonl"]
    outputs = parse_semicolon_list(args.outputs) or ["citations/ref.bib", "citations/verified.jsonl"]

    notes_path = workspace / inputs[0]
    bib_path = workspace / outputs[0]
    verified_path = workspace / outputs[1] if len(outputs) > 1 else workspace / "citations/verified.jsonl"

    notes = read_jsonl(notes_path)
    if not notes:
        raise SystemExit(f"No paper notes found: {notes_path}")

    ensure_dir(bib_path.parent)
    ensure_dir(verified_path.parent)

    bib_entries: list[str] = []
    verified: list[dict[str, Any]] = []
    for note in notes:
        bibkey = str(note.get("bibkey") or "").strip()
        title = str(note.get("title") or "").strip()
        url = str(note.get("url") or "").strip()
        year = note.get("year")
        authors = note.get("authors") or []
        author_field = _bibtex_author(authors)
        year_field = str(year) if year is not None else ""
        arxiv_id = _arxiv_id_from_note(note)
        primary_class = str(note.get("primary_category") or "").strip()

        if not bibkey:
            continue

        bib_entries.append(_bibtex_entry(bibkey=bibkey, title=title, author=author_field, year=year_field, url=url, arxiv_id=arxiv_id, primary_class=primary_class))
        verified.append(
            {
                "bibkey": bibkey,
                "title": title,
                "url": url,
                "date": today_iso(),
                "notes": args.verification_note,
            }
        )

    atomic_write_text(bib_path, "% Auto-generated BibTeX (verify as needed)\n\n" + "".join(bib_entries))
    write_jsonl(verified_path, verified)
    return 0


def _bibtex_author(authors: Any) -> str:
    if isinstance(authors, list) and authors:
        return " and ".join([str(a).strip() for a in authors if str(a).strip()])
    if isinstance(authors, str) and authors.strip():
        return authors.strip()
    return ""


def _escape_tex(text: str) -> str:
    text = text or ""
    return re.sub(r"([{}])", r"\\\1", text)


def _arxiv_id_from_note(note: dict[str, Any]) -> str:
    arxiv_id = str(note.get("arxiv_id") or "").strip()
    if arxiv_id:
        return _strip_arxiv_version(arxiv_id)
    url = str(note.get("url") or "").strip()
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^/?#]+)", url)
    if not m:
        return ""
    return _strip_arxiv_version(m.group(1))


def _strip_arxiv_version(arxiv_id: str) -> str:
    # 2509.03990v2 -> 2509.03990
    arxiv_id = (arxiv_id or "").strip()
    return re.sub(r"v\d+$", "", arxiv_id)


def _bibtex_entry(*, bibkey: str, title: str, author: str, year: str, url: str, arxiv_id: str, primary_class: str) -> str:
    fields: list[str] = []
    if arxiv_id:
        fields.append(f"@article{{{bibkey},")
        fields.append(f"  title        = {{{_escape_tex(title)}}},")
        fields.append(f"  author       = {{{_escape_tex(author)}}},")
        fields.append(f"  year         = {{{_escape_tex(year)}}},")
        fields.append(f"  journal      = {{arXiv preprint arXiv:{_escape_tex(arxiv_id)}}},")
        fields.append(f"  eprint       = {{{_escape_tex(arxiv_id)}}},")
        fields.append("  archivePrefix= {arXiv},")
        if primary_class:
            fields.append(f"  primaryClass = {{{_escape_tex(primary_class)}}},")
        if url:
            fields.append(f"  url          = {{{_escape_tex(url)}}},")
        fields.append("}")
        fields.append("")
        return "\n".join(fields)

    # Fallback: minimal @misc.
    fields.append(f"@misc{{{bibkey},")
    fields.append(f"  title        = {{{_escape_tex(title)}}},")
    fields.append(f"  author       = {{{_escape_tex(author)}}},")
    fields.append(f"  year         = {{{_escape_tex(year)}}},")
    if url:
        fields.append(f"  howpublished = {{\\url{{{_escape_tex(url)}}}}},")
    fields.append("}")
    fields.append("")
    return "\n".join(fields)


if __name__ == "__main__":
    raise SystemExit(main())
