from __future__ import annotations

import argparse
import shutil
import subprocess
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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["latex/main.pdf", "output/LATEX_BUILD_REPORT.md"]

    pdf_rel = outputs[0]
    report_rel = outputs[1] if len(outputs) > 1 else "output/LATEX_BUILD_REPORT.md"
    pdf_path = workspace / pdf_rel
    report_path = workspace / report_rel

    tex_path = workspace / "latex" / "main.tex"
    if not tex_path.exists():
        _write_report(report_path, ok=False, message=f"Missing input: {tex_path}")
        return 0

    latexmk = shutil.which("latexmk")
    if not latexmk:
        _write_report(report_path, ok=False, message="latexmk not found in PATH")
        return 0

    ensure_dir(pdf_path.parent)
    ensure_dir(report_path.parent)

    cmd = [
        latexmk,
        "-xelatex",
        "-bibtex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        tex_path.name,
    ]
    proc = subprocess.run(cmd, cwd=str(tex_path.parent), capture_output=True, text=True)

    ok = proc.returncode == 0 and (tex_path.parent / "main.pdf").exists()
    if ok:
        # Ensure the expected output path exists (latexmk writes into latex/ by default).
        if pdf_path != tex_path.parent / "main.pdf":
            shutil.copy2(tex_path.parent / "main.pdf", pdf_path)
        _write_report(report_path, ok=True, message="SUCCESS", stdout=proc.stdout, stderr=proc.stderr)
        return 0

    _write_report(
        report_path,
        ok=False,
        message=f"latexmk failed (exit {proc.returncode})",
        stdout=proc.stdout,
        stderr=proc.stderr,
    )
    return 0


def _write_report(path: Path, *, ok: bool, message: str, stdout: str = "", stderr: str = "") -> None:
    from datetime import datetime
    from tooling.common import atomic_write_text

    def _tail(s: str, n: int = 120) -> str:
        lines = (s or "").splitlines()
        if len(lines) <= n:
            return "\n".join(lines)
        return "\n".join(lines[-n:])

    ts = datetime.now().replace(microsecond=0).isoformat()
    content = "\n".join(
        [
            "# LaTeX build report",
            "",
            f"- Timestamp: `{ts}`",
            "- Entry: `latex/main.tex`",
            "- Output: `latex/main.pdf`",
            "- Engine: `latexmk -xelatex -bibtex`",
            "",
            "## Result",
            "",
            f"- Status: {'SUCCESS' if ok else 'FAILED'}",
            f"- Message: {message}",
            "",
            "## Stdout (tail)",
            "",
            "```",
            _tail(stdout),
            "```",
            "",
            "## Stderr (tail)",
            "",
            "```",
            _tail(stderr),
            "```",
            "",
        ]
    ).rstrip() + "\n"

    atomic_write_text(path, content)


if __name__ == "__main__":
    raise SystemExit(main())
