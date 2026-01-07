from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--unit-id", default="")
    parser.add_argument("--inputs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--checkpoint", default="")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable quality-gate mode (block when outputs look like scaffolding stubs; writes output/QUALITY_GATE.md)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo_root))

    from tooling.executor import run_one_unit

    result = run_one_unit(workspace=Path(args.workspace).resolve(), repo_root=repo_root, strict=bool(args.strict))
    print(f"{result.status}: {result.unit_id or '-'} {result.message}")
    return 0 if result.status in {"DONE", "IDLE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
