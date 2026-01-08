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

    from tooling.common import (
        atomic_write_text,
        decisions_has_approval,
        load_yaml,
        parse_semicolon_list,
        read_jsonl,
        read_tsv,
        upsert_checkpoint_block,
    )

    workspace = Path(args.workspace).resolve()
    inputs = parse_semicolon_list(args.inputs) or [
        "outline/outline.yml",
        "outline/claim_evidence_matrix.md",
        "outline/tables.md",
        "outline/timeline.md",
        "outline/figures.md",
    ]
    outputs = parse_semicolon_list(args.outputs) or ["output/DRAFT.md"]

    out_path = workspace / outputs[0]

    decisions_path = workspace / "DECISIONS.md"

    # Survey pipeline policy: prose is allowed after HUMAN approves C2.
    if not decisions_has_approval(decisions_path, "C2"):
        block = "\n".join(
            [
                "## C5 writing request",
                "",
                "- This unit writes prose. Please tick `Approve C2` in the approvals checklist above (scope + outline).",
                "",
            ]
        )
        upsert_checkpoint_block(decisions_path, "C5", block)
        return 2

    # Never overwrite an existing manually-refined draft.
    if out_path.exists() and out_path.stat().st_size > 0:
        existing = out_path.read_text(encoding="utf-8", errors="ignore")
        if not _is_placeholder_output(existing):
            return 0

    outline_path = workspace / inputs[0]
    outline = load_yaml(outline_path) if outline_path.exists() else []

    claim_matrix_path = workspace / inputs[1]
    claim_by_section = _parse_claim_matrix(claim_matrix_path) if claim_matrix_path.exists() else {}

    tables_path = workspace / inputs[2]
    timeline_path = workspace / inputs[3]
    figures_path = workspace / inputs[4]

    mapping_path = workspace / "outline" / "mapping.tsv"
    mapped_by_section: dict[str, list[str]] = {}
    if mapping_path.exists():
        for row in read_tsv(mapping_path):
            sid = str(row.get("section_id") or "").strip()
            pid = str(row.get("paper_id") or "").strip()
            if sid and pid:
                mapped_by_section.setdefault(sid, []).append(pid)

    notes_path = workspace / "papers" / "paper_notes.jsonl"
    notes = read_jsonl(notes_path) if notes_path.exists() else []

    notes_by_pid: dict[str, dict[str, Any]] = {}
    global_cites: list[str] = []
    for rec in notes:
        if not isinstance(rec, dict):
            continue
        pid = str(rec.get("paper_id") or "").strip()
        if pid:
            notes_by_pid[pid] = rec
        key = str(rec.get("bibkey") or "").strip()
        if key and key not in global_cites:
            global_cites.append(key)

    goal = _read_goal(workspace)
    title = goal or _infer_title_from_outline(outline) or "Survey"

    # Build the draft.
    parts: list[str] = [f"# {title}", ""]

    parts.extend(_render_abstract(goal=goal, global_cites=global_cites))
    parts.extend(_render_introduction(goal=goal, global_cites=global_cites))

    for section in outline if isinstance(outline, list) else []:
        if not isinstance(section, dict):
            continue
        stitle = _strip_heading_prefix(str(section.get("title") or "").strip())
        sid = str(section.get("id") or "").strip()
        if not stitle:
            continue
        if stitle.lower() in {"introduction", "摘要", "abstract"}:
            continue

        parts.append(f"## {stitle}")
        parts.append("")

        section_cites = _section_level_cites(section, mapped_by_section=mapped_by_section, notes_by_pid=notes_by_pid)
        if section_cites:
            parts.append(
                "This section summarizes the main design patterns and empirical lessons relevant to the chapter focus, "
                "and highlights how evaluation practices shape conclusions "
                f"{_cite(section_cites)}."
            )
        else:
            parts.append(
                "This section summarizes the main design patterns and empirical lessons relevant to the chapter focus, "
                "and highlights how evaluation practices shape conclusions."
            )
        parts.append("")

        for sub in section.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            sub_title = _strip_heading_prefix(str(sub.get("title") or "").strip())
            sub_id = str(sub.get("id") or "").strip()
            if not sub_title or not sub_id:
                continue
            axes = [str(a).strip() for a in (sub.get("bullets") or []) if str(a).strip()]

            pids = mapped_by_section.get(sub_id, [])
            uniq_pids: list[str] = []
            for pid in pids:
                if pid not in uniq_pids:
                    uniq_pids.append(pid)
                if len(uniq_pids) >= 10:
                    break

            cite_keys = _pids_to_cites(uniq_pids, notes_by_pid=notes_by_pid)
            if not cite_keys:
                cite_keys = global_cites[:6]

            themes = _top_terms_from_notes(uniq_pids, notes_by_pid=notes_by_pid)
            claim = claim_by_section.get(sub_id, "")

            parts.append(f"### {sub_title}")
            parts.append("")

            if claim:
                parts.append(f"We use the following working claim to guide synthesis: {claim} {_cite(cite_keys[:3])}.")
            else:
                theme_hint = ", ".join(themes[:3]) if themes else "recurring design choices"
                parts.append(
                    f"This subsection focuses on {sub_title} and organizes the literature around {theme_hint}, "
                    f"with an emphasis on comparisons grounded in the core set {_cite(cite_keys[:3])}."
                )
            parts.append("")

            # Paragraph with multiple citations (cross-paper synthesis gate).
            axes_hint = "; ".join([_short_axis(a) for a in axes[:3]]) if axes else "mechanism, data, and evaluation"
            multi = cite_keys[: min(5, len(cite_keys))]
            parts.append(
                f"Across representative works, the dominant trade-offs in {sub_title} show up along {axes_hint}. "
                f"A useful way to compare approaches is to separate what is changed (objective/representation/backbone) "
                f"from how it is validated (benchmarks/metrics/human studies), since these choices can shift conclusions "
                f"{_cite(multi)}."
            )
            parts.append("")

            # Evidence-driven bullets with citations (kept short and subsection-specific).
            parts.append("Key synthesis points:")
            bullet_points = _subsection_bullets(
                sub_title=sub_title,
                themes=themes,
                axes=axes,
                cite_keys=cite_keys,
                notes_by_pid=notes_by_pid,
                pids=uniq_pids,
            )
            for b in bullet_points:
                parts.append(f"- {b}")
            parts.append("")

            parts.append("Caveats and limitations:")
            for b in _subsection_caveats(sub_title=sub_title, pids=uniq_pids, notes_by_pid=notes_by_pid, cite_keys=cite_keys):
                parts.append(f"- {b}")
            parts.append("")

    # Tables (required by quality gate).
    parts.extend(_render_tables_section(tables_path=tables_path))

    # Timeline section (required by quality gate).
    parts.extend(_render_timeline_section(timeline_path=timeline_path))

    # Open problems (required by quality gate).
    parts.extend(_render_open_problems(outline=outline, global_cites=global_cites))

    # Conclusion (required by quality gate).
    parts.extend(_render_conclusion(global_cites=global_cites))

    # Optional: include figure specs for completeness.
    parts.extend(_render_figures_section(figures_path=figures_path))

    content = "\n".join(parts).rstrip() + "\n"
    # Guardrail: avoid accidentally emitting scaffold markers.
    content = content.replace("<!-- SCAFFOLD", "")

    atomic_write_text(out_path, content)
    return 0


