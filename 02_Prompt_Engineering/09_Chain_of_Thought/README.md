# Chain-of-Thought (CoT)

> **Mentor note:** LLMs are famously bad at multi-step math and logic because they try to "predict" the answer instantly. Chain-of-Thought is the "scratchpad" for the AI. By forcing it to write out its reasoning, you aren't just getting better transparency—you're literally making the model smarter by giving it a mathematical "memory" for its own intermediate steps.

---

## What You'll Learn

- The "Zero-Shot CoT" effect: Why "Let's think step by step" works
- How auto-regressive decoding creates a "working memory" in the context window
- Implementing CoT to handle complex math, logistics, and reasoning puzzles
- The trade-offs between accuracy, latency, and token cost
- Extracting clean answers from long-winded reasoning chains

---

## Theory & Intuition

### The "Paper and Pencil" Effect

Imagine doing the multiplication `982 x 14` in your head vs. on a piece of paper. You'll likely fail mentally but succeed on paper. LLMs are the same. 

```mermaid
graph TD
    subgraph No_CoT["Without CoT (Mental Math)"]
        Q1[Question] --> LLM1[LLM Layer]
        LLM1 --> Ans1[Predicted Answer - High chance of error]
    end
    
    subgraph CoT["With CoT (The Scratchpad)"]
        Q2[Question] --> R1[Reasoning Step 1]
        R1 --> R2[Reasoning Step 2]
        R2 --> R3[Reasoning Step 3]
        R3 --> Ans2[Final Answer - Verified by logic]
    end
    
    style No_CoT fill:#fff,stroke:#333
    style CoT fill:#f9f,stroke:#333
```

**Why it works:** Since the AI predicts the *next* token based on *all previous* tokens, writing out "Step 1: 100 - 20 = 80" puts the intermediate result `80` into its context window. It no longer has to remember it; it is right there in the "script."

---

## 💻 Code & Implementation

### Solving Logistics Puzzles with Step-by-Step Logic

This script demonstrates how to force the model to reason through a multi-step inventory problem.

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_cot_demo():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel('gemini-2.5-flash')

    # A complex multi-step inventory problem
    problem = """
    A warehouse has 100 units of 'AI Chips'. 
    1. They send 20 units to a client. 
    2. The client returns 5 of those units.
    3. The warehouse sells HALF of their current stock in a flash sale.
    4. They receive a new shipment of 10 units.
    How many units are in the warehouse now?
    """

    # THE CoT PROMPT: We demand the thinking process.
    prompt = f"""
    Solve the inventory problem below. 
    IMPORTANT: Think through this STEP-BY-STEP. List your calculations for each step level.
    End your response with 'Final Result: [number]'.
    
    Problem: {problem}
    """

    print("Running Chain-of-Thought (CoT) Demo...")
    response = model.generate_content(prompt)
    
    print("-" * 50)
    print(response.text.strip())
    print("-" * 50)

if __name__ == "__main__":
    run_cot_demo()
```

---

## When NOT to Use Chain-of-Thought

- **Real-Time Latency Sensitivity:** CoT generates many more tokens, which significantly increases the time a user has to wait.
- **Simple, Direct Tasks:** Tasks like "Translate to French" or "Correct my grammar" don't benefit from hidden reasoning.
- **Strict Budget Constraints:** You pay for every word of "thinking" the model writes. If you only care about the answer, CoT is up to 10x more expensive.

---

## Interview Questions & Model Answers

**Q: Explain the "Zero-Shot CoT" phenomenon.**
> **Answer:** Zero-shot CoT was discovered in a famous paper where researchers found that simply appending the phrase "Let's think step by step" to a prompt dramatically improved performance on math benchmarks, even without providing any manual examples. It activates the model's latent reasoning capabilities.

**Q: How do you handle "Hallucinated Reasoning" in CoT responses?**
> **Answer:** This often happens in smaller models where the "thinking" looks logical but 1+1 equals 3. Solution: Use "Self-Consistency" (Topic 28), where you generate 5 CoT responses at a high temperature and pick the "Final Result" that appears most often.

**Q: Why is CoT considered an "In-Context" reasoning technique?**
> **Answer:** Because it doesn't require fine-tuning or weight updates. It relies purely on the model's ability to attend to its own previously generated tokens (the reasoning steps) to inform its final prediction.

---

## Quick Reference

| Feature | Standard Response | Chain-of-Thought |
|---|---|---|
| **Accuracy** | Lower for logic/math | Higher (50-80% improvement) |
| **Latency** | Low (Fast) | High (Needs to "write" more) |
| **Token Cost** | Cheap | Expensive (Pays for reasoning) |
| **Best For** | Fact retrieval, chat | Math, Logic, Multi-step plans |
| **Trigger phrase** | "What is..." | "Think step-by-step..." |
