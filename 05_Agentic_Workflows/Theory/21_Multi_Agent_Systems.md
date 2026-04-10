# Topic 21: Multi-Agent Systems - Coordination and Collaboration

## 1. Scenario: The "Startup Team" AI
Imagine you are building a full software application using AI.
- **The Old Way (Single Agent):** You ask one LLM to write the code, design the UI, write the tests, and deploy. The LLM gets confused, forgets parts of the code, and hallucinates API keys.
- **The New Way (Multi-Agent):** You hire three "specialists":
  1. **Coder Agent:** Writes the logic.
  2. **Reviewer Agent:** Finds bugs in the code.
  3. **DevOps Agent:** Writes the Dockerfile.
- **The Result:** Because each agent has a specific "Role" and a smaller context window to fill, the quality of work skyrockets.

## 2. The Concept: Multi-Agent Orchestration
Multi-Agent Systems (MAS) are architectures where multiple autonomous entities interact to solve a problem that is too complex for a single agent.

### Orchestration Patterns:

1.  **Sequential Chain:** Agent A finishes -> Agent B starts (e.g., Translate then Summarize).
2.  **Manager / Hierarchical:** A "Manager" agent receives the task, decides which sub-agents to call, and compiles their results.
3.  **Joint Collaboration (Peer-to-peer):** Agents talk in a shared "blackboard" or group chat (e.g., AutoGen style).
4.  **Specialization:** Different agents use different system prompts and different tools.

### Key Frameworks:
- **AutoGen (Microsoft):** Agents talk to each other to solve tasks.
- **CrewAI:** Focuses on "Role-playing" and task delegation.
- **LangGraph:** Treat agents as nodes in a state machine.

## 3. Workflow Diagram (Text)
[User Goal] -> [Manager Agent] 
    -> [Agent 1: Researcher] -> (output) -> [Manager]
    -> [Agent 2: Writer] -> (output) -> [Manager]
    -> [Final Answer]

## 4. Challenges of MAS
- **Infinite Loops:** Agent A asks Agent B for help, Agent B asks Agent A.
- **Token Usage:** Multi-agent conversations can consume thousands of tokens in seconds.
- **State Management:** Keeping all agents "aligned" on the current progress of the project.

## 5. Interview Corner

1. **"When should I use Multi-Agent instead of a single powerful model?"**
   * Answer: Use MAS when the task has distinct sub-steps that require different tools or "mindsets" (e.g., creative writing vs. security auditing). MAS is also better for handling very large tasks that exceed a single context window.

2. **"What is the role of a 'Critic' or 'Reflector' agent?"**
   * Answer: It's an agent whose only job is to provide feedback on another agent's work. This "thinking twice" reduces hallucinations and improves code quality significantly.

3. **"Does every agent need its own LLM?"**
   * Answer: Not necessarily. You can use the same LLM (e.g., Gemini 1.5) with different **System Instructions** for each agent.

4. **"What is the 'Manager' pattern in MAS?"**
   * Answer: It is a pattern where one agent acts as a router. It analyzes the user request and delegates to specific worker agents, ensuring the final output is cohesive.