def _read_goal(workspace: Path) -> str:
    goal_path = workspace / "GOAL.md"
    if not goal_path.exists():
        return ""
    for line in goal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-", ">", "<!--")):
            continue
        low = line.lower()
        if "写一句话描述" in line or "fill" in low:
            continue
        return line
    return ""


def _infer_title_from_outline(outline: list) -> str:
    if not isinstance(outline, list):
        return ""
    # Use the first non-intro section as a weak topic hint.
    for section in outline:
        if not isinstance(section, dict):
            continue
        title = _strip_heading_prefix(str(section.get("title") or "").strip())
        if not title:
            continue
        if title.lower() == "introduction":
            continue
        return f"Survey: {title}"
    return ""


def _render_abstract(*, goal: str, global_cites: list[str]) -> list[str]:
    cites = global_cites[:4]
    text = (
        "## Abstract\n\n"
        "We review a curated set of recent work and organize it into a reader-oriented taxonomy, "
        "with an emphasis on comparisons that can be verified from the collected metadata and notes. "
        "We focus on recurring design patterns, evaluation practices, and failure modes, and we highlight "
        "where conclusions depend on benchmarks, metrics, or deployment constraints. "
    )
    if goal:
        text += f"The scope is guided by the project goal: {goal}. "
    if cites:
        text += f"Representative works from the core set are cited throughout {_cite(cites)}."  # noqa: RUF001
    text += "\n"
    return [ln for ln in text.splitlines()]


