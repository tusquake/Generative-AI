# Topic 24: Planning & Execution - The Strategy Layer

## 1. Scenario: The "Overwhelmed Travel Agent"
You tell an AI: "Plan a 3-day trip to Tokyo, book a hotel near Shibuya, and find me three ramen spots that are open on Tuesdays."
- **The Impulsive Agent:** Immediately starts searching for hotels. Then realizes it doesn't know the budget. Then finds ramen spots but forgets they need to be in Shibuya. The result is a mess.
- **The Planning Agent:** Takes a breath. It writes:
  1. Ask the user for their budget.
  2. Search for hotels in Shibuya within that budget.
  3. Validate which ramen spots are open on Tuesdays.
  4. Present the final itinerary.
- **Result:** The agent is organized, efficient, and less likely to fail.

## 2. The Concept: Planning Frameworks
**Planning** is the "Think-Before-You-Act" phase of an AI agent. It breaks a complex high-level goal into smaller, executable steps.

### Common Planning Methods:

1.  **Chain-of-Thought (CoT):** "Step 1 is X, Step 2 is Y." (Simple, linear).
2.  **ReAct (Reason + Act):** The agent writes a "Thought," then takes an "Action," then "Observes" the result. It iterates until the goal is met. (Dynamic).
3.  **Plan-and-Solve:** The agent generates the *entire* plan first, then executes it step-by-step. If a step fails, it "Re-plans."
4.  **Self-Reflection:** After executing a plan, the agent reviews its own work: *"Did I actually find ramen spots that are open on Tuesday? No, I missed that. Let me fix it."*

## 3. Workflow Diagram (Text)
[User Goal] -> [Planner] -> [Step 1, Step 2, Step 3] -> [Executor executes Step 1] -> [Check Success] -> [Proceed to Step 2]

## 4. Why Planning Fails
- **Error Propagation:** If Step 1 fails or returns bad data, the whole plan can collapse.
- **Stochastic Behavior:** LLMs might change the plan halfway through for no reason.
- **Inertia:** The agent keeps trying the same failing action over and over (an "Infinite Loop").

## 5. Interview Corner

1. **"What is the difference between 'Linear Planning' and 'Dynamic Planning'?"**
   * Answer: Linear planning generates all steps at once and follows them. Dynamic planning (like ReAct) observes the outcome of each step and decides what to do next in real-time.

2. **"How does an agent know when to 'Stop' planning and start 'Doing'?"**
   * Answer: By using a "Stop Token" or a specific format. Usually, the prompt tells the AI: *"When you have enough information, output a FINAL ANSWER."*

3. **"What is the 'Reflection' pattern in agent planning?"**
   * Answer: It is a pattern where the AI is asked to "grade" its own initial plan or output before showing it to the user. This "double-check" logic is remarkably effective at catching small errors.

4. **"What is 'Task Decomposition'?"**
   * Answer: It is the ability to break a "Big Task" (Build a website) into "Atomized Tasks" (Write HTML, Write CSS, Test Button). This makes the task manageable for the LLM's narrow context window for each specific action.
