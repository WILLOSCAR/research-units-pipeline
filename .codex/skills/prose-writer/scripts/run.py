from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


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
    outputs = parse_semicolon_list(args.outputs) or ["output/DRAFT.md"]
    out_path = workspace / outputs[0]

    outline_path = workspace / "outline" / "outline.yml"
    outline = load_yaml(outline_path) if outline_path.exists() else []

    # Optional enrichers to make the scaffold more actionable (still scaffold; LLM must write).
    mapping_path = workspace / "outline" / "mapping.tsv"
    notes_path = workspace / "papers" / "paper_notes.jsonl"
    mapped_by_section: dict[str, list[str]] = {}
    if mapping_path.exists():
        for row in read_tsv(mapping_path):
            sid = str(row.get("section_id") or "").strip()
            pid = str(row.get("paper_id") or "").strip()
            if sid and pid:
                mapped_by_section.setdefault(sid, []).append(pid)

    bibkey_by_pid: dict[str, str] = {}
    if notes_path.exists():
        for rec in read_jsonl(notes_path):
            if not isinstance(rec, dict):
                continue
            pid = str(rec.get("paper_id") or "").strip()
            bibkey = str(rec.get("bibkey") or "").strip()
            if pid and bibkey:
                bibkey_by_pid[pid] = bibkey

    goal = _read_goal(workspace)
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

    # Never overwrite an existing manually-refined draft, but do replace template placeholders.
    if out_path.exists() and out_path.stat().st_size > 0:
        existing = out_path.read_text(encoding="utf-8", errors="ignore")
        if not _is_placeholder_output(existing):
            return 0

    if out_path.name.upper() == "SNAPSHOT.MD":
        content = _render_snapshot_scaffold(goal=goal, outline=outline)
    else:
        content = _render_draft_scaffold(
            goal=goal,
            outline=outline,
            mapped_by_section=mapped_by_section,
            bibkey_by_pid=bibkey_by_pid,
        )

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


