from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.common import copy_tree

    workspace = Path(args.workspace).resolve()
    template_dir = repo_root / ".codex" / "skills" / "workspace-init" / "assets" / "workspace-template"
    copy_tree(template_dir, workspace, overwrite=bool(args.overwrite))

    required = ["STATUS.md", "UNITS.csv", "CHECKPOINTS.md", "DECISIONS.md", "GOAL.md"]
    missing = [name for name in required if not (workspace / name).exists()]
    if missing:
        raise SystemExit(f"Missing required workspace files: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
