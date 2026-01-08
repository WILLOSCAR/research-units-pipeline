from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".codex" / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new skill skeleton under .codex/skills/<name>/")
    parser.add_argument("--name", required=True, help="Skill folder name (kebab-case recommended).")
    parser.add_argument("--category", default="", help="Optional category label (for humans).")
    parser.add_argument(
        "--inputs",
        default="",
        help="Comma/semicolon-separated input artifact paths (e.g., papers/core_set.csv; outline/mapping.tsv).",
    )
    parser.add_argument(
        "--outputs",
        default="",
        help="Comma/semicolon-separated output artifact paths (e.g., outline/taxonomy.yml; output/REPORT.md).",
    )
    parser.add_argument("--with-script", action="store_true", help="Also create scripts/run.py template.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing SKILL.md/run.py if present.")
    args = parser.parse_args()

    name = _slug(args.name)
    if not name:
        raise SystemExit("Invalid --name (expected non-empty, kebab-case-ish).")

    inputs = _split_list(args.inputs)
    outputs = _split_list(args.outputs)

    skill_dir = SKILLS_DIR / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {skill_md} (use --overwrite).")

    skill_md.write_text(
        _render_skill_md(
            name=name,
            category=str(args.category or "").strip(),
            inputs=inputs,
            outputs=outputs,
            with_script=bool(args.with_script),
        ),
        encoding="utf-8",
    )

    if args.with_script:
        run_py = skill_dir / "scripts" / "run.py"
        run_py.parent.mkdir(parents=True, exist_ok=True)
        if run_py.exists() and not args.overwrite:
            raise SystemExit(f"Refusing to overwrite existing file: {run_py} (use --overwrite).")
        run_py.write_text(_render_run_py(skill=name, default_inputs=inputs, default_outputs=outputs), encoding="utf-8")

    print(f"Created skill skeleton: {skill_md}")
    if args.with_script:
        print(f"Created script template: {skill_dir / 'scripts' / 'run.py'}")
    print("Next: fill in the workflow/checklists and add to templates/UNITS.*.csv if used by a pipeline.")
    return 0


def _slug(value: str) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"[^a-z0-9\\-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def _split_list(value: str) -> list[str]:
    raw = str(value or "").strip()
    if not raw:
        return []
    parts = re.split(r"[;,]\\s*", raw)
    return [p.strip() for p in parts if p.strip()]


def _title(name: str) -> str:
    return " ".join([w.capitalize() for w in re.split(r"[-_]+", name) if w])


def _render_skill_md(*, name: str, category: str, inputs: list[str], outputs: list[str], with_script: bool) -> str:
    title = _title(name)
    cat_block = f"- Category: `{category}`\n\n" if category else ""

    inputs_lines = "\n".join([f"- `{p}`" for p in inputs]) if inputs else "- (none)"
    outputs_lines = "\n".join([f"- `{p}`" for p in outputs]) if outputs else "- (none)"

    script_block = ""
    if with_script:
        script_block = f"""

## Script

### Quick Start

- `python .codex/skills/{name}/scripts/run.py --help`
- `python .codex/skills/{name}/scripts/run.py --workspace <workspace_dir>`

### All Options

- `--workspace <dir>`: workspace directory
- `--inputs <a;b;...>`: override inputs (semicolon-separated)
- `--outputs <a;b;...>`: override outputs (semicolon-separated)
- `--unit-id <id>` / `--checkpoint <C*>`: optional runner metadata

### Examples

- Basic:
  - `python .codex/skills/{name}/scripts/run.py --workspace <ws>`
"""

    return (
        f"---\n"
        f"name: {name}\n"
        f"description: |\n"
        f"  <one-line summary>.\n"
        f"  **Trigger**: <keywords (EN/中文), comma-separated>.\n"
        f"  **Use when**: <when this skill is the right next step>.\n"
        f"  **Skip if**: <when not to use>.\n"
        f"  **Network**: <none|required|optional + offline fallback>.\n"
        f"  **Guardrail**: <NO PROSE / checkpoints / invariants>.\n"
        f"---\n\n"
        f"# {title}\n\n"
        f"{cat_block}"
        f"## Inputs\n\n"
        f"{inputs_lines}\n\n"
        f"## Outputs\n\n"
        f"{outputs_lines}\n\n"
        f"## Workflow (heuristic)\n\n"
        f"1. <Step 1>\n"
        f"2. <Step 2>\n"
        f"3. <Step 3>\n\n"
        f"## Quality checklist\n\n"
        f"- [ ] Outputs exist and match the unit contract.\n"
        f"- [ ] No placeholders/template text remain.\n"
        f"- [ ] Any required human checkpoint is respected.\n"
        f"{script_block}\n"
        f"## Troubleshooting\n\n"
        f"### Common Issues\n\n"
        f"#### Issue: <short description>\n\n"
        f"**Symptom**:\n"
        f"- <what you observe>\n\n"
        f"**Causes**:\n"
        f"- <likely causes>\n\n"
        f"**Solutions**:\n"
        f"- <how to fix>\n\n"
        f"### Recovery Checklist\n\n"
        f"- [ ] Re-check inputs/outputs paths.\n"
        f"- [ ] Re-run the step deterministically (script) if available.\n"
        f"- [ ] If blocked, record questions in `DECISIONS.md` and wait for approval.\n"
    ).rstrip() + "\n"


def _render_run_py(*, skill: str, default_inputs: list[str], default_outputs: list[str]) -> str:
    def _list_literal(values: list[str]) -> str:
        if not values:
            return "[]"
        inner = ", ".join([repr(v) for v in values])
        return f"[{inner}]"

    default_inputs_lit = _list_literal(default_inputs)
    default_outputs_lit = _list_literal(default_outputs)

    return (
        "from __future__ import annotations\n\n"
        "import argparse\n"
        "import sys\n"
        "from pathlib import Path\n\n\n"
        "def main() -> int:\n"
        "    parser = argparse.ArgumentParser()\n"
        "    parser.add_argument('--workspace', required=True)\n"
        "    parser.add_argument('--unit-id', default='')\n"
        "    parser.add_argument('--inputs', default='')\n"
        "    parser.add_argument('--outputs', default='')\n"
        "    parser.add_argument('--checkpoint', default='')\n"
        "    args = parser.parse_args()\n\n"
        "    repo_root = Path(__file__).resolve().parents[4]\n"
        "    sys.path.insert(0, str(repo_root))\n\n"
        "    from tooling.common import ensure_dir, parse_semicolon_list\n\n"
        "    workspace = Path(args.workspace).resolve()\n"
        f"    inputs = parse_semicolon_list(args.inputs) or {default_inputs_lit}\n"
        f"    outputs = parse_semicolon_list(args.outputs) or {default_outputs_lit}\n\n"
        "    # Deterministic scaffolding placeholder:\n"
        "    # - Create output parent directories.\n"
        "    # - Do not write semantic content here; keep this script a helper.\n"
        "    for out in outputs:\n"
        "        out_path = workspace / out\n"
        "        ensure_dir(out_path.parent)\n"
        "        if not out_path.exists():\n"
        "            out_path.write_text('', encoding='utf-8')\n\n"
        "    return 0\n\n\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
