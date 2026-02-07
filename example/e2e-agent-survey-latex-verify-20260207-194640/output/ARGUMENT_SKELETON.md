# Argument skeleton (writer-facing; never merged into the paper)

## Consistency Contract

Canonical terms (use consistently):
- *Agent (tool-using LLM agent)*: a closed-loop system that observes, decides, acts through external tools, and updates state via feedback.
- *Agent loop*: the recurring control cycle (state -> decide -> act -> observe), including termination/retry behavior.
- *Tool/interface contract*: the executable action/observation boundary (schemas, permissions, sandboxing, observability, validators).
- *Evaluation protocol*: task + metric + constraints (steps/latency/cost) + tool access + termination + (if relevant) threat model.

Scope boundary (what this draft treats as in-scope):
- In-scope: tool-using LLM agents; planning/reasoning loops; memory/retrieval; self-improvement/adaptation; multi-agent coordination; evaluation protocols; safety/security/governance for tool use.
- Out-of-scope by default: embodied robotics; pure RL without tool-using LLM loops; agent-based modeling; non-agent LLM prompting without a tool/action loop.

Evaluation anchor policy (for any numeric claim):
- Always state minimal context in the same paragraph: *benchmark/task*, *metric*, and at least one constraint (*budget: steps/latency/cost*).
- If the claim is about robustness/safety: include the *threat model* and the *governance surface* (permissions/sandbox/monitoring).
- Treat results as *conditional evidence* unless protocol metadata is sufficient for replication.

Citation scope hygiene (writing-time rule):
- Cite only keys in `citations/ref.bib`.
- Prefer subsection-scoped keys (writer packs) and avoid cross-chapter “free cites” unless the work is genuinely cross-cutting.

Style hygiene (paper voice):
- Avoid meta narration (e.g., “This subsection surveys ...”). Open with a content claim or a concrete tension.
- Keep signposting light; use connectors to express relations, not repeated paragraph-starter templates.

## Section map (roles + dependencies)

H2 1. Introduction
- Role: set scope, define the protocol-aware lens, and preview the chapter structure.
- Produces: scope boundary + consistency contract commitments (terms and protocol fields).

H2 2. Related Work
- Role: position relative to prior surveys and adjacent topics (agents, tool use, evaluation, security).
- Produces: what this survey adds (organization lens + evidence-first posture).

H2 3. Foundations & Interfaces
- Role: define the operational object (loop + interface contract) that later comparisons assume.
- Produces: a stable vocabulary for action spaces, orchestration, and protocol fields.

H3 3.1 Agent loop and action spaces
- Consumes: agent-as-closed-loop + protocol field list.
- Adds: loop-as-executable-contract lens; action-space vs verifiability trade-off; protocol-aware reading of reported numbers.

H3 3.2 Tool interfaces and orchestration
- Consumes: loop framing (actions/observations) + budget sensitivity.
- Adds: interface contract as first-class method variable (schemas/permissions/observability) + orchestration-as-policy framing.

H2 4. Core Components (Planning + Memory)
- Role: compare the two components that most strongly shape long-horizon behavior under a fixed interface contract.

H3 4.1 Planning and reasoning loops
- Consumes: interface contract + protocol budgets.
- Adds: planning as a control policy; reactive vs planning-heavy contrast; normalization requirement (latency/cost vs success).

H3 4.2 Memory and retrieval (RAG)
- Consumes: protocol-aware comparison lens + action-loop view of retrieval.
- Adds: persistence vs freshness trade-off; retrieval-as-context vs retrieval-as-control; verification and write-policy requirements.

H2 5. Learning, Adaptation & Coordination
- Role: handle “systems that change” (self-improvement) and “systems that split work” (teams).

H3 5.1 Self-improvement and adaptation
- Consumes: protocol-aware interpretation of gains.
- Adds: constrained vs unconstrained updates; adaptation as a controlled process (what is updated, under what constraints).

H3 5.2 Multi-agent coordination
- Consumes: interface contract + protocol budget framing.
- Adds: coordination as an interaction protocol (roles/messages/aggregation); evaluation must log traces and specify trust boundaries.

H2 6. Evaluation & Risks
- Role: make comparability and deployment safety explicit; treat evaluation and governance as part of the protocol.

H3 6.1 Benchmarks and evaluation protocols
- Consumes: protocol-aware lens from prior chapters.
- Adds: breadth vs diagnostic benchmark contrast; protocol metadata as the unit of comparability; normalization before aggregation.

H3 6.2 Safety, security, and governance
- Consumes: interface contract + benchmark/protocol framing.
- Adds: threat model + permissions/monitoring/sandboxing as evaluation contract fields; robustness claims are system properties.

## Drift watchlist (where things tend to silently change)

- What counts as “the agent”: model-only vs model+tools vs model+orchestrator vs multi-agent team.
- Protocol fields: step limits, retries, termination, tool availability, and whether retrieval/tool outputs are treated as trusted evidence.
- Security framing: whether the threat model is explicit, and which governance controls are assumed (permissions/sandbox/monitoring).
- Baseline labeling: avoid vague “baseline/ours”; keep method family labels stable across chapters.
