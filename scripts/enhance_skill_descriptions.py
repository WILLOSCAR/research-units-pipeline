from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".codex" / "skills"


REQUIRED_LINES = [
    "**Trigger**:",
    "**Use when**:",
    "**Skip if**:",
    "**Network**:",
    "**Guardrail**:",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-add missing description template lines to SKILL.md front matter.")
    parser.add_argument("--apply", action="store_true", help="Write changes back to SKILL.md (default: dry-run).")
    args = parser.parse_args()

    skill_paths = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_paths:
        raise SystemExit(f"No skills found under {SKILLS_DIR}")

    changed = 0
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        fm, body = _split_frontmatter(text)
        if not isinstance(fm, dict):
            continue

        desc = str(fm.get("description") or "").rstrip()
        updated = _ensure_description_lines(desc, skill_key=path.parent.name, body=body)
        if updated == desc:
            continue

        fm["description"] = updated + "\n"
        new_text = _render_frontmatter(fm) + body.lstrip("\n")
        changed += 1

        if args.apply:
            path.write_text(new_text.rstrip() + "\n", encoding="utf-8")
        else:
            print(f"[DRY] Would update: {path}")

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"{mode}: {changed} file(s) would be updated.")
    return 0


def _ensure_description_lines(desc: str, *, skill_key: str, body: str) -> str:
    if not desc.strip():
        desc = f"{skill_key}.\n"

    lines = desc.splitlines()
    if not lines:
        lines = [f"{skill_key}."]

    present = "\n".join(lines)
    missing = [m for m in REQUIRED_LINES if m not in present]
    if not missing:
        return desc.rstrip()

    # Suggest basic triggers from skill key + mentioned paths.
    suggested = _suggest_triggers(skill_key=skill_key, body=body)
    out: list[str] = [lines[0].rstrip(".") + "."]

    if "**Trigger**:" not in present:
        out.append(f"**Trigger**: {', '.join(suggested)}.")

    for marker in ["**Use when**:", "**Skip if**:", "**Network**:", "**Guardrail**:"]:
        if marker in present:
            continue
        out.append(f"{marker} <fill>.")

    # Keep any remaining original lines (best-effort).
    for ln in lines[1:]:
        if ln.strip():
            out.append(ln)
    return "\n".join(out).rstrip()


def _suggest_triggers(*, skill_key: str, body: str) -> list[str]:
    tokens: list[str] = []
    tokens.extend([skill_key, skill_key.replace("-", " ")])
    for m in re.findall(r"`([^`]+)`", body or ""):
        m = m.strip()
        if "/" in m:
            tokens.append(Path(m).name)
    dedup: list[str] = []
    seen = set()
    for t in tokens:
        t = re.sub(r"\\s+", " ", str(t or "").strip())
        if not t:
            continue
        if t.lower() in seen:
            continue
        seen.add(t.lower())
        dedup.append(t)
    return dedup[:10] or [skill_key]


def _split_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML front matter (`---`).")
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("Unterminated YAML front matter (missing closing `---`).")
    raw = "\n".join(lines[1:end_idx])
    fm = yaml.safe_load(raw) or {}
    body = "\n".join(lines[end_idx + 1 :])
    return fm, body


def _render_frontmatter(fm: dict) -> str:
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).rstrip()
    return f"---\n{dumped}\n---\n\n"


if __name__ == "__main__":
    raise SystemExit(main())