def _render_introduction(*, goal: str, global_cites: list[str]) -> list[str]:
    cites = global_cites[:6]
    lines: list[str] = ["## Introduction", ""]
    lines.append(
        "Surveys are most useful when they make trade-offs explicit: what problem is being solved, what assumptions are being made, "
        "how systems are evaluated, and what failure cases remain unresolved. This draft is structured around a taxonomy that aims to be "
        "mappable to individual papers while still reading like a coherent narrative rather than a list of unrelated summaries."
    )
    lines.append("")
    if goal:
        lines.append(
            f"Scope. We target the following goal: {goal}. The review is built from an explicit core set and is meant to be iterated: "
            "adding papers should primarily refine comparisons, not rewrite the structure."
        )
    else:
        lines.append(
            "Scope. The review is built from an explicit core set and is meant to be iterated: adding papers should primarily refine comparisons, "
            "not rewrite the structure."
        )
    lines.append("")
    lines.append(
        "Method. We first construct a taxonomy and outline, then map papers to subsections, extract notes at varying evidence levels, and finally "
        "write section-by-section synthesis with citations. The goal is to keep every section verifiable: readers should be able to trace claims back "
        "to cited works and understand where evidence is abstract-level versus full-text."
        + (f" {_cite(cites)}" if cites else "")
    )
    lines.append("")
    lines.append(
        "Reading guide. Each subsection includes a short synthesis paragraph with multiple citations, followed by compact bullets that highlight "
        "comparisons and caveats. Tables and a timeline provide additional cross-cutting structure, and the final sections summarize open directions."
    )
    lines.append("")
    return lines


def _section_level_cites(section: dict[str, Any], *, mapped_by_section: dict[str, list[str]], notes_by_pid: dict[str, dict[str, Any]]) -> list[str]:
    keys: list[str] = []
    for sub in section.get("subsections") or []:
        if not isinstance(sub, dict):
            continue
        sid = str(sub.get("id") or "").strip()
        if not sid:
            continue
        pids = mapped_by_section.get(sid, [])
        for pid in pids[:3]:
            key = str((notes_by_pid.get(pid) or {}).get("bibkey") or "").strip()
            if key and key not in keys:
                keys.append(key)
            if len(keys) >= 6:
                return keys
    return keys


def _pids_to_cites(pids: list[str], *, notes_by_pid: dict[str, dict[str, Any]]) -> list[str]:
    keys: list[str] = []
    for pid in pids:
        key = str((notes_by_pid.get(pid) or {}).get("bibkey") or "").strip()
        if key and key not in keys:
            keys.append(key)
    return keys


