from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PipelineSpec:
    path: Path
    name: str
    units_template: str
    default_checkpoints: list[str]

    @staticmethod
    def load(path: Path) -> "PipelineSpec":
        text = path.read_text(encoding="utf-8")
        frontmatter = _parse_frontmatter(text)
        name = str(frontmatter.get("name") or path.stem.replace(".pipeline", ""))
        units_template = str(frontmatter.get("units_template") or "")
        default_checkpoints = list(frontmatter.get("default_checkpoints") or [])
        if not units_template:
            raise ValueError(f"Missing units_template in pipeline front matter: {path}")
        return PipelineSpec(
            path=path,
            name=name,
            units_template=units_template,
            default_checkpoints=default_checkpoints,
        )


def _parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Pipeline file must start with YAML front matter '---'")
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("Unterminated YAML front matter (missing closing '---')")
    raw = "\n".join(lines[1:end_idx])
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError("Pipeline YAML front matter must be a mapping")
    return data

