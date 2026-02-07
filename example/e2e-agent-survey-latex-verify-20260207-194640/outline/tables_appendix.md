Appendix Table A1. Agent loop patterns and interface assumptions (representative works).

| Pattern | What changes in the agent loop | Interface / assumptions (what must be specified) | Key refs |
|---|---|---|---|
| Think-Act-Observe prompting | Interleave reasoning and tool actions; update plans from observations | Tool schema + observation format; step budget/state | [@Yao2022React] |
| Self-supervised tool calling | Model learns to insert tool calls during generation | Tool execution sandbox; consistent tool outputs | [@Schick2023Toolformer] |
| Reflection-based self-improvement | Use self-critique/feedback to revise prompts or plans after failures | Feedback signal; memory of past attempts | [@Shinn2023Reflexion] |
| Search/planning over thoughts | Explore candidate reasoning branches before acting | Scoring/selection rule; budgeted search | [@Yao2023Tree] |
| Skill/library-driven embodied agent | Acquire reusable skills/tools for long-horizon tasks | Environment API; skill representation + retrieval | [@Wang2023Voyager] |
| Dataset-driven tool-use SFT | Scale instruction/traces to improve tool selection and execution | Standardized tool definitions; train/eval harness | [@Yang2025Toolmind; @Song2025Agent; @Du2024Anytool] |
| Protocolized tool interface (MCP / function calling) | Standardize discovery, invocation, and tool-side metadata | Schema/versioning; permissions/sandbox; observability | [@Liu2025Mcpagentbench; @Gasmi2025Bridging] |
| Multi-agent coordination | Split subtasks across agents; aggregate via vote/referee | Role protocol; message format; conflict resolution | [@Feng2025Group; @Yang2024Based] |
| Cost/latency-aware routing | Optimize tool routing to reduce cost/latency without losing task success | Budget metrics + tracing; cost-aware policy | [@Zhang2026Evoroute] |
| Safety/guardrail layer | Detect and mitigate prompt injection and malicious tool outputs | Threat model; safe tool invocation policy | [@Zhang2025Security; @Mou2026Toolsafe; @Fu2025Eval] |

Appendix Table A2. Benchmarks and evaluation settings for tool-using agents (examples).

| Benchmark / setting | What it tests | Typical metric(s) | Notes / constraints | Key refs |
|---|---|---|---|---|
| ALFWorld | Interactive, multi-step decision making | Success rate / completion | Environment interaction; step budget | [@Yao2022React] |
| WebShop | Web navigation + tool-augmented reasoning | Success rate / task completion | Long-horizon browsing; noisy observations | [@Yao2022React] |
| GAIA | General agentic problem solving | Task success | Often paired with cost/latency analysis | [@Zhang2026Evoroute] |
| BrowseComp+ | Web browsing competency | Task success; cost/latency | Tool calls; latency-sensitive workflows | [@Zhang2026Evoroute] |
| MCPAgentBench | Tool-use via MCP definitions | Pass rate / tool correctness | Realistic tool schemas/protocols | [@Liu2025Mcpagentbench] |
| SOP-Bench | Industrial API workflows | Task success on 1,800+ tasks | Domain diversity; human-validated cases | [@Nandi2025Bench] |
| BFCL (function calling) | Function-call selection + arguments | Leaderboard score / success | Focus on structured tool calls | [@Lu2025Just] |
| M3ToolEval, TauBench | Multi-turn tool-use agents | Benchmark score / success | Emphasizes multi-step tool use | [@Zhou2025Self] |
| MMAU | Broad agent capabilities suite | Aggregate score | Multi-task prompting protocol | [@Yin2024Mmau] |
| AgentDojo (prompt injection) | Robustness to injection attacks | ASR vs utility | Defense trade-offs are common | [@Zhong2025Rtbas; @Alizadeh2025Simple] |
| RAS-Eval and related attack suites | Tool-use security evaluation | ASR / privacy leakage | Attack-task suites; multiple tool formats | [@Fu2025Eval; @Mo2025Attractive] |
| Tool-safety guardrail evaluation | Harm reduction under attack | Harmful tool invocations; utility | Requires explicit threat model + benign baseline | [@Mou2026Toolsafe] |
