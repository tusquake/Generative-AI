# Topic 11: Tree of Thoughts (ToT) - Exploring Multiple Reasoning Paths

## 1. Scenario: The Complex Creative Strategy

You are an AI consultant for a startup. They need to decide how to allocate \$10,000 between Marketing, Engineering, and Sales. 

**The Problem:**
If you just ask "How should I spend it?", the AI will give you a standard 40/40/20 split. It won't consider that if you spend too little on Engineering, the Marketing won't have a product to sell. 

**Tree of Thoughts** forces the AI to explore different "worlds":
- World A: Marketing-heavy
- World B: Product-led Growth
- World C: Sales-driven

It then evaluates which "world" has the best chance of long-term success.

## 2. The Concept: Look Before You Leap

Tree of Thoughts is essentially **Chain-of-Thought + Branching**.

Instead of a single line of thinking, we create a structure:
1. **Brainstorming:** Generate multiple potential next steps.
2. **Evaluation:** Critique each step for "Fitness."
3. **Execution:** Pursue only the most successful branch.

**Why this matters for Engineers:**
LLMs are "greedy." They always pick the most likely *next word*. Sometimes the most likely next word leads to a dead end. ToT allows the model to "peek" at the dead end and turn back.

## 3. How to Prompt for ToT (Simulated)

To do this in a single prompt, you follow this structure:

> "I want you to solve [Problem]. First, generate 3 radically different approaches. Then, for each approach, list one major weakness. Finally, choose the approach that is most robust and provide a detailed plan for just that one."

## 4. Interview Corner

1. **"What is the 'Pruning' in Tree of Thoughts?"**
   * Answer: Pruning is the process of eliminating reasoning paths that are evaluated as unlikely to lead to a solution, saving "compute" (or tokens) for more promising branches.

2. **"Does ToT require a specific model capability?"**
   * Answer: No, it is a prompting framework. However, it relies heavily on the model's ability to be a "discriminator" (judge). The model needs to be smart enough to recognize a bad idea.

3. **"Is ToT faster than Chain-of-Thought?"**
   * Answer: No, it is significantly slower. Because you are generating multiple "thought candidates" and evaluating them, it takes more time and tokens.

4. **"Can you use ToT for coding?"**
   * Answer: Yes! You can ask the AI to generate 3 different algorithms for a function (e.g., Iterative, Recursive, Dynamic Programming), evaluate their Time Complexity, and then only write the code for the most efficient one.

5. **"How does ToT compare to 'Self-Consistency'?"**
   * Answer: Self-Consistency runs the *same* path multiple times and picks the most common answer. ToT explores *different* paths and evaluates which one is logically superior.

## 5. Practical Insight

- **The 'Consultant' Prompt:** This is a famous ToT-style prompt: *"Imagine three different experts are discussing this problem. They each offer one solution. They then critique each other's ideas. Finally, the moderator chooses the best parts of all three."*
- **Algorithmic Use:** True ToT is used in search-based frameworks (like AlphaGo logic for text).
- **When NOT to use:** For standard, low-complexity tasks. It's like using a supercomputer to solve 2+2.
