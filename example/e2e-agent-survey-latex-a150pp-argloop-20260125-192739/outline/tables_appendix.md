**Appendix Table A1. Representative agent approaches and their interface and loop assumptions (selected examples).**

| Approach / work family | Core idea | Interface / loop assumption | Key refs |
|---|---|---|---|
| Reasoning-action interleaving | interleave reasoning traces with environment and tool actions | closed-loop, multi-step interaction where actions become context for later decisions | [@Yao2022React] |
| Memory retrieval as an agent module | treat memory retrieval as an autonomous component | retrieval decisions are part of the agent loop; memory access policy affects comparability | [@Du2025Memr] |
| Interface hardening (memory and tool guardrails) | reduce attack success by constraining memory and tool interactions | adversarial inputs are in-scope; guardrails are evaluated as part of the loop | [@Wei2025Memguard] |
| Tool protocol orchestration | compare tool modes under a protocolized interface | explicit tool protocol; repeated interactions surface reliability limits | [@Lumer2025Memtool] |
| Benchmark-driven agent framework | evaluate agents across diverse settings (web, embodied, tool use, games) | comparability depends on consistent environments and tool-access assumptions | [@Shang2024Agentsquare] |
| Benchmark landscape synthesis | aggregate large benchmark landscapes to track evaluation drift | protocols vary by task, metric, and budget; alignment is needed for cross-paper comparison | [@Hu2025Survey] |
| Context optimization for agents | optimize contexts offline and online as an adaptation mechanism | prompt and context are part of controllable state; stability depends on protocol constraints | [@Zhang2025Agentic] |
| Security benchmarking for tool protocols | characterize attack surfaces and vulnerabilities in tool interfaces | threat model and system and tool boundary determine what "attack success" means | [@Zhang2025Security; @Gasmi2025Bridging] |

**Appendix Table A2. Evaluation settings and protocol anchors for LLM agents (examples).**

| Benchmark / setting | Task family + metric (example) | Key protocol constraints (what must be reported) | Key refs |
|---|---|---|---|
| ALFWorld; WebShop | interactive decision making; task success | step budget; tool access; environment stochasticity; cost and latency | [@Yao2022React] |
| ScaleMCP | tool-protocol interactions; success over repeated sessions | consecutive user interactions; model suite; protocol versioning; tool availability | [@Lumer2025Memtool] |
| MCP Security Benchmark (MSB) | attacks on tool protocols; attack success rate | threat model; injection channel; system and tool boundary; mitigations | [@Zhang2025Security; @Gasmi2025Bridging] |
| GAIA; BrowseComp+ | agentic browsing and composite tasks; success rate | tool budget; time and step limits; evaluation rubric; access constraints | [@Zhang2026Evoroute] |
| ASAP benchmark (AutoSCORE) | scoring tasks; accuracy and quality metrics | model choice (open vs proprietary); prompt format; dataset splits | [@Wang2025Autoscore] |
| Rubric-based multi-agent evaluation (ARCANE) | multi-agent tasks; rubric-based scoring | role protocol; aggregation and voting; interaction budget | [@Masters2025Arcane] |
