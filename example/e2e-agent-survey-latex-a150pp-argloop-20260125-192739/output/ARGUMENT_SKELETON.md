# Argument skeleton (writer-facing, non-reader)

This document makes the survey argument structure explicit so we can detect (a) discontinuities and (b) premise/definition drift.
It is an intermediate artifact and must never be merged into the paper.

## Global thesis (what the paper is trying to establish)

- Agent results are only comparable when the interface contract and the evaluation protocol (task + metric + constraints) are made explicit.
- Many apparent gains are protocol-contingent; synthesis must therefore prioritize protocol-aligned contrasts and surface transfer limits.

## Chapter roles and dependencies (monotone argument progression)

### S1 Introduction

- Produces:
  - Scope boundary: what counts as an LLM agent in this survey (closed-loop interaction; tool/environment boundary).
  - Survey lens: interfaces, core components (planning/memory), adaptation/coordination, evaluation/risks.
  - Evidence policy: evidence_mode and how to interpret abstract-level claims.

### S2 Related Work

- Consumes: scope boundary + lens axes from S1.
- Produces:
  - Positioning through the same lenses (not self-referential narration).
  - A protocol-first framing for why prior comparisons are fragile.

### S3 Foundations & Interfaces

- Consumes:
  - The protocol-first framing (comparability requires task+metric+constraints).
- Produces:
  - A stable comparability claim: interface/action-space design co-determines what claims are interpretable.

Subsection outputs:
- S3.1 (Agent loop and action spaces):
  - Output: action-space richness trades off against controllability and comparability; protocol context is a first-order confounder.
  - Boundary: many works underspecify budgets/tool access/visibility; synthesis must weaken claims rather than infer missing context.
- S3.2 (Tool interfaces and orchestration):
  - Output: tool contracts (schemas/permissions/observability) explain why the same model behaves differently across benchmarks.
  - Boundary: omitted operational constraints (sandboxing/failure recovery) undermine post hoc comparison.

### S4 Core Components (Planning + Memory)

- Consumes:
  - The interface/protocol comparability lens from S3.
- Produces:
  - A component-level decomposition: planning and memory change failure modes and cost profiles under fixed protocols.

Subsection outputs:
- S4.1 (Planning and reasoning loops):
  - Output: planning loops trade off exploration depth, verification, and cost; evaluation must specify horizon/budget.
  - Boundary: planner effectiveness is sensitive to protocol details (step limits, tool errors, environment versions).
- S4.2 (Memory and retrieval):
  - Output: memory choices trade off retrieval reliability, contamination risk, and auditability.
  - Boundary: results do not transfer when retrieval corpora, update rules, or visibility assumptions differ.

### S5 Learning, Adaptation & Coordination

- Consumes:
  - Component-level failure modes and protocol constraints from S4.
- Produces:
  - A learning/coordination lens: adaptation can improve performance but can also create instability and evaluation leakage.

Subsection outputs:
- S5.1 (Self-improvement and adaptation):
  - Output: self-improvement loops depend on feedback channels and accounting assumptions; protocol must define what is allowed to change.
  - Boundary: risk of reward hacking / unstable updates; claims require explicit update and evaluation protocols.
- S5.2 (Multi-agent coordination):
  - Output: coordination protocols shift error modes (communication overhead, aggregation bias); success depends on cost and role assumptions.
  - Boundary: coordination results are fragile across communication constraints and evaluation budgets.

### S6 Evaluation & Risks

- Consumes:
  - The protocol-first comparability stance developed in S3-S5.
- Produces:
  - An evaluation contract: which benchmarks/protocols support which claims, and what risks must be evaluated as first-class objectives.

Subsection outputs:
- S6.1 (Benchmarks and evaluation protocols):
  - Output: benchmark diversity implies many comparisons are protocol-driven; evaluation must report task family, metric, and constraints.
  - Boundary: benchmark design biases conclusions; synthesis must separate protocol effects from method effects.
- S6.2 (Safety, security, and governance):
  - Output: risk is interface-dependent; threat models and permission boundaries must be part of the evaluation contract.
  - Boundary: fragmented security benchmarks and incompatible tool stacks limit aggregation without explicit alignment.

### Discussion / Conclusion

- Discussion should consume chapter outputs and produce cross-cutting takeaways (protocol alignment, cost-aware robustness, governance).
- Conclusion should restate the global thesis and the strongest decision-relevant implications.

## Premise drift watchlist (non-blocking, but high risk)

- Protocol: always anchor as task + metric + constraint (budget/tool access/horizon/threat model). Do not use as a vague synonym for setup.
- Budget: keep units consistent (steps vs tokens vs monetary cost). Do not mix without stating the mapping.
- Tool access: keep explicit whether access is assumed, constrained, or benchmark-defined; avoid implicit upgrades.
- Agent: keep the boundary stable (agent vs tool-using LM vs workflow automation).
- Security/robustness: keep threat model explicit; avoid upgrading from benchmark robustness to deployment safety.
