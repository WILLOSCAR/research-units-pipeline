# Transitions

- Introduction → Related Work: With the scope fixed around closed-loop agents, prior work becomes clearer when grouped by which interface contracts and evaluation protocols it assumes.
- Related Work → Foundations & Interfaces: Before comparing planning or memory, the agent must have a well-defined action space and tool boundary that makes its behavior interpretable.
- Foundations & Interfaces → Core Components (Planning + Memory): Once actions and observations are grounded, long-horizon behavior depends on how agents plan over actions and what memory they carry across steps.
- Core Components (Planning + Memory) → Learning, Adaptation & Coordination: When planning and memory are fixed, adaptation and coordination become the mechanisms that reshape policies and distribute decision-making over time.
- Learning, Adaptation & Coordination → Evaluation & Risks: These mechanisms are only comparable under matched protocols, which makes evaluation design and risk analysis the natural endpoint of the taxonomy.
- Evaluation & Risks → Discussion: After reviewing benchmarks and threat models, the discussion synthesizes cross-chapter trade-offs and highlights what remains hard to measure.
- Discussion → Conclusion: The conclusion closes the loop by restating the central lens: interface contracts and protocols determine which agent claims are meaningful.
- 3.1 → 3.2: Once the agent loop defines what actions are possible, tool interfaces determine how those actions are grounded in executable APIs and how orchestration policies manage ambiguity and failure.
- 4.1 → 4.2: Planning determines which actions to take under uncertainty, while memory determines what evidence those decisions can reliably condition on across long horizons.
- 5.1 → 5.2: Adaptation changes how an agent updates behavior from feedback, and coordination extends this dynamic to interacting agents whose communication protocols reshape the loop.
- 6.1 → 6.2: Protocol design enables interpretable evaluation, but threat models and governance assumptions are required to make safety and security claims meaningful in deployed agents.
