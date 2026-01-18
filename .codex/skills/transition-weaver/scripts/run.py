from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def _stable_choice(key: str, options: list[str]) -> str:
    """Deterministic choice (stable across runs) while allowing rich template variety."""

    if not options:
        return ""
    digest = hashlib.sha1((key or "").encode("utf-8", errors="ignore")).hexdigest()
    idx = int(digest[:8], 16) % len(options)
    return options[idx]


def _load_subsection_briefs(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return {}
    out: dict[str, dict[str, Any]] = {}
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        sid = str(rec.get("sub_id") or "").strip()
        if sid:
            out[sid] = rec
    return out


def _iter_outline_boundaries(outline: Any) -> dict[str, list[tuple[str, str]]]:
    """Return adjacency boundaries for transition generation.

    Keys:
      - within_h3: (sub_id -> next_sub_id) pairs within the same H2.
      - h2_openers: (section_title -> first_sub_id) openers per H2.
      - h2_closers: (last_sub_id -> next_section_title) handoffs between H2s.
      - between_h2: (section_title -> next_section_title) pairs.
    """

    out: dict[str, list[tuple[str, str]]] = {"within_h3": [], "h2_openers": [], "h2_closers": [], "between_h2": []}

    if not isinstance(outline, list):
        return out

    sections: list[dict[str, Any]] = []
    for sec in outline:
        if isinstance(sec, dict):
            sections.append(sec)

    for i, sec in enumerate(sections):
        sec_title = str(sec.get("title") or "").strip()
        subs = sec.get("subsections") or []
        sub_ids: list[str] = []
        if isinstance(subs, list):
            for sub in subs:
                if not isinstance(sub, dict):
                    continue
                sid = str(sub.get("id") or "").strip()
                if sid:
                    sub_ids.append(sid)

        if sec_title and sub_ids:
            out["h2_openers"].append((sec_title, sub_ids[0]))

        for a, b in zip(sub_ids, sub_ids[1:]):
            out["within_h3"].append((a, b))

        if i < len(sections) - 1:
            next_title = str(sections[i + 1].get("title") or "").strip()
            if sec_title and next_title:
                out["between_h2"].append((sec_title, next_title))
            if sub_ids and next_title:
                out["h2_closers"].append((sub_ids[-1], next_title))

    return out


def _short_list(items: Any, *, limit: int = 4) -> list[str]:
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for x in items:
        s = str(x or "").strip()
        if not s:
            continue
        if s not in out:
            out.append(s)
        if len(out) >= int(limit):
            break
    return out


def _focus_terms(rec: dict[str, Any]) -> str:
    """Pick subsection-specific, no-facts handles to mention in transitions.

    Return a short phrase (no planner-talk enumerations).
    """

    parts: list[str] = []

    for t in _short_list(rec.get("bridge_terms"), limit=3):
        if t and t not in parts:
            parts.append(t)

    for a in _short_list(rec.get("axes"), limit=2):
        if a and a not in parts:
            parts.append(a)

    hook = str(rec.get("contrast_hook") or "").strip()
    if hook and hook not in parts:
        parts.append(hook)

    # Keep it short and readable; avoid semicolon-style construction notes.
    return " / ".join(parts[:3]).strip()

def _h3_transition(*, a_id: str, b_id: str, briefs: dict[str, dict[str, Any]]) -> str:
    a = briefs.get(a_id) or {}
    b = briefs.get(b_id) or {}

    a_title = str(a.get("title") or a_id).strip()
    b_title = str(b.get("title") or b_id).strip()

    a_focus = _focus_terms(a) or a_title
    b_focus = _focus_terms(b) or b_title

    # Paper voice, no planner talk: established point -> remaining uncertainty -> why next.
    variants = [
        f"The remaining uncertainty is {b_focus}, and resolving it makes the next trade-offs easier to interpret.",
        f"With {a_focus} as context, {b_focus} becomes the next handle for comparing approaches under shared constraints.",
        f"Where the previous subsection frames the decision, {b_focus} pins down what later comparisons can be meaningfully attributed to.",
        f"To keep the chapter’s contrasts coherent, we next focus on {b_focus} as the comparison lens.",
        f"{b_focus} sharpens the throughline by making key assumptions explicit before we interpret results across studies.",
    ]

    sent = _stable_choice(f"h3:{a_id}:{a_focus}->{b_id}:{b_focus}", variants)
    return f"- {a_id} → {b_id}: {sent}"

def _h2_opener(*, sec_title: str, first_sub_id: str, briefs: dict[str, dict[str, Any]]) -> str:
    b = briefs.get(first_sub_id) or {}
    b_title = str(b.get("title") or first_sub_id).strip()
    b_focus = _focus_terms(b) or "shared comparison handles"

    variants = [
        f"{sec_title} opens with {b_title} to establish {b_focus} as the common lens reused across the chapter.",
        f"{sec_title} begins with {b_title}, translating the theme into {b_focus} that later subsections can vary and stress-test.",
        f"To ground {sec_title}, {b_title} pins down {b_focus} before the chapter layers on additional constraints.",
        f"{b_title} is the first step in {sec_title}: it fixes {b_focus} so subsequent comparisons do not drift.",
        f"{sec_title} begins at {b_title}, where {b_focus} turns a broad topic into concrete evaluation-ready handles.",
    ]

    sent = _stable_choice(f"h2open:{sec_title}->{first_sub_id}:{b_title}:{b_focus}", variants)
    return f"- {sec_title} → {first_sub_id}: {sent}"


def _h2_handoff(*, last_sub_id: str, next_sec_title: str, briefs: dict[str, dict[str, Any]]) -> str:
    a = briefs.get(last_sub_id) or {}
    a_title = str(a.get("title") or last_sub_id).strip()
    a_focus = _focus_terms(a) or a_title

    variants = [
        f"With the local trade-offs around {a_focus} established, {next_sec_title} broadens the lens to what remains unresolved at the next layer.",
        f"{next_sec_title} builds on the preceding contrasts by shifting the lens while keeping {a_focus} as the bridge.",
        f"Having grounded the chapter in {a_focus}, {next_sec_title} turns to a different source of variation, such as interfaces, constraints, or evaluation emphasis.",
        f"{next_sec_title} follows by revisiting the same theme under a different constraint set, using {a_focus} as the reference point.",
        f"{a_focus} provides the immediate context, and {next_sec_title} asks what changes when we change the lens.",
    ]

    sent = _stable_choice(f"h2handoff:{last_sub_id}:{a_focus}->{next_sec_title}", variants)
    return f"- {last_sub_id} → {next_sec_title}: {sent}"

def _h2_to_h2(*, a_title: str, b_title: str) -> str:
    # Paper-like handoff: keep it as an argument bridge, not title narration.
    variants = [
        f"{b_title} builds on {a_title} by tightening the lens on what is compared, under what constraints, and why those constraints matter.",
        f"{b_title} follows from {a_title} by shifting from motivation to decisions and the evidence used to judge them.",
        f"{b_title} continues the argument by foregrounding the comparison handles that recur across the later sections.",
        f"{b_title} complements {a_title} by focusing on how claims are operationalized in protocols, metrics, and failure cases.",
        f"{b_title} extends {a_title} by making the next layer concrete: what varies, what stays fixed, and what we can conclude under that setup.",
    ]

    sent = _stable_choice(f"h2:{a_title}->{b_title}", variants)
    return f"- {a_title} → {b_title}: {sent}"

def _render_transitions(*, outline: Any, briefs: dict[str, dict[str, Any]]) -> str:
    b = _iter_outline_boundaries(outline)
    within = b.get("within_h3") or []
    openers = b.get("h2_openers") or []
    handoffs = b.get("h2_closers") or []
    between = b.get("between_h2") or []

    lines: list[str] = [
        "# Transitions (no new facts; no citations)",
        "",
        "- Guardrail: transitions add no new facts and introduce no new citations.",
        "- Use these as hand-offs: what was established → what remains unclear → why the next unit follows.",
        "",
        "## Section openers (H2 → first H3)",
    ]

    if openers:
        for sec_title, first_sub_id in openers:
            lines.append(_h2_opener(sec_title=sec_title, first_sub_id=first_sub_id, briefs=briefs))
    else:
        lines.append("- (no section openers detected)")

    lines.extend(["", "## Within-section (H3 → next H3)", ""])
    if within:
        for a_id, b_id in within:
            lines.append(_h3_transition(a_id=a_id, b_id=b_id, briefs=briefs))
    else:
        lines.append("- (no within-section pairs detected)")

    lines.extend(["", "## Between sections (last H3 → next H2)", ""])
    if handoffs:
        for last_sub_id, next_sec_title in handoffs:
            lines.append(_h2_handoff(last_sub_id=last_sub_id, next_sec_title=next_sec_title, briefs=briefs))
    else:
        lines.append("- (no section handoffs detected)")

    lines.extend(["", "## Between sections (H2 → next H2)", ""])
    if between:
        for a_title, b_title in between:
            lines.append(_h2_to_h2(a_title=a_title, b_title=b_title))
    else:
        lines.append("- (no H2 adjacency detected)")

    lines.append("")
    return "\n".join(lines)


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

    from tooling.common import atomic_write_text, ensure_dir, load_yaml, parse_semicolon_list
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or "U098").strip() or "U098"

    inputs = parse_semicolon_list(args.inputs) or ["outline/outline.yml", "outline/subsection_briefs.jsonl"]
    outputs = parse_semicolon_list(args.outputs) or ["outline/transitions.md"]

    out_rel = outputs[0] if outputs else "outline/transitions.md"
    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    freeze_marker = out_path.with_name("transitions.refined.ok")
    if out_path.exists() and out_path.stat().st_size > 0 and freeze_marker.exists():
        return 0

    issues = check_unit_outputs(skill="transition-weaver", workspace=workspace, outputs=[out_rel])
    if not issues:
        return 0

    outline_rel = inputs[0]
    briefs_rel = inputs[1] if len(inputs) >= 2 else "outline/subsection_briefs.jsonl"
    outline = load_yaml(workspace / outline_rel) if (workspace / outline_rel).exists() else []
    briefs = _load_subsection_briefs(workspace / briefs_rel)

    atomic_write_text(out_path, _render_transitions(outline=outline, briefs=briefs))

    issues = check_unit_outputs(skill="transition-weaver", workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill="transition-weaver", issues=issues)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
