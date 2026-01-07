# Catalog

## Pipelines

- `pipelines/lit-snapshot.pipeline.md`：48h 文献快照（bullets/evidence 为主）
- `pipelines/arxiv-survey.pipeline.md`：arXiv survey / review（默认仅在 C2 做一次 HITL 批准）
- `pipelines/arxiv-survey-latex.pipeline.md`：arXiv survey / review（附带 LaTeX scaffold+编译，输出 PDF）
- `pipelines/tutorial.pipeline.md`：教程型产出（目标/概念图/模块/练习）
- `pipelines/systematic-review.pipeline.md`：系统综述（PRISMA 风格 checkpoints）
- `pipelines/peer-review.pipeline.md`：审稿/评审（claims→evidence→rubric）

## Skills (repo-scoped)

- Meta / orchestration: `pipeline-router`, `workspace-init`, `unit-planner`, `unit-executor`
- End-to-end runner: `research-pipeline-runner`
- Survey flow: `arxiv-search`, `keyword-expansion`, `survey-seed-harvest`, `dedupe-rank`, `taxonomy-builder`, `outline-builder`, `section-mapper`, `pdf-text-extractor`, `paper-notes`, `claim-evidence-matrix`, `citation-verifier`, `survey-visuals`, `prose-writer`, `latex-scaffold`, `latex-compile-qa`
- Tutorial flow: `tutorial-spec`, `concept-graph`, `module-planner`, `exercise-builder`, `tutorial-module-writer`
- Systematic review flow: `protocol-writer`, `screening-manager`, `extraction-form`, `bias-assessor`, `synthesis-writer`
- Peer review flow: `claims-extractor`, `evidence-auditor`, `novelty-matrix`, `rubric-writer`
