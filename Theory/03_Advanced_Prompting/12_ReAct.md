# Topic 12: ReAct (Reason + Act) - Reasoning with External Tools

## 1. Scenario: The Live Intelligence Agent

You are building a Customer Support AI for a bank. 

**The Problem:**
If a user asks, "What is my account balance?", a normal AI will say "I don't know" or make up a number.
If you just give the AI a "GetBalance" tool, it might call it at the wrong time or with the wrong ID.

**ReAct** forces the AI to check its own logic:
1. **Thought:** "The user is asking for a balance. I first need to verify their Account ID."
2. **Action:** `GetUserID[user@email.com]`
3. **Observation:** "ID is 12345."
4. **Thought:** "Now that I have the ID, I can fetch the balance."
5. **Action:** `GetBalance[12345]`

## 2. The Concept: The Interleaved Loop

ReAct is the "Gold Standard" for building Agents. It mimics how humans solve problems: we think about what we need, we do it, we see the result, and we adjust.

- **Synergy:** Actions help clear up confusing thoughts. Thoughts help prevent stupid actions.
- **Traceability:** You can read the "Thoughts" in the logs to understand exactly why the AI made a mistake.

**Why this matters for Engineers:**
This is the bridge between LLMs and Software. ReAct is how you connect an LLM to your existing APIs, Databases, and the Internet.

## 3. The ReAct Template

In a real agent, the prompt looks like this:

> "Solve the problem using this format:
> Thought: you explain why you are doing something.
> Action: you call one of these tools: [Search, Calculator, MyDatabase].
> Observation: I will provide the result.
> ... (Repeat until done)
> Final Answer: your conclusion."

## 4. Interview Corner

1. **"What is the difference between ReAct and Chain-of-Thought?"**
   * Answer: Chain-of-Thought is purely internal (thinking only). ReAct is external (thinking + using tools).

2. **"What happens if the 'Observation' is empty or an error?"**
   * Answer: A good ReAct model will read the error in the Observation and use its next 'Thought' to try a different approach (e.g., "The search failed, I will try searching for a different keyword").

3. **"Why is 'Thought' indispensable?"**
   * Answer: Without explicit reasoning, models often suffer from 'Action Drift' where they lose track of the original goal after a few tool calls.

4. **"Can ReAct run forever?"**
   * Answer: Yes, if the model gets into a loop. Engineers must implement 'Max Iterations' (e.g., 5 loops max) to prevent infinite API costs.

5. **"Which models are best for ReAct?"**
   * Answer: High-reasoning models like GPT-4, Claude 3 Opus, or Gemini 1.5 Pro. Smaller models often forget the formatting rules ("Thought/Action/Observation") and break the loop.

## 5. Practical Insight

- **The 'Pause' Technique:** In code, you stop the generation after the AI writes its **Action**. You then run the actual function in Python, get the result, and append it back to the prompt before calling the AI again.
- **Agentic Workflows:** Tools like **LangGraph** or **AutoGPT** are essentially advanced implementations of the ReAct paper.
- **When NOT to use:** For tasks that don't need external data. If the AI already has all the info in its context, a simple Chain-of-Thought is faster and cheaper.
