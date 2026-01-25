Interface choices largely determine what an agent can reliably do and what its measured performance means. Viewing agents as closed-loop systems makes it natural to treat action spaces, observation channels, and tool protocols as first-class design variables rather than peripheral implementation details [@Yao2022React; @Zhang2025Tool].

This chapter therefore separates (i) the agent loop and action space abstraction from (ii) the concrete tool interface and orchestration layer. The first subsection focuses on how loop assumptions shape failure recovery and evaluation comparability, while the second focuses on how schema design, routing, and protocolization affect reliability and safety under repeated interactions [@Lumer2025Memtool; @Liu2025Mcpagentbench].

