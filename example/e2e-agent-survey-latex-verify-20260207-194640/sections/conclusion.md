## Conclusion

Tool-using LLM agents are best understood as closed-loop systems whose behavior depends jointly on the agent loop, the interface contract, and protocol constraints such as budgets and threat models. This perspective clarifies why results can be difficult to compare across papers: changing tool schemas, permissions, or termination rules can shift measured performance as much as changing the underlying model or planner. [@Yao2022React; @Liu2025Mcpagentbench; @Mohammadi2025Evaluation]

Three takeaways follow. First, interface contracts determine what evaluation claims are even interpretable, so benchmarks and papers should publish tool schemas and execution constraints alongside metrics. Second, planning, memory, and adaptation mechanisms should be compared within compatible protocols, with explicit accounting for cost and latency when those are part of the claim. Third, safety and governance constraints must be integrated into evaluation because tool access expands the attack surface and creates new failure modes that benign metrics can hide. [@Fu2025Eval; @Zhang2026Evoroute; @Zhang2025Security; @Mou2026Toolsafe]

The most actionable path forward is to standardize protocol reporting and benchmark metadata so that future work can separate model-level capability from orchestration choices and can evaluate robustness under explicit threat models. [@Chowa2025From; @Mohammadi2025Evaluation; @Kale2025Reliable]

