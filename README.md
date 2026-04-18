# Generative AI Engineering Mastery

A comprehensive engineering-focused platform for mastering Generative AI, from LLM fundamentals to production-grade Agentic Workflows and LLMOps.

---

## Core Philosophy

This repository is designed for engineers who want to go beyond simple prompting. It focuses on the underlying mechanics of Large Language Models (LLMs), retrieval systems, and autonomous agents. Every topic includes detailed theoretical insights and production-ready implementation patterns.

---

## Engineering Curriculum

The curriculum is organized into 10 specialized domains covering the entire lifecycle of Generative AI applications.

### Domain 1: Foundations
*Internal mechanics, scaling, and foundational architectures.*

- [01. Architecture Intuition](01_Foundations/Architecture/README.md)
- [02. Tokenization & Context Windows](01_Foundations/Theory/02_Tokenization.md)
- [03. Sampling Parameters](01_Foundations/Theory/03_Sampling_Parameters.md)
- [04. API Fundamentals](01_Foundations/Theory/04_API_Fundamentals.md)
- [05. System vs. User Prompts](01_Foundations/Theory/05_System_vs_User.md)
- [06. Structured Outputs & JSON Mode](01_Foundations/Theory/06_Structured_Outputs_&_JSON_Mode.md)

---

### Domain 2: Prompt Engineering
*Optimizing model performance through instruction design.*

- [07. Zero-Shot Prompting](02_Prompt_Engineering/Theory/07_Zero_Shot.md)
- [08. Few-Shot Prompting](02_Prompt_Engineering/Theory/08_Few_Shot.md)
- [09. Chain-of-Thought](02_Prompt_Engineering/Theory/09_Chain_of_Thought.md)
- [10. Self-Correction](02_Prompt_Engineering/Theory/10_Self_Correction.md)
- [11. Role Prompting](02_Prompt_Engineering/Theory/11_Role_Prompting.md)

---

### Domain 3: Advanced Reasoning
*Logic frameworks for complex problem solving.*

- [12. Tree of Thoughts](03_Advanced_Prompting/Theory/12_Tree_of_Thoughts.md)
- [13. ReAct (Reason + Act)](03_Advanced_Prompting/Theory/13_ReAct.md)
- [14. Directional Stimulus](03_Advanced_Prompting/Theory/14_Directional_Stimulus.md)
- [15. Program-of-Thoughts](03_Advanced_Prompting/Theory/15_Program_of_Thoughts.md)
- [16. Automatic Prompt Engineer](03_Advanced_Prompting/Theory/16_Automatic_Prompt_Engineer.md)
- [17. Prompt Injection & Security](03_Advanced_Prompting/Theory/17_Prompt_Injection.md)

---

### Domain 4: Data & Context (RAG)
*Retrieval Augmented Generation for factual grounding.*

- [18. RAG Fundamentals](04_Data_and_Context/Theory/18_RAG_Fundamentals.md)
- [19. Vector Databases & Embeddings](04_Data_and_Context/Theory/19_Vector_Databases_and_Embeddings.md)
- [20. Chunking Strategies](04_Data_and_Context/Theory/20_Chunking_Strategies.md)
- [21. Context Management](04_Data_and_Context/Theory/21_Context_Management.md)
- [22. Evaluation & Grounding](04_Data_and_Context/Theory/22_Evaluation_and_Grounding.md)
- [23. Advanced RAG & Reranking](04_Data_and_Context/Theory/23_Advanced_RAG.md)

---

### Domain 5: Agentic Workflows
*Autonomous loops and multi-agent orchestration.*

- [24. Multi-Agent Systems](05_Agentic_Workflows/Theory/24_Multi_Agent_Systems.md)
- [25. Tool Calling & Function Binding](05_Agentic_Workflows/Theory/25_Tool_Calling.md)
- [26. Memory Management](05_Agentic_Workflows/Theory/26_Memory_Management.md)
- [27. Planning & Plan Execution](05_Agentic_Workflows/Theory/27_Planning_and_Execution.md)
- [28. Agent Reliability & Self-Consistency](05_Agentic_Workflows/Theory/28_Agent_Reliability.md)

