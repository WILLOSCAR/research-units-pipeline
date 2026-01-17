from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Counts:
    causal: int
    contrast: int
    extension: int
    implication: int


def _draft_profile(workspace: Path) -> str:
    path = workspace / "queries.md"
    if not path.exists():
        return "survey"
    keys = {"draft_profile", "writing_profile", "quality_profile"}
    try:
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line.startswith("- ") or ":" not in line:
                continue
            key, value = line[2:].split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            if key not in keys:
                continue
            value = value.split("#", 1)[0].strip().strip('"').strip("'").strip().lower()
            if value in {"lite", "survey", "deep"}:
                return value
            return "survey"
    except Exception:
        return "survey"
    return "survey"


def _h3_files(workspace: Path) -> list[Path]:
    sec_dir = workspace / "sections"
    if not sec_dir.exists():
        return []
    out: list[Path] = []
    for p in sorted(sec_dir.glob("S*.md")):
        name = p.name
        if name in {"abstract.md", "discussion.md", "conclusion.md"}:
            continue
        if name.endswith("_lead.md"):
            continue
        # H3 IDs are rendered as S<sec>_<sub>.md (underscore).
        if "_" not in name:
            continue
        out.append(p)
    return out


def _first_paragraph(text: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\s*\n", (text or "").strip()) if p.strip()]
    return paras[0] if paras else ""


def _has_thesis(paragraph: str) -> bool:
    if not paragraph:
        return False
    p = re.sub(r"\[@[^\]]+\]", "", paragraph)
    p = re.sub(r"\s+", " ", p).strip()
    if not p:
        return False

    thesis_patterns = [
        r"(?i)\bthis\s+subsection\s+(?:argues|shows|surveys|suggests|demonstrates|contends)\s+that\b",
        r"(?i)\bin\s+this\s+subsection,\s*(?:we\s+)?(?:argue|show|survey|suggest)\s+that\b",
        r"(?i)\bwe\s+(?:argue|show|suggest)\s+that\b",
        r"(?:本小节|本节)(?:认为|指出|主张|讨论|表明)",
    ]
    return any(re.search(pat, p) for pat in thesis_patterns)


def _connector_counts(text: str) -> Counts:
    blob = re.sub(r"\[@[^\]]+\]", "", text or "")
    blob = blob.lower()

    causal = r"\b(therefore|thus|hence|as a result|consequently|accordingly)\b|因此|所以|从而|因而|由此"
    contrast = r"\b(however|nevertheless|nonetheless|yet|whereas|unlike|in contrast|by contrast)\b|然而|相比之下|相较|不同于"
    extension = r"\b(moreover|furthermore|additionally|in addition|similarly|likewise|building on|following)\b|此外|并且|同时|进一步|另外"
    implication = r"\b(this raises|this suggests|this implies|this motivates|this highlights)\b|这(?:提示|表明|意味着|引出)"

    return Counts(
        causal=len(re.findall(causal, blob)),
        contrast=len(re.findall(contrast, blob)),
        extension=len(re.findall(extension, blob)),
        implication=len(re.findall(implication, blob)),
    )


def _thresholds(profile: str) -> Counts:
    profile = (profile or "").strip().lower()
    if profile == "deep":
        return Counts(causal=3, contrast=2, extension=2, implication=1)
    if profile == "lite":
        return Counts(causal=1, contrast=1, extension=1, implication=0)
    return Counts(causal=2, contrast=2, extension=2, implication=1)


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

    from tooling.common import ensure_dir, now_iso_seconds, parse_semicolon_list

    workspace = Path(args.workspace).resolve()
    outputs = parse_semicolon_list(args.outputs) or ["output/SECTION_LOGIC_REPORT.md"]
    out_rel = outputs[0] if outputs else "output/SECTION_LOGIC_REPORT.md"
    out_path = workspace / out_rel
    ensure_dir(out_path.parent)

    prof = _draft_profile(workspace)
    thresh = _thresholds(prof)

    rows: list[tuple[str, bool, Counts, bool]] = []
    for p in _h3_files(workspace):
        text = p.read_text(encoding="utf-8", errors="ignore")
        thesis_ok = _has_thesis(_first_paragraph(text))
        counts = _connector_counts(text)
        connectors_ok = (
            counts.causal >= thresh.causal
            and counts.contrast >= thresh.contrast
            and counts.extension >= thresh.extension
            and counts.implication >= thresh.implication
        )
        ok = thesis_ok and connectors_ok
        rows.append((p.relative_to(workspace).as_posix(), thesis_ok, counts, ok))

    fail = [r for r in rows if not r[3]]
    status = "PASS" if (rows and not fail) else "FAIL"

    lines: list[str] = [
        "# Section Logic Report",
        "",
        f"- Generated at: {now_iso_seconds()}",
        f"- Draft profile: `{prof}`",
        f"- Status: {status}",
        "",
        "## Thresholds",
        "",
        "| Type | Min |",
        "|---|---:|",
        f"| causal | {thresh.causal} |",
        f"| contrast | {thresh.contrast} |",
        f"| extension | {thresh.extension} |",
        f"| implication | {thresh.implication} |",
        "",
        "## Per-section (H3)",
        "",
        "| File | Thesis | causal | contrast | extension | implication | Status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for rel, thesis_ok, c, ok in rows:
        lines.append(
            f"| `{rel}` | {'Y' if thesis_ok else 'N'} | {c.causal} | {c.contrast} | {c.extension} | {c.implication} | {'PASS' if ok else 'FAIL'} |"
        )

    if not rows:
        lines.extend(["", "- No H3 section files found under `sections/` (expected `S<sec>_<sub>.md`)."])

    if fail:
        lines.extend(
            [
                "",
                "## How to fix (LLM-first)",
                "",
                "- Add a thesis sentence to the end of paragraph 1 (prefer `This subsection argues that ...`).",
                "- Rewrite paragraph openings to include explicit logical connectors (causal/contrast/extension/implication).",
                "- Do not add new citation keys; keep scope within the subsection.",
            ]
        )

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
