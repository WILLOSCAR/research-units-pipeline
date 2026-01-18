# Transitions (no new facts; no citations)

- Guardrail: transitions add no new facts and introduce no new citations.
- Use these as hand-offs: what was established → what remains unclear → why the next unit follows.

## Section openers (H2 → first H3)
- Foundations & Interfaces → 3.1: Foundations & Interfaces begins with Agent loop and action spaces, translating the theme into benchmarks/metrics, compute; mechanism / architecture, data / training setup that later subsections can vary and stress-test.
- Core Components (Planning + Memory) → 4.1: Core Components (Planning + Memory) begins at Planning and reasoning loops, where planner/executor, search, deliberation; control loop design (planner / executor, search), deliberation method (CoT / ToT / MCTS) turns a broad topic into concrete evaluation-ready handles.
- Learning, Adaptation & Coordination → 5.1: Learning, Adaptation & Coordination opens with Self-improvement and adaptation to establish preference, reward, feedback; training signal (SFT / preference / RL), data synthesis + evaluator / reward as the common lens reused across the chapter.
- Evaluation & Risks → 6.1: Benchmarks and evaluation protocols is the first step in Evaluation & Risks: it fixes function calling, tool schema, routing; tool interface (function calling, schemas, protocols), tool selection / routing policy so subsequent comparisons do not drift.

## Within-section (H3 → next H3)

- 3.1 → 3.2: After Agent loop and action spaces, Tool interfaces and orchestration makes the bridge explicit via function calling, tool schema, routing; tool interface (function calling, schemas, protocols), tool selection / routing policy, setting up a cleaner A-vs-B comparison.
- 4.1 → 4.2: Memory and retrieval (RAG) follows naturally by turning Planning and reasoning loops's framing into retrieval, index, write policy; memory type (episodic / semantic / scratchpad), retrieval source + index (docs / web / logs)-anchored evaluation questions.
- 5.1 → 5.2: Multi-agent coordination follows naturally by turning Self-improvement and adaptation's framing into roles, communication, debate; communication protocol + role assignment, aggregation (vote / debate / referee)-anchored evaluation questions.
- 6.1 → 6.2: Rather than restarting, Safety, security, and governance carries forward the thread from Benchmarks and evaluation protocols and stresses it through threat model, prompt/tool injection, monitoring; threat model (prompt / tool injection, exfiltration), defense surface (policy, sandbox, monitoring).

## Between sections (last H3 → next H2)

- 3.2 → Core Components (Planning + Memory): Core Components (Planning + Memory) carries forward function calling, tool schema, routing; tool interface (function calling, schemas, protocols), tool selection / routing policy from Tool interfaces and orchestration but applies it to a different part of the overall argument.
- 4.2 → Learning, Adaptation & Coordination: After Memory and retrieval (RAG) closes the local comparison (retrieval, index, write policy; memory type (episodic / semantic / scratchpad), retrieval source + index (docs / web / logs)), Learning, Adaptation & Coordination revisits the theme at the next layer of abstraction.
- 5.2 → Evaluation & Risks: After Multi-agent coordination closes the local comparison (roles, communication, debate; communication protocol + role assignment, aggregation (vote / debate / referee)), Evaluation & Risks revisits the theme at the next layer of abstraction.

## Between sections (H2 → next H2)

- Introduction → Related Work: Related Work makes the next layer of the argument concrete, emphasizing comparison handles the later subsections reuse.
- Related Work → Foundations & Interfaces: Foundations & Interfaces picks up the thread by reframing Related Work into operational questions the later subsections can stress-test.
- Foundations & Interfaces → Core Components (Planning + Memory): Core Components (Planning + Memory) follows by narrowing to the evidence: what is measured, under what constraints, and what remains ambiguous.
- Core Components (Planning + Memory) → Learning, Adaptation & Coordination: Learning, Adaptation & Coordination makes the next layer of the argument concrete, emphasizing comparison handles the later subsections reuse.
- Learning, Adaptation & Coordination → Evaluation & Risks: Evaluation & Risks picks up the thread by reframing Learning, Adaptation & Coordination into operational questions the later subsections can stress-test.
