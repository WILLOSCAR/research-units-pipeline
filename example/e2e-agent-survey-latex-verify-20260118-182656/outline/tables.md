# Tables

All tables are generated evidence-first from subsection briefs + evidence packs.

## Table 1: Subsection comparison map (axes + representative works)

| Subsection | Axes | Representative works |
|---|---|---|
| 3.1 Agent loop and action spaces | mechanism / architecture<br>data / training setup<br>evaluation protocol (datasets / metrics / human)<br>efficiency / compute<br>failure modes / limitations | [@Kim2025Bridging; @Zhao2025Achieving; @Liu2025Mcpagentbench; @Qiu2025Locobench; @Fumero2025Cybersleuth] |
| 3.2 Tool interfaces and orchestration | tool interface (function calling, schemas, protocols)<br>tool selection / routing policy<br>sandboxing / permissions / observability<br>mechanism / architecture<br>data / training setup | [@Liu2025Toolscope; @Zhou2025Self; @Dong2025Bench; @Li2025Dissonances; @Lumer2025Memtool] |
| 4.1 Planning and reasoning loops | control loop design (planner / executor, search)<br>deliberation method (CoT / ToT / MCTS)<br>action grounding (tool calls vs environment actions)<br>mechanism / architecture<br>data / training setup | [@Hu2025Training; @Nakano2025Guided; @Seo2025Simuhome; @Hong2025Planning; @Kim2025Bridging] |
| 4.2 Memory and retrieval (RAG) | memory type (episodic / semantic / scratchpad)<br>retrieval source + index (docs / web / logs)<br>write / update / forgetting policy<br>mechanism / architecture<br>data / training setup | [@Anokhin2024Arigraph; @Du2025Memr; @Wei2025Memory; @Tawosi2025Meta; @Abbineni2025Muallm] |
| 5.1 Self-improvement and adaptation | training signal (SFT / preference / RL)<br>data synthesis + evaluator / reward<br>generalization + regression control<br>mechanism / architecture<br>data / training setup | [@Zhou2025Self; @Zhao2025Achieving; @Van2025Survey; @Wu2025Evolver; @Yao2022React] |
| 5.2 Multi-agent coordination | communication protocol + role assignment<br>aggregation (vote / debate / referee)<br>stability (collusion, mode collapse, incentives)<br>mechanism / architecture<br>data / training setup | [@Sarkar2025Survey; @Wang2023Voyager; @Shen2024Small; @Lumer2025Memtool; @Cao2025Skyrl] |
| 6.1 Benchmarks and evaluation protocols | tool interface (function calling, schemas, protocols)<br>tool selection / routing policy<br>sandboxing / permissions / observability<br>task suites (web / code / embodied / tools)<br>metrics (success, cost, reliability, safety) | [@Zhang2025Security; @Mohammadi2025Evaluation; @Shi2025Progent; @Shang2024Agentsquare; @Fu2025Eval] |
| 6.2 Safety, security, and governance | threat model (prompt / tool injection, exfiltration)<br>defense surface (policy, sandbox, monitoring)<br>security evaluation protocol<br>mechanism / architecture<br>data / training setup | [@Zhang2025Security; @Lichkovski2025Agent; @Kale2025Reliable; @Fu2025Eval; @Shi2025Progent] |

## Table 2: Evidence readiness + verification needs

| Subsection | Evidence levels | Verify fields | Representative works |
|---|---|---|---|
| 3.1 Agent loop and action spaces | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>compute/training/inference cost<br>training data and supervision signal<br>failure modes / known limitations | [@Kim2025Bridging; @Zhao2025Achieving; @Liu2025Mcpagentbench; @Qiu2025Locobench; @Fumero2025Cybersleuth] |
| 3.2 Tool interfaces and orchestration | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>training data and supervision signal<br>baseline choices and ablation evidence | [@Liu2025Toolscope; @Zhou2025Self; @Dong2025Bench; @Li2025Dissonances; @Lumer2025Memtool] |
| 4.1 Planning and reasoning loops | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>training data and supervision signal<br>baseline choices and ablation evidence | [@Hu2025Training; @Nakano2025Guided; @Seo2025Simuhome; @Hong2025Planning; @Kim2025Bridging] |
| 4.2 Memory and retrieval (RAG) | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>training data and supervision signal<br>baseline choices and ablation evidence | [@Anokhin2024Arigraph; @Du2025Memr; @Wei2025Memory; @Tawosi2025Meta; @Abbineni2025Muallm] |
| 5.1 Self-improvement and adaptation | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>training data and supervision signal<br>baseline choices and ablation evidence | [@Zhou2025Self; @Zhao2025Achieving; @Van2025Survey; @Wu2025Evolver; @Yao2022React] |
| 5.2 Multi-agent coordination | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>training data and supervision signal<br>baseline choices and ablation evidence | [@Sarkar2025Survey; @Wang2023Voyager; @Shen2024Small; @Lumer2025Memtool; @Cao2025Skyrl] |
| 6.1 Benchmarks and evaluation protocols | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>compute/training/inference cost<br>baseline choices and ablation evidence | [@Zhang2025Security; @Mohammadi2025Evaluation; @Shi2025Progent; @Shang2024Agentsquare; @Fu2025Eval] |
| 6.2 Safety, security, and governance | fulltext=0, abstract=18, title=0 | named benchmarks/datasets used<br>metrics/human-eval protocol<br>training data and supervision signal<br>baseline choices and ablation evidence | [@Zhang2025Security; @Lichkovski2025Agent; @Kale2025Reliable; @Fu2025Eval; @Shi2025Progent] |
