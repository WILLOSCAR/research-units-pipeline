# Pipeline spec v1 (MD-first)

每个 pipeline 文件为 `pipelines/*.pipeline.md`，并且必须包含 YAML front matter。

## Front matter (required)

```yaml
---
name: <pipeline-name>
version: 1.0
target_artifacts:
  - <path>
default_checkpoints: [C0,C1,C2]
units_template: templates/<UNITS-template>.csv
---
```

## Body (required)

正文必须按 stage 分段，并在每个 stage 中声明：

- `required_skills`: 必需 skills（目录名）
- `optional_skills`: 可选 skills（目录名）
- `produces`: 本 stage 产物（路径）
- `checkpoint`: 该 stage 关联 checkpoint（若有）
- `human_checkpoint`: 人类检查点（若有：写入 `DECISIONS.md` 的签字要求）

> 设计原则：pipeline 不直接“写论文”，而是驱动 workspace 工件逐步满足 checkpoint；满足 checkpoint 后才允许 prose/LaTeX（如果该 pipeline 需要）。

## Consistency rules (recommended)

- `required_skills` in the pipeline doc must be present in the referenced `units_template` CSV.
- `target_artifacts` should be covered by the units’ `outputs` (or be explicitly optional).
- Use `python scripts/validate_repo.py` to sanity-check pipeline↔template↔skill alignment.
