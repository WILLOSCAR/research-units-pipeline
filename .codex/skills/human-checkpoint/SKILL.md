---
name: human-checkpoint
description: |
  Record a human sign-off at a declared checkpoint (tick `Approve C*` in `DECISIONS.md`) so the pipeline can resume.
  **Trigger**: approve checkpoint, human approval, sign off, HITL, Approve C2, 审批, 签字, 人类检查点.
  **Use when**: A unit has `owner=HUMAN` and is BLOCKED waiting for a checkbox in `DECISIONS.md`.
  **Skip if**: The approval is already recorded (the checkbox is ticked).
  **Network**: none.
  **Guardrail**: Do not modify any content artifacts; only update `DECISIONS.md` (and optionally append a short sign-off note).
---

# Human Checkpoint (HITL sign-off)

Goal: make human approvals explicit and auditable, so downstream units can safely proceed.

This skill is intentionally simple: it standardizes how a human signs off in `DECISIONS.md`.

## Inputs

Required:
- `DECISIONS.md`

Optional:
- `UNITS.csv` (to confirm which checkpoint is currently blocked, e.g., `C1`/`C2`)
- `STATUS.md` (to confirm the current checkpoint)

## Outputs

- `DECISIONS.md` (updated checkbox + short sign-off note)

## Procedure

1. Identify the blocked checkpoint
   - Check the runner message (or `STATUS.md`), or inspect `UNITS.csv` for the first `owner=HUMAN` unit that is `BLOCKED`.

2. Open `DECISIONS.md` and find the approvals checklist
   - Look for a line like: `- [ ] Approve C2 ...`

3. Review the artifacts required by that checkpoint
   - The pipeline doc (`pipelines/*.pipeline.md`) usually lists what to review (e.g., protocol, outline, module plan).
   - If the checkpoint block is missing, add a short checklist into `DECISIONS.md` (what you reviewed).

4. Approve
   - Tick the checkbox: `- [x] Approve C*`
   - Append a short note under the checkpoint block (recommended):
     - Date
     - Artifacts reviewed
     - What you approved + constraints (if any)
     - Signed by

## Acceptance

- The correct `Approve C*` checkbox in `DECISIONS.md` is ticked (`[x]`).
- Any added sign-off note does not silently expand scope or contradict the run goal.

## Troubleshooting

### The approvals checklist is missing in `DECISIONS.md`

Fix:
- Run `pipeline-router` for the relevant checkpoint block, or add a minimal block manually:

```markdown
## Approvals (check to unblock)
- [ ] Approve C2
```
