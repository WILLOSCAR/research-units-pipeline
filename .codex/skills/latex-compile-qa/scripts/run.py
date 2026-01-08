from __future__ import annotations

import argparse
import re
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

    from tooling.common import ensure_dir, parse_semicolon_list

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

    built_pdf = tex_path.parent / "main.pdf"
    ok = proc.returncode == 0 and built_pdf.exists()

    if ok and pdf_path != built_pdf:
        shutil.copy2(built_pdf, pdf_path)

    page_count = _pdf_page_count(pdf_path if pdf_path.exists() else built_pdf)
    warnings = _collect_warnings(tex_dir=tex_path.parent, stdout=proc.stdout, stderr=proc.stderr)

    if ok:
        _write_report(
            report_path,
            ok=True,
            message="SUCCESS",
            stdout=proc.stdout,
            stderr=proc.stderr,
            page_count=page_count,
            warnings=warnings,
        )
        return 0

    _write_report(
        report_path,
        ok=False,
        message=f"latexmk failed (exit {proc.returncode})",
        stdout=proc.stdout,
        stderr=proc.stderr,
        page_count=page_count,
        warnings=warnings,
    )
    return 0


def _pdf_page_count(path: Path) -> int | None:
    if not path or not path.exists():
        return None
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(path)
        n = int(len(doc))
        doc.close()
        return n
    except Exception:
        return None


def _collect_warnings(*, tex_dir: Path, stdout: str, stderr: str) -> dict[str, int]:
    # Prefer the final LaTeX log; latexmk stdout/stderr can include warnings from
    # intermediate runs (e.g., before bibtex is applied), which would create
    # false positives for resolved citations.

    log_path = tex_dir / "main.log"
    log_text = log_path.read_text(encoding="utf-8", errors="ignore") if log_path.exists() else ""
    aux_text = "\n".join([stdout or "", stderr or ""]).strip()

    text = log_text if log_text.strip() else aux_text

    patterns: list[tuple[str, str]] = [
        ("citation_undefined", r"(?im)^Package\s+natbib\s+Warning: Citation.+undefined"),
        ("citation_undefined", r"(?im)There were undefined citations"),
        ("reference_undefined", r"(?im)there were undefined references"),
        ("overfull_hbox", r"(?im)^Overfull \\hbox"),
        ("underfull_hbox", r"(?im)^Underfull \\hbox"),
        ("rerun_references", r"(?im)Rerun to get cross-references right"),
    ]

    counts: dict[str, int] = {}
    for name, pat in patterns:
        counts[name] = counts.get(name, 0) + len(re.findall(pat, text))

    latex_warns = 0
    for ln in text.splitlines():
        if "LaTeX Warning:" in ln and "hbox" not in ln.lower():
            latex_warns += 1
    if latex_warns:
        counts["latex_warnings"] = latex_warns

    return {k: v for k, v in counts.items() if v}



def _write_report(
    path: Path,
    *,
    ok: bool,
    message: str,
    stdout: str = "",
    stderr: str = "",
    page_count: int | None = None,
    warnings: dict[str, int] | None = None,
) -> None:
    from datetime import datetime

    from tooling.common import atomic_write_text

    def _tail(s: str, n: int = 120) -> str:
        lines = (s or "").splitlines()
        if len(lines) <= n:
            return "\n".join(lines)
        return "\n".join(lines[-n:])

    ts = datetime.now().replace(microsecond=0).isoformat()
    warn = warnings or {}

    header_lines = [
        "# LaTeX build report",
        "",
        f"- Timestamp: `{ts}`",
        "- Entry: `latex/main.tex`",
        "- Output: `latex/main.pdf`",
        "- Engine: `latexmk -xelatex -bibtex`",
    ]
    if page_count is not None:
        header_lines.append(f"- Page count: `{page_count}`")

    content_lines: list[str] = []
    content_lines.extend(header_lines)
    content_lines.extend(
        [
            "",
            "## Result",
            "",
            f"- Status: {'SUCCESS' if ok else 'FAILED'}",
            f"- Message: {message}",
            "",
        ]
    )

    if warn:
        content_lines.extend(["## Warning summary", ""])
        for k in sorted(warn):
            content_lines.append(f"- {k}: {warn[k]}")
        content_lines.append("")

    content_lines.extend(
        [
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
    )

    atomic_write_text(path, "\n".join(content_lines).rstrip() + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
