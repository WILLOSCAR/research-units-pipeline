from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


def _iter_outline_pairs(outline: Any) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    # Returns (within_h3_pairs, between_h2_pairs)
    h3_pairs: list[tuple[str, str]] = []
    h2_pairs: list[tuple[str, str]] = []

    if not isinstance(outline, list):
        return h3_pairs, h2_pairs

    section_titles: list[str] = []
    for sec in outline:
        if not isinstance(sec, dict):
            continue
        stitle = str(sec.get('title') or '').strip()
        subs = sec.get('subsections') or []
        if stitle:
            section_titles.append(stitle)
        if isinstance(subs, list) and len(subs) >= 2:
            ids = []
            for sub in subs:
                if not isinstance(sub, dict):
                    continue
                sid = str(sub.get('id') or '').strip()
                if sid:
                    ids.append(sid)
            for i in range(len(ids) - 1):
                h3_pairs.append((ids[i], ids[i + 1]))

    for i in range(len(section_titles) - 1):
        h2_pairs.append((section_titles[i], section_titles[i + 1]))

    return h3_pairs, h2_pairs


def _scaffold_text(*, outline: Any) -> str:
    h3_pairs, h2_pairs = _iter_outline_pairs(outline)

    lines: list[str] = [
        '# Transitions (fill; no new facts; no citations)',
        '',
        '- Guardrail: transitions add no new facts and introduce no new citations.',
        '- Write transitions as gap/hand-off sentences: what was established → what remains unclear → why the next subsection follows.',
        '',
        '## Within-section (H3 → next H3)',
    ]
    if h3_pairs:
        for a, b in h3_pairs:
            lines.append(f'- {a} → {b}: TODO')
    else:
        lines.append('- (none)')

    lines.extend(['', '## Between sections (H2 → next H2)', ''])
    if h2_pairs:
        for a, b in h2_pairs:
            lines.append(f'- {a} → {b}: TODO')
    else:
        lines.append('- (none)')

    lines.append('')
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import atomic_write_text, ensure_dir, load_yaml, parse_semicolon_list
    from tooling.quality_gate import check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or 'U098').strip() or 'U098'

    inputs = parse_semicolon_list(args.inputs) or ['outline/outline.yml', 'outline/subsection_briefs.jsonl']
    outputs = parse_semicolon_list(args.outputs) or ['outline/transitions.md']

    out_rel = outputs[0] if outputs else 'outline/transitions.md'
    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    freeze_marker = out_path.with_name('transitions.refined.ok')
    if out_path.exists() and out_path.stat().st_size > 0 and freeze_marker.exists():
        return 0

    issues = check_unit_outputs(skill='transition-weaver', workspace=workspace, outputs=[out_rel])
    if not issues:
        return 0

    # If missing/empty, write a scaffold (it intentionally contains TODO so the gate will block).
    if not out_path.exists() or out_path.stat().st_size == 0:
        outline_rel = inputs[0]
        outline = load_yaml(workspace / outline_rel) if (workspace / outline_rel).exists() else []
        atomic_write_text(out_path, _scaffold_text(outline=outline))

    # Re-check and block with a quality report.
    issues = check_unit_outputs(skill='transition-weaver', workspace=workspace, outputs=[out_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='transition-weaver', issues=issues)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
