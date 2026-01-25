## Conclusion

LLM agents can be understood as closed-loop systems whose apparent capabilities depend as much on interface contracts and protocol constraints as on model quality [@Yao2022React; @Luo2025Universe; @Zhou2026Beyond]. Reading the literature through this lens clarifies why results often fail to transfer: tool access, budgets, and environment assumptions change the meaning of "success" and the visibility of failure modes [@Hu2025Survey; @Shang2024Agentsquare; @Zhang2026Evoroute].

The synthesis in this paper emphasizes protocol-aware contrasts across four lenses: foundations and interfaces, planning and memory components, adaptation and coordination mechanisms, and evaluation and risks. Across these lenses, the most reusable takeaways are rarely single system designs; they are patterns of trade-offs and failure modes that persist across benchmarks when assumptions are made explicit [@Hu2025Evaluating; @Ji2024Testing; @Zhang2025Generalizability].

A final implication is that evaluation and governance are coupled for tool-using agents. Security and safety outcomes hinge on the same interface decisions that drive capability, so threat models and protocol constraints should be treated as first-class evaluation objects rather than post hoc caveats [@Zhang2025Security; @Gasmi2025Bridging; @Wei2025Memguard].

