# Claim–Evidence matrix

This artifact is bullets-only and is meant to make evidence explicit before writing.

Generated as a projection of `outline/evidence_drafts.jsonl` (evidence packs).

## 3.1 Agent loop and action spaces

- RQ: Which design choices in Agent loop and action spaces drive the major trade-offs, and how are those trade-offs measured?
- Claim: Experiments on challenging agentic benchmarks such as GAIA and BrowseComp+ demonstrate that EvoRoute, when integrated into off-the-shelf agentic systems, not only sustains or enhances system performance but also reduces
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0092` [@Zhang2026Evoroute] — Experiments on challenging agentic benchmarks such as GAIA and BrowseComp+ demonstrate that EvoRoute, when integrated into off-the-shelf agentic systems, not only sustains or enhances system performance but also reduces execution cost by up to $80\%$ and latency by over $70\%$. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0092#key_results[0])
  - Evidence: `P0016` [@Kim2025Bridging] — We introduce Structured Cognitive Loop (SCL), a modular architecture that explicitly separates agent cognition into five phases: Retrieval, Cognition, Control, Action, and Memory (R-CCAM). (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0016#method)
  - Evidence: `P0027` [@Shen2024Small] — While traditional works focus on training a single LLM with all these capabilities, performance limitations become apparent, particularly with smaller models. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0027#limitations[1])
  - Evidence: `P0199` [@Zhao2025Achieving] — However, due to weak heuristics for auxiliary constructions, AI for geometry problem solving remains dominated by expert models such as AlphaGeometry 2, which rely heavily on large-scale data synthesis and search for both training and evaluation. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0199#key_results[0])
  - Evidence: `P0014` [@Li2025Agentswift] — Evaluated across a comprehensive set of seven benchmarks spanning embodied, math, web, tool, and game domains, AgentSwift discovers agents that achieve an average performance gain of 8.34\% over both existing automated agent search methods and manually designed agents. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0014#key_results[0])
  - Evidence: `P0078` [@Shang2024Agentsquare] — Extensive experiments across six benchmarks, covering the diverse scenarios of web, embodied, tool use and game applications, show that AgentSquare substantially outperforms hand-crafted agents, achieving an average performance gain of 17.2% against best-known human designs. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0078#key_results[0])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 3.2 Tool interfaces and orchestration

- RQ: Which design choices in Tool interfaces and orchestration drive the major trade-offs, and how are those trade-offs measured?
- Claim: This survey provides an in-depth overview of the emerging field of LLM agent evaluation, introducing a two-dimensional taxonomy that organizes existing work along (1) evaluation objectives -- what to evaluate, such as ag
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0047` [@Mohammadi2025Evaluation] — This survey provides an in-depth overview of the emerging field of LLM agent evaluation, introducing a two-dimensional taxonomy that organizes existing work along (1) evaluation objectives -- what to evaluate, such as agent behavior, capabilities, reliability, and safety -- and (2) evaluation process -- how to evaluate, including interaction modes, datasets and benchmarks, metric computation methods, and tooling. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0047#key_results[0])
  - Evidence: `P0017` [@Dong2025Etom] — We introduce ETOM, a five-level benchmark for evaluating multi-hop, end-to-end tool orchestration by LLM agents within a hierarchical Model-Context Protocol (MCP) ecosystem. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0017#method)
  - Evidence: `P0056` [@Liu2025Mcpagentbench] — To address these limitations, we propose MCPAgentBench, a benchmark based on real-world MCP definitions designed to evaluate the tool-use capabilities of agents. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0056#limitations[1])
  - Evidence: `P0054` [@Li2025Dissonances] — Our evaluation of 66 real-world tools from the repositories of two major LLM agent development frameworks, LangChain and LlamaIndex, revealed a significant security concern: 75% are vulnerable to XTHP attacks, highlighting the prevalence of this threat. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0054#key_results[0])
  - Evidence: `P0080` [@Du2024Anytool] — Experiments across various datasets demonstrate the superiority of our AnyTool over strong baselines such as ToolLLM and a GPT-4 variant tailored for tool utilization. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0080#key_results[0])
  - Evidence: `P0058` [@Lumer2025Memtool] — Evaluating each MemTool mode across 13+ LLMs on the ScaleMCP benchmark, we conducted experiments over 100 consecutive user interactions, measuring tool removal ratios (short-term memory efficiency) and task completion accuracy. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0058#key_results[0])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 4.1 Planning and reasoning loops