---

### Domain 6: Multimodality
*Vision, Audio, Video, and cross-modal embeddings.*

- [29. Vision-Language Models (VLM)](06_Multimodality/Theory/29_VLM.md)
- [30. Image Generation (Stable Diffusion / DALL-E)](06_Multimodality/Theory/30_Image_Generation.md)
- [31. Audio Synthesis & STT](06_Multimodality/Theory/31_Audio.md)
- [32. Video Generation Fundamentals](06_Multimodality/Theory/32_Video_Generation.md)
- [33. Specialized Architectures (MoE, State Space)](06_Multimodality/Theory/33_Architectures.md)
- [34. Multimodal RAG & Vision Search](06_Multimodality/Theory/34_Multimodal_RAG.md)
- [35. Embeddings for Retrieval & Analytics](06_Multimodality/Theory/35_Embeddings.md)

---

### Domain 7: Fine-Tuning & Alignment
*Customizing models for specific behaviors and logic.*

- [36. Fine-Tuning vs. RAG: Strategy Selection](07_Fine_Tuning/Theory/36_Fine_Tuning_vs_RAG.md)
- [37. RLHF, DPO & Alignment](07_Fine_Tuning/Theory/37_Alignment.md)
- [38. Supervised Fine-Tuning (SFT)](07_Fine_Tuning/Theory/38_SFT.md)
- [39. Parameter Efficient Fine-Tuning (PEFT, LoRA)](07_Fine_Tuning/Theory/39_PEFT.md)

---

### Domain 8: Evaluation & Safety
*Adversarial testing and production guardrails.*

- [40. LLM-as-a-Judge (Automated Evaluation)](08_Evaluation/Theory/40_LLM_as_a_Judge.md)
- [41. Benchmarking & Red-Teaming](08_Evaluation/Theory/41_Benchmarking.md)
- [42. Guardrails & Content Safety](08_Evaluation/Theory/42_Guardrails.md)
- [43. Bias, Fairness & Hallucination](08_Evaluation/Theory/43_Bias_Hallucination.md)

---

### Domain 9: LLMOps & Deployment
*Optimization, observability, and scaling for production.*

- [44. Quantization & Deployment Strategies](09_LLMOps/Theory/44_Quantization.md)
- [45. Caching & Latency Optimization](09_LLMOps/Theory/45_Caching.md)
- [46. Observability & Tracing](09_LLMOps/Theory/46_Observability.md)
- [47. Cost Optimization & Model Routing](09_LLMOps/Theory/47_Cost_Optimization.md)
- [48. CI/CD for LLM Applications](09_LLMOps/Theory/48_CICD.md)

---

### Domain 10: Future Trends
*The roadmap to AGI and emerging scaling paradigms.*

- [49. Frontier Models & Scaling Laws](10_Future/Theory/49_Scaling_Laws.md)
- [50. AGI Roadmap & Ethics](10_Future/Theory/50_AGI_Ethics.md)

---

## Standalone Projects

- **gemini-rag-chatbot/**: Full-stack implementation of a RAG-based assistant.
- **AI Agent/**: Function calling and tool integration demos.
- **Cursor/**: Agentic workflows for code execution.
- **MCP Server/**: Model Context Protocol integration.
- **OpenAI Agent SDK/**: Alternative agent framework implementations.

---

## Technology Stack

- **Models**: Google Gemini 1.5/2.0, OpenAI, Anthropic Claude
- **Orchestration**: LangChain, AutoGen, CrewAI, MCP
- **Vector Storage**: Pinecone, ChromaDB
- **Evaluation**: LangSmith, Langfuse, Ragas
- **Safety**: Llama Guard, NeMo Guardrails
- **Environment**: Python, Node.js, Docker

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tusquake/Generative-AI.git
   ```

2. Configure environment variables in a `.env` file:
   ```env
   GOOGLE_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   PINECONE_API_KEY=your_key_here
   ```

3. Explore a specific topic:
   ```bash
   # Example: Run foundation practice
   python 01_Foundations/Practice/01_Architecture.py
   ```

---


*This curriculum is continuously updated with the latest breakthroughs in the Generative AI landscape.*