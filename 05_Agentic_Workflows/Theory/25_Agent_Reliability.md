# Topic 25: Agent Reliability - Building Trustworthy Loops

## 1. Scenario: The "Broken Loop"
You build an AI agent to clean up your email.
- **Trial 1:** It successfully deletes a spam email.
- **Trial 2:** It accidentally deletes an email from your boss because the word "Invoice" looked like "Scam."
- **Trial 3:** It gets stuck in a loop trying to delete an email that is "Read-Only" and crashes.
- **The Problem:** AI agents are non-deterministic. They might do something perfect once and fail the next time.

## 2. The Concept: Self-Consistency & Reliability
**Reliability** in agents means ensuring they behave predictably across thousands of runs.

### Reliability Techniques:

1.  **Self-Consistency (Majority Voting):**
    *   **Method:** Run the agent's logic 3 times for the same request. If 2 out of 3 agree on the answer, pick that one.
    *   **Result:** Reduces "random" errors significantly.

2.  **State Verification (The "Guardrail"):**
    *   **Method:** Before taking an action (like deleting a file), a second, smaller model (or a script) checks the action against a set of rules.
    *   **Example:** "Never delete files over 100MB."

3.  **Graceful Degeneracy:**
    *   **Method:** If a tool call fails, the agent should have a "Plan B."
    *   **Logic:** *"If the weather API is down, tell the user the service is unavailable, do NOT make up a temperature."*

4.  **Loop Detection:**
    *   **Logic:** If an agent calls the *exact same tool* with the *exact same arguments* 3 times in a row, FORCE it to stop and ask for human help.

## 3. Workflow Diagram (Text)
[Action] -> [Consistency Check] -> [Constraint Check] -> [Execute] -> [Success?]
    (if No) -> [Self-Correction] -> [Try once more]

## 4. Why Reliability is the #1 Barrier to AI
- **Hallucinations:** One wrong fact can ruin a complex 10-step plan.
- **Prompt Sensitivity:** Changing "Please" to "I need you to" can change the agent's success rate by 5%.
- **Cost vs. Reliability:** Running a check 3 times triples your cost. Where is the balance?

## 5. Interview Corner

1. **"What is 'Majority Voting' in the context of LLMs?"**
   * Answer: It's a technique where you generate multiple paths of reasoning for the same problem and select the most frequent final answer. This helps mitigate the randomness of LLMs.

2. **"How do you handle an agent that enters an 'Infinite Loop'?"**
   * Answer: I implement a `max_iterations` counter (e.g., 10 steps). If the agent hasn't solved the task by then, it must output its best guess or an error message to the user.

3. **"What is 'Self-Correction'?"**
   * Answer: It's when the AI is given the output of its failed attempt and asked to find its own mistake. LLMs are surprisingly good at finding errors they just made.

4. **"Why is 'Deterministic Output' hard for AI agents?"**
   * Answer: Because LLMs are probabilistic at their core. Even with `temperature: 0.0`, some internal optimizations and parallel processing can lead to slightly different results across runs.
