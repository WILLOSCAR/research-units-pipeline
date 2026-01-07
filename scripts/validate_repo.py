from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINES_DIR = REPO_ROOT / "pipelines"
SKILLS_DIR = REPO_ROOT / ".codex" / "skills"

REQUIRED_UNITS_COLS = {
    "unit_id",
    "title",
    "type",
    "skill",
    "inputs",
    "outputs",
    "acceptance",
    "checkpoint",
    "status",
    "depends_on",
    "owner",
}


@dataclass(frozen=True)
class Finding:
    level: str  # ERROR|WARN|INFO
    message: str


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pipeline ↔ units template ↔ skills alignment.")
    parser.add_argument("--check-claude-symlink", action="store_true", help="Also check `.claude/skills` presence.")
    args = parser.parse_args()

    findings: list[Finding] = []
    pipeline_paths = sorted(PIPELINES_DIR.glob("*.pipeline.md"))
    if not pipeline_paths:
        findings.append(Finding("ERROR", f"No pipelines found under `{PIPELINES_DIR}`."))
        return _report(findings)

    for pipeline_path in pipeline_paths:
        findings.extend(_validate_pipeline(pipeline_path))

    if args.check_claude_symlink:
        findings.extend(_validate_claude_skills())

    return _report(findings)


def _validate_pipeline(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        fm, body = _split_frontmatter(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [Finding("ERROR", f"{path}: {exc}")]

    units_template = str(fm.get("units_template") or "").strip()
    if not units_template:
        findings.append(Finding("ERROR", f"{path}: missing `units_template` in YAML front matter."))
        return findings

    units_path = (REPO_ROOT / units_template).resolve()
    if not units_path.exists():
        findings.append(Finding("ERROR", f"{path}: units template not found: `{units_template}`."))
        return findings

    target_artifacts = fm.get("target_artifacts") or []
    if target_artifacts and not isinstance(target_artifacts, list):
        findings.append(Finding("WARN", f"{path}: `target_artifacts` should be a YAML list."))
        target_artifacts = []

    required_skills = _parse_required_skills(body)

    template_skills: set[str] = set()
    template_outputs: set[str] = set()
    missing_skill_dirs: set[str] = set()
    missing_skill_md: set[str] = set()
    skills_without_scripts: set[str] = set()

    try:
        with units_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            cols = set(reader.fieldnames or [])
            missing_cols = sorted(REQUIRED_UNITS_COLS - cols)
            if missing_cols:
                findings.append(
                    Finding("ERROR", f"{units_template}: missing required columns: {', '.join(missing_cols)}")
                )
                return findings

            for row in reader:
                skill = (row.get("skill") or "").strip()
                if not skill:
                    continue
                template_skills.add(skill)

                for out in _split_semicolon(row.get("outputs") or ""):
                    out = out.lstrip("?").strip()
                    if out:
                        template_outputs.add(out)

                skill_dir = SKILLS_DIR / skill
                if not skill_dir.exists():
                    missing_skill_dirs.add(skill)
                    continue

                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    missing_skill_md.add(skill)

                script = skill_dir / "scripts" / "run.py"
                if not script.exists():
                    skills_without_scripts.add(skill)
    except Exception as exc:
        findings.append(Finding("ERROR", f"Failed to read `{units_template}`: {exc}"))
        return findings

    for skill in sorted(missing_skill_dirs):
        findings.append(Finding("ERROR", f"{path.name}: `{units_template}` references missing skill dir: `{skill}`"))
    for skill in sorted(missing_skill_md):
        findings.append(Finding("ERROR", f"{path.name}: skill `{skill}` is missing `SKILL.md`"))

    missing_required = sorted(required_skills - template_skills)
    if missing_required:
        findings.append(
            Finding(
                "ERROR",
                f"{path.name}: pipeline `required_skills` missing from `{units_template}`: {', '.join(missing_required)}",
            )
        )

    if target_artifacts:
        missing_artifacts = sorted(set(map(str, target_artifacts)) - template_outputs)
        if missing_artifacts:
            findings.append(
                Finding(
                    "WARN",
                    f"{path.name}: `target_artifacts` not present in `{units_template}` outputs: {', '.join(missing_artifacts)}",
                )
            )

    if skills_without_scripts:
        findings.append(
            Finding(
                "INFO",
                f"{path.name}: skills without scripts (LLM-first expected): {', '.join(sorted(skills_without_scripts))}",
            )
        )

    return findings


def _validate_claude_skills() -> list[Finding]:
    skills_path = REPO_ROOT / ".claude" / "skills"
    if skills_path.exists():
        return [Finding("INFO", f"Claude Code skills path present: `{skills_path}`")]
    return [
        Finding(
            "WARN",
            "Claude Code skills path missing: `.claude/skills` (consider symlinking/copying `.codex/skills`).",
        )
    ]


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("pipeline file must start with YAML front matter (`---`).")
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("unterminated YAML front matter (missing closing `---`).")
    raw = "\n".join(lines[1:end_idx])
    fm = yaml.safe_load(raw) or {}
    if not isinstance(fm, dict):
        raise ValueError("pipeline YAML front matter must be a mapping.")
    body = "\n".join(lines[end_idx + 1 :])
    return fm, body


def _parse_required_skills(body: str) -> set[str]:
    skills: set[str] = set()
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() != "required_skills:":
            i += 1
            continue
        i += 1
        while i < len(lines):
            line = lines[i].rstrip()
            if not line.strip():
                break
            m = re.match(r"^\s*-\s*(\S+)\s*$", line)
            if not m:
                break
            skills.add(m.group(1))
            i += 1
        continue
    return skills


def _split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def _report(findings: list[Finding]) -> int:
    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]
    infos = [f for f in findings if f.level == "INFO"]

    for f in errors + warns + infos:
        prefix = {"ERROR": "ERROR", "WARN": "WARN", "INFO": "INFO"}.get(f.level, f.level)
        print(f"{prefix}: {f.message}")

    print("")
    print(f"Summary: {len(errors)} error(s), {len(warns)} warning(s), {len(infos)} info.")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())