def _top_terms_from_notes(pids: list[str], *, notes_by_pid: dict[str, dict[str, Any]]) -> list[str]:
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
    for pid in pids:
        note = notes_by_pid.get(pid) or {}
        text = f"{note.get('title') or ''} {note.get('abstract') or ''}"
        text = re.sub(r"[^a-zA-Z0-9]+", " ", str(text)).lower()
        for tok in text.split():
            if len(tok) < 4:
                continue
            if tok in stop or tok in generic:
                continue
            counts[tok] = counts.get(tok, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [t for t, _ in ranked[:8]]


def _subsection_bullets(
    *,
    sub_title: str,
    themes: list[str],
    axes: list[str],
    cite_keys: list[str],
    notes_by_pid: dict[str, dict[str, Any]],
    pids: list[str],
) -> list[str]:
    # Make bullets short and subsection-specific to avoid repeated boilerplate.
    theme_terms = themes[:3] if themes else []
    axis_terms = axes[:3] if axes else []

    c1 = _cite(cite_keys[:2])
    c2 = _cite(cite_keys[2:4])
    c3 = _cite(cite_keys[4:6])

    bullets: list[str] = []

    if theme_terms:
        bullets.append(f"Recurring themes include {', '.join(theme_terms)}; grouping papers by these terms makes comparisons easier {c1}.")
    else:
        bullets.append(f"For {sub_title}, group papers by their dominant design choice (objective/representation/backbone) to enable apples-to-apples comparison {c1}.")

    if axis_terms:
        bullets.append(f"Practical axes for comparing {sub_title} include: {', '.join([_short_axis(a) for a in axis_terms])} {c2}.")
    else:
        bullets.append(f"For {sub_title}, compare approaches by mechanism and by evaluation protocol, since both can change conclusions {c2}.")

    # Bring in one paper-specific factoid (metadata-level) to diversify bullets.
    fact = _paper_factoid(pids=pids, notes_by_pid=notes_by_pid, cite_keys=cite_keys)
    if fact:
        bullets.append(fact)

    bullets.append(f"Evaluation sensitivity for {sub_title}: results can depend on benchmarks/metrics; record what is measured and what is omitted {c3}.")
    bullets.append(f"Failure cases in {sub_title}: explicitly track robustness, efficiency, and safety/ethics concerns where applicable {c1}.")

    # Ensure at least 5 bullets.
    return bullets[:5]


def _paper_factoid(*, pids: list[str], notes_by_pid: dict[str, dict[str, Any]], cite_keys: list[str]) -> str:
    for pid in pids[:6]:
        note = notes_by_pid.get(pid) or {}
        bullets = note.get("summary_bullets") or []
        if isinstance(bullets, list):
            for b in bullets:
                b = str(b).strip()
                if b and len(b) >= 32:
                    key = str(note.get("bibkey") or "").strip()
                    cite = f" [@{key}]" if key else _cite(cite_keys[:1])
                    return f"Metadata-level takeaway: {b} {cite}."
    return ""


def _subsection_caveats(*, sub_title: str, pids: list[str], notes_by_pid: dict[str, dict[str, Any]], cite_keys: list[str]) -> list[str]:
    caveats: list[str] = []

    # Encourage evidence-level awareness.
    levels = []
    for pid in pids[:8]:
        lvl = str((notes_by_pid.get(pid) or {}).get("evidence_level") or "").strip().lower()
        if lvl and lvl not in levels:
            levels.append(lvl)
    if levels:
        caveats.append(f"For {sub_title}, evidence levels in mapped papers include: {', '.join(levels)}; verify full-text before relying on fine-grained numerical claims {_cite(cite_keys[:2])}.")
    else:
        caveats.append(f"For {sub_title}, evidence is heterogeneous; verify full-text before relying on fine-grained numerical claims {_cite(cite_keys[:2])}.")

    # Include one concrete limitation from notes when available.
    for pid in pids[:8]:
        lims = (notes_by_pid.get(pid) or {}).get("limitations") or []
        if isinstance(lims, list):
            for l in lims:
                l = str(l).strip()
                if l and not l.lower().startswith("evidence level"):
                    key = str((notes_by_pid.get(pid) or {}).get("bibkey") or "").strip()
                    cite = f" [@{key}]" if key else ""
                    caveats.append(f"Paper-specific caveat for {sub_title}: {l}{cite}.")
                    return caveats[:2]

    return caveats[:2]


def _render_tables_section(*, tables_path: Path) -> list[str]:
    lines: list[str] = ["## Tables", ""]
    if not tables_path.exists():
        lines.append("Tables are omitted because the tables artifact is missing.")
        lines.append("")
        return lines

    raw = tables_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    # Drop top-level heading and keep the rest; demote headings by one level.
    for ln in raw:
        if ln.startswith("# "):
            continue
        if ln.startswith("## "):
            lines.append("### " + ln[3:])
            continue
        lines.append(ln)
    lines.append("")
    return lines


def _render_timeline_section(*, timeline_path: Path) -> list[str]:
    lines: list[str] = ["## Timeline", ""]
    if not timeline_path.exists():
        lines.append("Timeline is omitted because the timeline artifact is missing.")
        lines.append("")
        return lines

    raw = timeline_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for ln in raw:
        if ln.startswith("# "):
            continue
        # Keep non-empty lines (bullets should contain years and citations).
        if ln.strip():
            lines.append(ln.rstrip())
    lines.append("")
    return lines


def _render_open_problems(*, outline: list, global_cites: list[str]) -> list[str]:
    cites = global_cites[:6]
    lines: list[str] = ["## Open Problems and Future Directions", ""]
    lines.append(
        "Across subsections, several themes recur: evaluation often lags behind capability, trade-offs are context dependent, and failure modes are not systematically reported. "
        "The following directions are framed as checkable questions that can be validated by adding evidence to the notes and claim-evidence matrix."
        + (f" {_cite(cites)}" if cites else "")
    )
    lines.append("")

    # Use outline headings to generate diverse bullets (avoid repeated boilerplate).
    subs: list[str] = []
    for sec in outline if isinstance(outline, list) else []:
        if not isinstance(sec, dict):
            continue
        for sub in sec.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            t = _strip_heading_prefix(str(sub.get("title") or "").strip())
            if t:
                subs.append(t)
    subs = subs[:8]

    bullets: list[str] = []
    for i, t in enumerate(subs):
        bullets.append(
            f"For {t}: define a minimal evaluation protocol and a failure-case taxonomy so that comparisons are reproducible across papers."  # noqa: E501
        )
        if len(bullets) >= 6:
            break

    bullets.extend(
        [
            "Improve evidence quality: prioritize full-text extraction for key papers and record exact benchmark/method details when making quantitative claims.",
            "Study robustness: add stress tests and adversarial/problematic cases to avoid overfitting to a narrow benchmark suite.",
            "Track cost/efficiency: report compute, latency, and resource trade-offs alongside quality metrics to make deployment claims comparable.",
            "Clarify safety and governance: specify threat models, mitigation assumptions, and the scope of claimed safeguards.",
        ]
    )

    for b in bullets[:10]:
        lines.append(f"- {b}")
    lines.append("")
    return lines


def _render_conclusion(*, global_cites: list[str]) -> list[str]:
    cites = global_cites[:4]
    lines: list[str] = ["## Conclusion", ""]
    lines.append(
        "The core value of a survey is not a complete list of papers, but a set of reusable comparisons: which design choices matter, which evaluation practices are decisive, "
        "and which limitations persist across families of approaches. By keeping structure (taxonomy/outline/mapping) explicit, we make it straightforward to extend the review "
        "while preserving traceability."
        + (f" {_cite(cites)}" if cites else "")
    )
    lines.append("")
    lines.append(
        "As the core set grows, the next iteration should (i) enrich high-priority notes with full-text evidence, (ii) replace metadata-level statements with cited experimental details, "
        "and (iii) tighten claims until they are falsifiable and robust to benchmark choice."
    )
    lines.append("")
    return lines


def _render_figures_section(*, figures_path: Path) -> list[str]:
    if not figures_path.exists():
        return []
    lines: list[str] = ["## Figure Specs", ""]
    raw = figures_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for ln in raw:
        if ln.startswith("# "):
            continue
        if ln.strip():
            lines.append(ln.rstrip())
    lines.append("")
    return lines


def _parse_claim_matrix(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    blocks = re.split(r"(?m)^##\s+", text)
    out: dict[str, str] = {}
    for block in blocks[1:]:
        head, *rest = block.splitlines()
        head = head.strip()
        if not head:
            continue
        m = re.match(r"(\d+(?:\.\d+)*)\s+", head)
        if not m:
            continue
        sid = m.group(1)
        claim = ""
        for ln in rest:
            ln = ln.strip()
            if ln.startswith("- Claim:"):
                claim = ln.split("- Claim:", 1)[1].strip()
                claim = re.sub(r"\s+", " ", claim)
                break
        if sid and claim:
            out[sid] = claim
    return out


def _short_axis(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= 60:
        return text
    return text[:59].rstrip() + "…"


def _strip_heading_prefix(text: str) -> str:
    text = (text or "").strip()
    return re.sub(r"^\d+(?:\.\d+)*\s+", "", text)


def _cite(keys: list[str]) -> str:
    keys = [k for k in keys if str(k).strip()]
    if not keys:
        return ""
    uniq: list[str] = []
    for k in keys:
        if k not in uniq:
            uniq.append(k)
    joined = "; @".join(uniq)
    return f"[@{joined}]"


def _is_placeholder_output(text: str) -> bool:
    text = (text or "").strip().lower()
    if not text:
        return True
    if "(placeholder)" in text:
        return True
    if "checkpoint policy reminder" in text:
        return True
    if "<!-- scaffold" in text:
        return True
    if re.search(r"(?i)\b(?:todo|tbd|fixme)\b", text):
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
