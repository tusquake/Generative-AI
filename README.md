# Generative AI Mastery & Learning Repository

This repository is a comprehensive learning platform for **Generative AI Engineering**. It combines a systematically structured 50-topic mastery curriculum with production-grade conceptual implementations and standalone AI applications.

---

## 🎓 50-Topic Mastery Curriculum
We are covering 50 critical topics in Generative AI, organized into 10 domains. Each domain contains **Theory** (conceptual guides & interview prep) and **Practice** (Python/JS implementations) co-located within their respective folders.

**Current Progress**: 25/50 Topics Completed (Domains 1-5)

### 🧱 Domain 1: Foundations
*How LLMs work under the hood.*
- [x] [01. Architecture Intuition](01_Foundations/Theory/01_Architecture.md)
- [x] [02. Tokenization & Context Windows](01_Foundations/Theory/02_Tokenization.md)
- [x] [03. Sampling Parameters](01_Foundations/Theory/03_Sampling_Parameters.md)
- [x] [04. API Fundamentals](01_Foundations/Theory/04_API_Fundamentals.md)
- [x] [05. System vs. User Prompts](01_Foundations/Theory/05_System_vs_User.md)

### ✍️ Domain 2: Prompt Engineering
*Improving output quality via static instructions.*
- [x] [06. Zero-Shot Prompting](02_Prompt_Engineering/Theory/06_Zero_Shot.md)
- [x] [07. Few-Shot Prompting](02_Prompt_Engineering/Theory/07_Few_Shot.md)
- [x] [08. Chain-of-Thought](02_Prompt_Engineering/Theory/08_Chain_of_Thought.md)
- [x] [09. Self-Correction](02_Prompt_Engineering/Theory/09_Self_Correction.md)
- [x] [10. Role Prompting](02_Prompt_Engineering/Theory/10_Role_Prompting.md)

### 🧠 Domain 3: Advanced Prompting & Reasoning
*Advanced logical frameworks for complex problem solving.*
- [x] [11. Tree of Thoughts](03_Advanced_Prompting/Theory/11_Tree_of_Thoughts.md)
- [x] [12. ReAct (Reason + Act)](03_Advanced_Prompting/Theory/12_ReAct.md)
- [x] [13. Directional Stimulus](03_Advanced_Prompting/Theory/13_Directional_Stimulus.md)
- [x] [14. Program-of-Thoughts](03_Advanced_Prompting/Theory/14_Program_of_Thoughts.md)
- [x] [15. Automatic Prompt Engineer](03_Advanced_Prompting/Theory/15_Automatic_Prompt_Engineer.md)

### 📂 Domain 4: Data & Context (RAG)
*Retrieving private data to ground the AI's knowledge.*
- [x] [16. RAG Fundamentals](04_Data_and_Context/Theory/16_RAG_Fundamentals.md)
- [x] [17. Vector Databases & Embeddings](04_Data_and_Context/Theory/17_Vector_Databases_and_Embeddings.md)
- [x] [18. Chunking Strategies](04_Data_and_Context/Theory/18_Chunking_Strategies.md)
- [x] [19. Context Management](04_Data_and_Context/Theory/19_Context_Management.md)
- [x] [20. Evaluation & Grounding](04_Data_and_Context/Theory/20_Evaluation_and_Grounding.md)

### 🤖 Domain 5: Agentic Workflows
*Building autonomous loops that can take actions.*
- [x] [21. Multi-Agent Systems](05_Agent_Workflows/Theory/21_Multi_Agent_Systems.md)
- [x] [22. Tool Calling & Function Binding](05_Agent_Workflows/Theory/22_Tool_Calling.md)
- [x] [23. Memory Management](05_Agent_Workflows/Theory/23_Memory_Management.md)
- [x] [24. Planning & Plan Execution](05_Agent_Workflows/Theory/24_Planning_and_Execution.md)
- [x] [25. Agent Reliability & Self-Consistency](05_Agent_Workflows/Theory/25_Agent_Reliability.md)

### 🎨 Domain 6: Multi-Modality
*Beyond text: Vision, Audio, and Image Generation.*
- [ ] 26. Vision-Language Models (VLM)
- [ ] 27. Image Generation (Stable Diffusion/DALL-E)
- [ ] 28. Audio Synthesis & STT
- [ ] 29. Video Generation Fundamentals
- [ ] 30. Specialized Architectures (MoE, State Space)

### 🛡️ Domain 7 - 10: Advanced Topics
*Fine-tuning, Evaluation, LLMOps, and Future Trends.*
- [ ] 31. SFT & PEFT (LoRA)
- [ ] 36. LLM-as-a-Judge
- [ ] 41. Quantization & Deployment
- [ ] 50. AGI Roadmap & Ethics
*(Full list available in the commit history)*

---

## 🚀 Standalone Projects & SDKs
- **[gemini-rag-chatbot/](file:///c:/Users/tushar.seth/Desktop/LLD/Generative-AI/gemini-rag-chatbot/)**: Full-stack RAG implementation.
- **[AI Agent/](file:///c:/Users/tushar.seth/Desktop/LLD/Generative-AI/AI%20Agent/)**: Function calling and tool integration demos.
- **[Cursor/](file:///c:/Users/tushar.seth/Desktop/LLD/Generative-AI/Cursor/)**: Agentic workflows for code execution.
- **[MCP Server/](file:///c:/Users/tushar.seth/Desktop/LLD/Generative-AI/MCP%20Server/)**: Model Context Protocol integration.
- **[OpenAI Agent SDK/](file:///c:/Users/tushar.seth/Desktop/LLD/Generative-AI/OpenAI%20Agent%20SDK/)**: Alternative agent frameworks.

---

## 🔑 Key Technologies
- **Models**: Google Gemini 2.0/2.5 Flash, OpenAI.
- **Vector DBs**: Pinecone, ChromaDB.
- **Frameworks**: LangChain, AutoGen, CrewAI, MCP.
- **Languages**: Python, JavaScript (Node.js).

---

## ⚙️ Installation & Setup

1.  Clone the repository and install dependencies at the root or within specific project folders.
2.  Configure your environment:
    ```bash
    GOOGLE_API_KEY=your_key_here
    PINECONE_API_KEY=your_key_here
    ```
3.  **Run a Topic**:
    ```bash
    # Example: Run a foundations practice script
    python 01_Foundations/Practice/01_Architecture.py
    ```

---
*Keep this file updated as we progress through the 50-topic mastery journey.*
