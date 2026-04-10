# Topic 23: Memory Management - Context, State, and Retrieval

## 1. Scenario: The "Forgetful Personal Assistant"
Imagine you are building a personal travel agent AI.
- **Short-term memory:** You tell the AI, "I want to go to Paris." The AI should remember that for the *next* message when you say, "How's the weather there?"
- **Long-term memory:** You told the AI *three months ago* that you are allergic to peanuts. If it suggests a restaurant today, it should remember that allergy.
- **The Problem:** LLMs naturally have zero memory between sessions. Every API call is a "forgetful" start.

## 2. The Concept: Memory Architecture
AI memory is simulated by intentionally feeding past data back into the current prompt.

### 1. Short-Term Memory (Context Window)
- **Method:** Passing the last 5-10 messages of the conversation (Topic 19).
- **Limit:** Once the conversation exceeds the "Context Window" limit, the AI starts "forgetting" the beginning.

### 2. Long-Term Memory (External Retrieval)
- **Method:** Storing user preferences or old chats in a **Vector Database** (Topic 17/19).
- **Execution:** When the user speaks, the system searches the DB for relevant past memories and adds them as a hidden "Context" snippet.

### 3. Entity Memory (The "Knowledge Graph" approach)
- **Method:** Extracting clear facts (e.g., "User likes spicy food") and storing them in an organized database, not just text.

## 3. Workflow Diagram (Text)
[New Prompt] -> [Check Vector DB for past memories] -> [Retrieve allergy info] -> [Combine with 5 recent chat messages] -> [Final LLM Input]

## 4. Why Memory is hard for Agents
- **Relevance:** Which memory is the most important right now?
- **Consistency:** What if the user says "I like Paris" on Monday and "I hate Paris" on Friday?
- **Privacy:** Managing which memories are personal and should be deleted (GDPR/Data Privacy).

## 5. Interview Corner

1. **"What is the 'Buffer Window' approach to AI memory?"**
   * Answer: It is keeping a rolling list of the most recent N tokens or messages and discarding everything older. It is the cheapest and most common way to handle short-term chat history.

2. **"How do you implement 'Semantic Memory' in an agent?"**
   * Answer: By using a Vector Database. You embed each old interaction. When the user asks something, you perform a similarity search to find the most "semantically" related past topics.

3. **"What is 'MemGPT'?"**
   * Answer: It's a research concept where the AI is given the ability to "swap" memory in and out of its context window manually, similar to how a computer uses RAM and a Hard Drive.

4. **"Does an agent's memory need to be read-only?"**
   * Answer: No. Advanced agents can use a tool like `update_user_preference` to actively change their own long-term memory based on new information.
