from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tooling.common import atomic_write_text, copy_tree, today_iso
from tooling.executor import run_one_unit
from tooling.pipeline_spec import PipelineSpec


def main() -> int:
    parser = argparse.ArgumentParser(prog="pipeline.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    init_p = sub.add_parser("init", help="Initialize a workspace from template + pipeline units template")
    init_p.add_argument("--workspace", required=True, help="Workspace directory")
    init_p.add_argument("--pipeline", required=True, help="Pipeline name or path (e.g., arxiv-survey)")
    init_p.add_argument("--overwrite", action="store_true", help="Overwrite existing workspace files")
    init_p.add_argument("--overwrite-units", action="store_true", help="Overwrite workspace UNITS.csv")

    kickoff_p = sub.add_parser("kickoff", help="Kick off a pipeline run from a topic (init workspace + draft decisions)")
    kickoff_p.add_argument("--topic", required=True, help="Topic/goal (used to create workspace and seed queries)")
    kickoff_p.add_argument("--pipeline", default="", help="Pipeline name or path (default: auto-pick from topic)")
    kickoff_p.add_argument("--workspace", default="", help="Workspace directory (default: ./workspaces/<slug>/)")
    kickoff_p.add_argument("--overwrite", action="store_true", help="Overwrite existing workspace files")
    kickoff_p.add_argument("--overwrite-units", action="store_true", help="Overwrite workspace UNITS.csv")
    kickoff_p.add_argument("--run", action="store_true", help="After kickoff, run units until blocked/complete")
    kickoff_p.add_argument("--max-steps", type=int, default=999, help="Maximum units to attempt when using --run")
    kickoff_p.add_argument(
        "--strict",
        action="store_true",
        help="Enable quality-gate mode (block when outputs look like scaffolding stubs; writes output/QUALITY_GATE.md)",
    )
    kickoff_p.add_argument(
        "--auto-approve",
        action="append",
        default=[],
        help="Auto-tick approvals in DECISIONS.md (repeatable, e.g., --auto-approve C2).",
    )

    run_one_p = sub.add_parser("run-one", help="Execute exactly one runnable unit from UNITS.csv")
    run_one_p.add_argument("--workspace", required=True, help="Workspace directory")
    run_one_p.add_argument("--strict", action="store_true", help="Enable quality-gate mode (see kickoff --strict)")
    run_one_p.add_argument(
        "--auto-approve",
        action="append",
        default=[],
        help="Auto-tick approvals in DECISIONS.md (repeatable, e.g., --auto-approve C2).",
    )

    run_p = sub.add_parser("run", help="Run units until blocked or complete")
    run_p.add_argument("--workspace", required=True, help="Workspace directory")
    run_p.add_argument("--max-steps", type=int, default=999, help="Maximum units to attempt")
    run_p.add_argument("--strict", action="store_true", help="Enable quality-gate mode (see kickoff --strict)")
    run_p.add_argument(
        "--auto-approve",
        action="append",
        default=[],
        help="Auto-tick approvals in DECISIONS.md (repeatable, e.g., --auto-approve C2).",
    )

    approve_p = sub.add_parser("approve", help="Tick an approval checkbox in DECISIONS.md (e.g., Approve C2)")
    approve_p.add_argument("--workspace", required=True, help="Workspace directory")
    approve_p.add_argument("--checkpoint", required=True, help="Checkpoint ID (e.g., C2)")

    mark_p = sub.add_parser("mark", help="Manually set a unit status in UNITS.csv (e.g., after LLM work)")
    mark_p.add_argument("--workspace", required=True, help="Workspace directory")
    mark_p.add_argument("--unit-id", required=True, help="Unit ID (e.g., U030)")
    mark_p.add_argument("--status", required=True, help="New status (TODO|DOING|DONE|BLOCKED|SKIP)")
    mark_p.add_argument("--note", default="", help="Optional note to append to STATUS.md run log")

    args = parser.parse_args()

    repo_root = REPO_ROOT

    if args.cmd == "init":
        workspace = Path(args.workspace).resolve()
        _ensure_not_repo_root(workspace, repo_root)
        pipeline_path = _resolve_pipeline_path(repo_root, args.pipeline)
        spec = PipelineSpec.load(pipeline_path)

        template_dir = repo_root / ".codex" / "skills" / "workspace-init" / "assets" / "workspace-template"
        copy_tree(template_dir, workspace, overwrite=bool(args.overwrite))

        lock_text = (
            f"pipeline: {spec.path.relative_to(repo_root)}\n"
            f"units_template: {spec.units_template}\n"
            f"locked_at: {today_iso()}\n"
        )
        atomic_write_text(workspace / "PIPELINE.lock.md", lock_text)

        units_src = repo_root / spec.units_template
        units_dst = workspace / "UNITS.csv"
        if units_dst.exists() and not args.overwrite_units:
            # The workspace template ships with a stub UNITS.csv (U001 only). Treat it as safe to overwrite.
            template_units = (template_dir / "UNITS.csv").read_text(encoding="utf-8", errors="ignore").strip()
            existing_units = units_dst.read_text(encoding="utf-8", errors="ignore").strip()
            if existing_units != template_units:
                raise SystemExit(f"UNITS.csv already exists at {units_dst} (use --overwrite-units)")
        atomic_write_text(units_dst, units_src.read_text(encoding="utf-8"))

        first_checkpoint = spec.default_checkpoints[0] if spec.default_checkpoints else "C0"
        _update_status(
            workspace / "STATUS.md",
            spec_path=str(spec.path.relative_to(repo_root)),
            checkpoint=first_checkpoint,
        )
        return 0

    if args.cmd == "kickoff":
        topic = str(args.topic).strip()
        if not topic:
            raise SystemExit("--topic must be non-empty")

        pipeline_name = str(args.pipeline).strip() or _auto_pick_pipeline(topic)
        workspace = (
            Path(args.workspace).resolve()
            if str(args.workspace).strip()
            else (repo_root / "workspaces" / _slugify(topic)).resolve()
        )
        _ensure_not_repo_root(workspace, repo_root)

        pipeline_path = _resolve_pipeline_path(repo_root, pipeline_name)
        spec = PipelineSpec.load(pipeline_path)

        template_dir = repo_root / ".codex" / "skills" / "workspace-init" / "assets" / "workspace-template"
        copy_tree(template_dir, workspace, overwrite=bool(args.overwrite))

        atomic_write_text(workspace / "GOAL.md", f"# Goal\n\n{topic}\n")

        lock_text = (
            f"pipeline: {spec.path.relative_to(repo_root)}\n"
            f"units_template: {spec.units_template}\n"
            f"locked_at: {today_iso()}\n"
        )
        atomic_write_text(workspace / "PIPELINE.lock.md", lock_text)

        units_src = repo_root / spec.units_template
        units_dst = workspace / "UNITS.csv"
        if units_dst.exists() and not args.overwrite_units:
            # The workspace template ships with a stub UNITS.csv (U001 only). Treat it as safe to overwrite.
            template_units = (template_dir / "UNITS.csv").read_text(encoding="utf-8", errors="ignore").strip()
            existing_units = units_dst.read_text(encoding="utf-8", errors="ignore").strip()
            if existing_units != template_units:
                raise SystemExit(f"UNITS.csv already exists at {units_dst} (use --overwrite-units)")
        atomic_write_text(units_dst, units_src.read_text(encoding="utf-8"))

        first_checkpoint = spec.default_checkpoints[0] if spec.default_checkpoints else "C0"
        _update_status(
            workspace / "STATUS.md",
            spec_path=str(spec.path.relative_to(repo_root)),
            checkpoint=first_checkpoint,
        )

        router_script = repo_root / ".codex" / "skills" / "pipeline-router" / "scripts" / "run.py"
        if router_script.exists():
            subprocess.run(
                [
                    sys.executable,
                    str(router_script),
                    "--workspace",
                    str(workspace),
                    "--checkpoint",
                    "C0",
                ],
                check=False,
            )

        print(f"Workspace ready: {workspace}")
        if args.run:
            for _ in range(int(args.max_steps)):
                result = run_one_unit(
                    workspace=workspace,
                    repo_root=repo_root,
                    strict=bool(args.strict),
                    auto_approve=set(args.auto_approve or []),
                )
                print(f"{result.status}: {result.unit_id or '-'} {result.message}")
                if result.status != "DONE":
                    break
            return 0

        print("Next: run `python scripts/pipeline.py run --workspace <ws>` (it will pause if a HUMAN approval is required)")
        return 0

    if args.cmd == "run-one":
        workspace = Path(args.workspace).resolve()
        result = run_one_unit(
            workspace=workspace,
            repo_root=repo_root,
            strict=bool(args.strict),
            auto_approve=set(args.auto_approve or []),
        )
        print(f"{result.status}: {result.unit_id or '-'} {result.message}")
        return 0 if result.status in {"DONE", "IDLE"} else 2

    if args.cmd == "run":
        workspace = Path(args.workspace).resolve()
        for _ in range(int(args.max_steps)):
            result = run_one_unit(
                workspace=workspace,
                repo_root=repo_root,
                strict=bool(args.strict),
                auto_approve=set(args.auto_approve or []),
            )
            print(f"{result.status}: {result.unit_id or '-'} {result.message}")
            if result.status != "DONE":
                break
        return 0

    if args.cmd == "approve":
        workspace = Path(args.workspace).resolve()
        checkpoint = str(args.checkpoint).strip()
        if not checkpoint:
            raise SystemExit("--checkpoint must be non-empty")

        from tooling.common import set_decisions_approval

        set_decisions_approval(workspace / "DECISIONS.md", checkpoint, approved=True)
        print(f"Approved {checkpoint} in {workspace / 'DECISIONS.md'}")
        return 0

    if args.cmd == "mark":
        workspace = Path(args.workspace).resolve()
        unit_id = str(args.unit_id).strip()
        status = str(args.status).strip().upper()
        note = str(args.note).strip()
        if not unit_id:
            raise SystemExit("--unit-id must be non-empty")
        if status not in {"TODO", "DOING", "DONE", "BLOCKED", "SKIP"}:
            raise SystemExit("--status must be one of TODO|DOING|DONE|BLOCKED|SKIP")

        from tooling.common import UnitsTable, now_iso_seconds, update_status_log
        from tooling.executor import _refresh_status_checkpoint  # type: ignore

        units_path = workspace / "UNITS.csv"
        if not units_path.exists():
            raise SystemExit(f"Missing {units_path}")
        table = UnitsTable.load(units_path)
        found = False
        for row in table.rows:
            if str(row.get("unit_id") or "").strip() == unit_id:
                row["status"] = status
                found = True
                break
        if not found:
            raise SystemExit(f"Unit not found: {unit_id}")
        table.save(units_path)
        if note:
            update_status_log(workspace / "STATUS.md", f"{now_iso_seconds()} {unit_id} NOTE {note}")
        _refresh_status_checkpoint(workspace / "STATUS.md", table)
        print(f"Marked {unit_id} as {status} in {units_path}")
        return 0

    raise SystemExit("unreachable")


def _resolve_pipeline_path(repo_root: Path, pipeline: str) -> Path:
    candidate = Path(pipeline)
    if candidate.exists():
        return candidate.resolve()
    name = pipeline
    if name.endswith(".pipeline.md"):
        filename = name
    else:
        filename = f"{name}.pipeline.md"
    path = repo_root / "pipelines" / filename
    if not path.exists():
        raise SystemExit(f"Pipeline not found: {path}")
    return path


def _ensure_not_repo_root(workspace: Path, repo_root: Path) -> None:
    if workspace.resolve() == repo_root.resolve():
        raise SystemExit("Refusing to use repo root as workspace. Use --workspace ./workspaces/<name>/")


def _slugify(text: str) -> str:
    out: list[str] = []
    prev_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
            continue
        if not prev_dash:
            out.append("-")
            prev_dash = True
    slug = "".join(out).strip("-")
    return slug[:64] or "run"


def _auto_pick_pipeline(topic: str) -> str:
    t = topic.lower()
    if "systematic" in t or "prisma" in t or "系统综述" in topic:
        return "systematic-review"
    if "tutorial" in t or "教程" in topic:
        return "tutorial"
    if "peer review" in t or "审稿" in topic or "review report" in t:
        return "peer-review"
    if "snapshot" in t or "快照" in topic:
        return "lit-snapshot"
    if "latex" in t or "pdf" in t or "paper" in t or ("论文" in topic) or ("可编译" in topic) or ("编译" in topic):
        return "arxiv-survey-latex"
    return "arxiv-survey"


def _update_status(status_path: Path, *, spec_path: str, checkpoint: str) -> None:
    if status_path.exists():
        lines = status_path.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["# Status"]

    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.strip() == "## Current pipeline":
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("-"):
                out.append(f"- `{spec_path}`")
                i += 2
                continue
            out.append(f"- `{spec_path}`")
        if line.strip() == "## Current checkpoint":
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("-"):
                out.append(f"- `{checkpoint}`")
                i += 2
                continue
            out.append(f"- `{checkpoint}`")
        i += 1

    if "## Current pipeline" not in "\n".join(lines):
        out.extend(["", "## Current pipeline", f"- `{spec_path}`"])
    if "## Current checkpoint" not in "\n".join(lines):
        out.extend(["", "## Current checkpoint", f"- `{checkpoint}`"])

    atomic_write_text(status_path, "\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