- RQ: Which design choices in Planning and reasoning loops drive the major trade-offs, and how are those trade-offs measured?
- Claim: Experimental evaluation on the complex task planning benchmark demonstrates that our 1.5B parameter model trained with single-turn GRPO achieves superior performance compared to larger baseline models up to 14B parameter
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0024` [@Hu2025Training] — Experimental evaluation on the complex task planning benchmark demonstrates that our 1.5B parameter model trained with single-turn GRPO achieves superior performance compared to larger baseline models up to 14B parameters, with success rates of 70% for long-horizon planning tasks. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0024#key_results[0])
  - Evidence: `P0087` [@Yin2024Safeagentbench] — To address this gap, we present SafeAgentBench -- the first comprehensive benchmark for safety-aware task planning of embodied LLM agents in interactive simulation environments, covering both explicit and implicit hazards. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0087#method)
  - Evidence: `P0151` [@Seo2025Simuhome] — Our evaluation of 16 agents under a unified ReAct framework reveals distinct capabilities and limitations across models. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0151#limitations[1])
  - Evidence: `P0151` [@Seo2025Simuhome] — Our evaluation of 16 agents under a unified ReAct framework reveals distinct capabilities and limitations across models. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0151#key_results[1])
  - Evidence: `P0001` [@Yao2022React] — On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0001#key_results[0])
  - Evidence: `P0064` [@Zhou2025Siraj] — Across diverse evaluation agent settings, our seed test case generation approach yields 2 -- 2.5x boost to the coverage of risk outcomes and tool-calling trajectories. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0064#key_results[0])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 4.2 Memory and retrieval (RAG)

- RQ: Which design choices in Memory and retrieval (RAG) drive the major trade-offs, and how are those trade-offs measured?
- Claim: Our system introduces a novel Retrieval Augmented Generation (RAG) approach, Meta-RAG, where we utilize summaries to condense codebases by an average of 79.8\%, into a compact, structured, natural language representation
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0019` [@Tawosi2025Meta] — Our system introduces a novel Retrieval Augmented Generation (RAG) approach, Meta-RAG, where we utilize summaries to condense codebases by an average of 79.8\%, into a compact, structured, natural language representation. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0019#key_results[1])
  - Evidence: `P0055` [@Zhang2025Security] — We present MSB (MCP Security Benchmark), the first end-to-end evaluation suite that systematically measures how well LLM agents resist MCP-specific attacks throughout the full tool-use pipeline: task planning, tool invocation, and response handling. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0055#method)
  - Evidence: `P0158` [@Huang2025Retrieval] — SAFE demonstrates robust improvements in long-form COVID-19 fact-checking by addressing LLM limitations in consistency and explainability. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0158#limitations[1])
  - Evidence: `P0055` [@Zhang2025Security] — MSB contributes: (1) a taxonomy of 12 attacks including name-collision, preference manipulation, prompt injections embedded in tool descriptions, out-of-scope parameter requests, user-impersonating responses, false-error escalation, tool-transfer, retrieval injection, and mixed attacks; (2) an evaluation harness that executes attacks by running real tools (both benign and malicious) via MCP rather than simulation; and (3) a robustness metric that quantifies the trade-off between security and performance: Net Resilient Performance (NRP). (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0055#key_results[0])
  - Evidence: `P0060` [@Shi2025Progent] — Our extensive evaluation across various agent use cases, using benchmarks like AgentDojo, ASB, and AgentPoison, demonstrates that Progent reduces attack success rates to 0%, while preserving agent utility and speed. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0060#key_results[0])
  - Evidence: `P0158` [@Huang2025Retrieval] — This study presents SAFE (system for accurate fact extraction and evaluation), an agent system that combines large language models with retrieval-augmented generation (RAG) to improve automated fact-checking of long-form COVID-19 misinformation. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0158#key_results[1])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 5.1 Self-improvement and adaptation

- RQ: Which design choices in Self-improvement and adaptation drive the major trade-offs, and how are those trade-offs measured?
- Claim: Evaluation on two existing multi-turn tool-use agent benchmarks, M3ToolEval and TauBench, shows the Self-Challenging framework achieves over a two-fold improvement in Llama-3.1-8B-Instruct, despite using only self-genera
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0022` [@Zhou2025Self] — Evaluation on two existing multi-turn tool-use agent benchmarks, M3ToolEval and TauBench, shows the Self-Challenging framework achieves over a two-fold improvement in Llama-3.1-8B-Instruct, despite using only self-generated training data. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0022#key_results[0])
  - Evidence: `P0028` [@Li2026Autonomous] — We demonstrate that large language model (LLM) agents can autonomously perform tensor network simulations of quantum many-body systems, achieving approximately 90% success rate across representative benchmark tasks. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0028#method)
  - Evidence: `P0080` [@Du2024Anytool] — We also revisit the evaluation protocol introduced by previous works and identify a limitation in this protocol that leads to an artificially high pass rate. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0080#limitations[1])
  - Evidence: `P0092` [@Zhang2026Evoroute] — Experiments on challenging agentic benchmarks such as GAIA and BrowseComp+ demonstrate that EvoRoute, when integrated into off-the-shelf agentic systems, not only sustains or enhances system performance but also reduces execution cost by up to $80\%$ and latency by over $70\%$. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0092#key_results[0])
  - Evidence: `P0175` [@Zhou2024Star] — Optimized datasets have achieved substantial improvements, with an average increase of 12% and notable gains in specific metrics, such as a 40% improvement in Fermi, as evidenced by benchmarks like MT-bench, Vicuna bench, and WizardLM testset. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0175#key_results[0])
  - Evidence: `P0028` [@Li2026Autonomous] — Systematic evaluation using DeepSeek-V3.2, Gemini 2.5 Pro, and Claude Opus 4.5 demonstrates that both in-context learning and multi-agent architecture are essential. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0028#key_results[1])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 5.2 Multi-agent coordination

- RQ: Which design choices in Multi-agent coordination drive the major trade-offs, and how are those trade-offs measured?
- Claim: However, due to weak heuristics for auxiliary constructions, AI for geometry problem solving remains dominated by expert models such as AlphaGeometry 2, which rely heavily on large-scale data synthesis and search for bot
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0199` [@Zhao2025Achieving] — However, due to weak heuristics for auxiliary constructions, AI for geometry problem solving remains dominated by expert models such as AlphaGeometry 2, which rely heavily on large-scale data synthesis and search for both training and evaluation. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0199#key_results[0])
  - Evidence: `P0023` [@Cao2025Skyrl] — We introduce SkyRL-Agent, a framework for efficient, multi-turn, long-horizon agent training and evaluation. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0023#method)
  - Evidence: `P0045` [@Lichkovski2025Agent] — We encourage future work extending agentic safety benchmarks to different legal jurisdictions and to multi-turn and multilingual interactions. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0045#limitations[1])
  - Evidence: `P0042` [@Shao2025Craken] — On evaluation of MITRE ATT&CK techniques, CRAKEN solves 25-30% more techniques than prior work, demonstrating improved cybersecurity capabilities via knowledge-based execution. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0042#key_results[1])
  - Evidence: `P0218` [@Li2025Continuum] — Our evaluation on real-world agentic workloads (SWE-Bench and BFCL) with Llama-3.1 8B/70B shows that Continuum significantly improves the average job completion times and its improvement scales with turn number increase. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0218#key_results[0])
  - Evidence: `P0058` [@Lumer2025Memtool] — Evaluating each MemTool mode across 13+ LLMs on the ScaleMCP benchmark, we conducted experiments over 100 consecutive user interactions, measuring tool removal ratios (short-term memory efficiency) and task completion accuracy. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0058#key_results[0])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 6.1 Benchmarks and evaluation protocols

- RQ: Which design choices in Benchmarks and evaluation protocols drive the major trade-offs, and how are those trade-offs measured?
- Claim: This survey provides an in-depth overview of the emerging field of LLM agent evaluation, introducing a two-dimensional taxonomy that organizes existing work along (1) evaluation objectives -- what to evaluate, such as ag
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0047` [@Mohammadi2025Evaluation] — This survey provides an in-depth overview of the emerging field of LLM agent evaluation, introducing a two-dimensional taxonomy that organizes existing work along (1) evaluation objectives -- what to evaluate, such as agent behavior, capabilities, reliability, and safety -- and (2) evaluation process -- how to evaluate, including interaction modes, datasets and benchmarks, metric computation methods, and tooling. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0047#key_results[0])
  - Evidence: `P0069` [@Chen2025Towards] — Based on these findings, we present an RPA evaluation design guideline to help researchers develop more systematic and consistent evaluation methods. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0069#method)
  - Evidence: `P0151` [@Seo2025Simuhome] — Our evaluation of 16 agents under a unified ReAct framework reveals distinct capabilities and limitations across models. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0151#limitations[1])
  - Evidence: `P0182` [@Ma2023Large] — Our experiment consists of two parts: first, an evaluation by human experts, which includes assessing the LLMs`s mastery of StarCraft II knowledge and the performance of LLM agents in the game; second, the in game performance of LLM agents, encompassing aspects like win rate and the impact of Chain of Summarization.Experiment results demonstrate that: 1. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0182#key_results[0])
  - Evidence: `P0030` [@Liu2026Agents] — Our major contributions include: (1) systematically analyzing the technical transition from standard legal LLMs to legal agents; (2) presenting a structured taxonomy of current agent applications across distinct legal practice areas; (3) discussing evaluation methodologies specifically for agentic performance in law; and (4) identifying open challenges and outlining future directions for developing robust and autonomous legal assistants. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0030#key_results[0])
  - Evidence: `P0069` [@Chen2025Towards] — This paper proposes an evidence-based, actionable, and generalizable evaluation design guideline for LLM-based RPA by systematically reviewing 1,676 papers published between Jan. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0069#key_results[0])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.

## 6.2 Safety, security, and governance

- RQ: Which design choices in Safety, security, and governance drive the major trade-offs, and how are those trade-offs measured?
- Claim: MSB contributes: (1) a taxonomy of 12 attacks including name-collision, preference manipulation, prompt injections embedded in tool descriptions, out-of-scope parameter requests, user-impersonating responses, false-error
  - Axes: evaluation protocol (datasets; metrics; human evaluation); compute and latency constraints; and failure modes and limitations
  - Evidence levels: fulltext=0, abstract=18, title=0.
  - Evidence: `P0055` [@Zhang2025Security] — MSB contributes: (1) a taxonomy of 12 attacks including name-collision, preference manipulation, prompt injections embedded in tool descriptions, out-of-scope parameter requests, user-impersonating responses, false-error escalation, tool-transfer, retrieval injection, and mixed attacks; (2) an evaluation harness that executes attacks by running real tools (both benign and malicious) via MCP rather than simulation; and (3) a robustness metric that quantifies the trade-off between security and performance: Net Resilient Performance (NRP). (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0055#key_results[0])
  - Evidence: `P0055` [@Zhang2025Security] — We present MSB (MCP Security Benchmark), the first end-to-end evaluation suite that systematically measures how well LLM agents resist MCP-specific attacks throughout the full tool-use pipeline: task planning, tool invocation, and response handling. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0055#method)
  - Evidence: `P0181` [@Kim2024When] — Additionally, our findings underscore the limitations of existing safeguards in contemporary commercial LLMs, emphasizing the urgent need for robust security measures to prevent the misuse of LLM agents. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0181#limitations[1])
  - Evidence: `P0060` [@Shi2025Progent] — Our extensive evaluation across various agent use cases, using benchmarks like AgentDojo, ASB, and AgentPoison, demonstrates that Progent reduces attack success rates to 0%, while preserving agent utility and speed. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0060#key_results[0])
  - Evidence: `P0144` [@Fu2025Eval] — RAS-Eval comprises 80 test cases and 3,802 attack tasks mapped to 11 Common Weakness Enumeration (CWE) categories, with tools implemented in JSON, LangGraph, and Model Context Protocol (MCP) formats. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0144#key_results[1])
  - Evidence: `P0055` [@Zhang2025Security] — We evaluate nine popular LLM agents across 10 domains and 400+ tools, producing 2,000 attack instances. (provenance: paper_notes | papers/paper_notes.jsonl:paper_id=P0055#key_results[1])
  - Caveat: Evidence is not full-text grounded for this subsection; treat claims as provisional and avoid strong generalizations.