def _render_snapshot_scaffold(*, goal: str, outline: list) -> str:
    title = goal or "Snapshot"
    parts: list[str] = [f"# Snapshot: {title}", ""]
    parts.append("<!-- SCAFFOLD: snapshot (bullets-first) -->")
    parts.append("")
    parts.append("- Scope: TODO")
    parts.append("- Core set size: TODO")
    parts.append("- Key taxonomy: TODO")
    parts.append("- Key gaps: TODO")
    parts.append("")
    parts.append("## Outline (bullets)")
    parts.append("")
    parts.extend(_render_outline_bullets(outline))
    parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _render_draft_scaffold(
    *,
    goal: str,
    outline: list,
    mapped_by_section: dict[str, list[str]] | None = None,
    bibkey_by_pid: dict[str, str] | None = None,
) -> str:
    title = goal or "LLM Agent Survey"
    parts: list[str] = [f"# {title}", ""]
    parts.append("<!-- SCAFFOLD: prose-writer (LLM must replace TODOs with real prose + citations) -->")
    parts.append("")
    parts.append("## Abstract")
    parts.append("")
    parts.append("TODO: 用 150–250 字概括问题、方法/分类维度、覆盖范围（时间/数据源）、主要发现与开放问题。")
    parts.append("")
    parts.append("## Introduction")
    parts.append("")
    parts.append("TODO: 写 1–2 页引言，至少包含：")
    parts.append("- 背景与动机：为什么 LLM agents 在 2022–2025 成为主流研究方向？")
    parts.append("- 问题定义与范围：本文将“agent”限定为哪些能力/组件？不包括哪些方向？")
    parts.append("- 与相关 survey 的区别：已有 survey 覆盖什么，本综述补充什么？（用真实引用）")
    parts.append("- 贡献点（3–5 条）：taxonomy、对比维度、评测/安全、趋势与空白等")
    parts.append("- 文章结构：按节概述组织方式")
    parts.append("")
    parts.extend(_render_sections_scaffold(outline, mapped_by_section=mapped_by_section, bibkey_by_pid=bibkey_by_pid))
    parts.append("")
    if not _outline_has_heading(outline, {"timeline", "evolution", "chronology", "发展", "演化", "时间线"}):
        parts.append("## Timeline / Evolution")
        parts.append("")
        parts.append("TODO: 用年份串联关键转折点（例如 ReAct/Toolformer/Reflexion/AutoGPT/函数调用/agents benchmark 等），每个点至少 1–2 个引用。")
        parts.append("")
    parts.append("## Comparison Tables")
    parts.append("")
    parts.append("TODO: 至少补 1–2 张对比表（可先 Markdown 表格，后续会转 LaTeX）。")
    parts.append("")
    parts.append("| Work | Core loop / planner | Tools | Memory | Environment | Evaluation | Key takeaway |")
    parts.append("|---|---|---|---|---|---|---|")
    parts.append("| TODO | TODO | TODO | TODO | TODO | TODO | TODO |")
    parts.append("")
    parts.append("| Benchmark | Tasks | Interface | Metrics | Notes |")
    parts.append("|---|---|---|---|---|")
    parts.append("| TODO | TODO | TODO | TODO | TODO |")
    parts.append("")
    if not _outline_has_heading(outline, {"open problems", "future directions", "future work", "开放问题", "未来方向"}):
        parts.append("## Open Problems & Future Directions")
        parts.append("")
        parts.append("TODO: 给出具体、可执行的未来方向（标准化评测、可靠性、对齐/安全、可复现、系统工程等），避免每小节重复同一句模板。")
        parts.append("")
    if not _outline_has_heading(outline, {"conclusion", "结论"}):
        parts.append("## Conclusion")
        parts.append("")
        parts.append("TODO: 总结 taxonomy + 主要趋势 + 关键挑战（与引言呼应），并给出简短 takeaways。")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _render_sections_scaffold(
    outline: list,
    *,
    mapped_by_section: dict[str, list[str]] | None = None,
    bibkey_by_pid: dict[str, str] | None = None,
) -> list[str]:
    lines: list[str] = []
    for section in outline if isinstance(outline, list) else []:
        if not isinstance(section, dict):
            continue
        stitle = _strip_heading_prefix(str(section.get("title") or "").strip())
        if not stitle:
            continue
        # Avoid duplicating our own Introduction skeleton.
        if stitle.lower() in {"introduction"} or stitle in {"引言"}:
            continue
        lines.append(f"## {stitle}")
        lines.append("")
        bullets = section.get("bullets") or []
        bullets = [str(b).strip() for b in bullets if str(b).strip()] if isinstance(bullets, list) else []
        if bullets:
            lines.append("TODO: 本节写作要点：")
            for b in bullets[:6]:
                lines.append(f"- {b}")
            lines.append("")
        for sub in section.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            sub_title = _strip_heading_prefix(str(sub.get("title") or "").strip())
            if not sub_title:
                continue
            sub_id = str(sub.get("id") or "").strip()
            lines.append(f"### {sub_title}")
            lines.append("")
            axes = sub.get("bullets") or []
            axes = [str(a).strip() for a in axes if str(a).strip()] if isinstance(axes, list) else []
            lines.append("TODO: 写 2–3 段综合性讨论（不是逐篇复述），至少包含：")
            lines.append("- 关键脉络/分支：把方法按机制/假设/环境拆分成 2–4 条路线")
            lines.append("- 对比与取舍：明确 trade-off（可靠性/成本/安全/可扩展性/可控性）")
            lines.append("- 失败模式：典型 failure cases 与诱因（最好引用）")
            lines.append("- 小结：本小节 2–3 条 takeaways")
            lines.append("- 重要：至少写 1 段“同段多引用”的对比段落（>=2 篇工作在同一段里被比较），否则容易退化成摘要罗列。")
            lines.append("")
            if axes:
                lines.append("对比维度（来自已批准 outline）：")
                for a in axes[:8]:
                    lines.append(f"- {a}")
                lines.append("")

            # Provide concrete starting citations (still scaffold; LLM must integrate into prose).
            mapped_pids: list[str] = []
            if sub_id and mapped_by_section and isinstance(mapped_by_section.get(sub_id), list):
                for pid in mapped_by_section.get(sub_id, []):
                    if pid not in mapped_pids:
                        mapped_pids.append(pid)
                    if len(mapped_pids) >= 8:
                        break
            cite_keys: list[str] = []
            if bibkey_by_pid:
                for pid in mapped_pids:
                    key = str(bibkey_by_pid.get(pid) or "").strip()
                    if key and key not in cite_keys:
                        cite_keys.append(key)
                    if len(cite_keys) >= 8:
                        break

            if mapped_pids:
                lines.append(f"Mapped paper IDs: {', '.join(mapped_pids)}")
            if cite_keys:
                joined = "; @".join(cite_keys)
                lines.append(f"Starter citations (integrate into prose; do not leave as a raw list): [@{joined}]")
            else:
                lines.append("Starter citations (integrate into prose; do not leave as a raw list): TODO [@Key1; @Key2; ...]")
            lines.append("")
            lines.append("Open problems (subsection-specific): TODO")
            lines.append("")
    return lines


def _render_outline_bullets(outline: list) -> list[str]:
    lines: list[str] = []
    for section in outline if isinstance(outline, list) else []:
        if not isinstance(section, dict):
            continue
        sid = str(section.get("id") or "").strip()
        stitle = str(section.get("title") or "").strip()
        if not stitle:
            continue
        header = f"- {sid} {stitle}".strip()
        lines.append(header)
        for sub in section.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            sub_id = str(sub.get("id") or "").strip()
            sub_title = str(sub.get("title") or "").strip()
            if sub_title:
                lines.append(f"  - {sub_id} {sub_title}".strip())
    return lines


def _outline_has_heading(outline: list, needles: set[str]) -> bool:
    needles_low = {n.strip().lower() for n in needles if str(n).strip()}
    for section in outline if isinstance(outline, list) else []:
        if not isinstance(section, dict):
            continue
        stitle = str(section.get("title") or "").strip().lower()
        if any(n in stitle for n in needles_low):
            return True
        for sub in section.get("subsections") or []:
            if not isinstance(sub, dict):
                continue
            sub_title = str(sub.get("title") or "").strip().lower()
            if any(n in sub_title for n in needles_low):
                return True
    return False


def _strip_heading_prefix(text: str) -> str:
    # Avoid duplicated numbering like "1 Introduction" in downstream LaTeX.
    text = (text or "").strip()
    return re.sub(r"^\d+(?:\.\d+)*\s+", "", text)


def _is_placeholder_output(text: str) -> bool:
    text = (text or "").strip().lower()
    if not text:
        return True
    if "(placeholder)" in text:
        return True
    if "checkpoint policy reminder" in text:
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
