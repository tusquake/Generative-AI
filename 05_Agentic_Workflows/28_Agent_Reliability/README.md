# Agent Reliability & Self-Consistency

> **Mentor note:** A prototype agent works 80% of the time; a production agent works 99.9% of the time. The gap between them is "Reliability." Because LLMs are probabilistic, they are prone to random failures, infinite loops, and "State Drift." Building for reliability means implementing guardrails, majority voting, and rigorous observability. Every agent you build should have a "Plan B" by default.

---

## What You'll Learn

- Self-Consistency: Reducing randomness via Majority Voting over multiple paths
- The "Guardrail" Pattern: Validating agent actions before execution
- Loop Detection: Preventing infinite "Thought-Action" cycles
- Graceful Degradation: Handling tool failures without crashing the system
- Determinism vs. Stochasticity: Managing `temperature` and `top_p` in agentic loops

---

## Theory & Intuition

### The Swiss Cheese Model of Reliability

No single reliability technique is perfect. Instead, we layer multiple "slices" of defense. If a hallucination passes through one slice, the next guardrail (e.g., self-correction) should catch it.

```mermaid
graph TD
    User[User: Finalize Invoice] --> P1[Plan Step]
    P1 --> G1{Guardrail: PII Check}
    G1 -->|Pass| E1[Execute Tool]
    E1 -->|Error| SC[Self-Correction Loop]
    SC -->|Retry| E1
    E1 -->|Success| V1{Verification: Majority Vote}
    V1 --> Output[Final Reliable Result]
    
    style G1 fill:#ff9999,stroke:#333
    style SC fill:#f9f,stroke:#333
    style V1 fill:#dfd,stroke:#333
```

**Why it matters:** In a business environment, a single "impulsive" error (like deleting the wrong record) is catastrophic. Majority voting ensures that the "consensus" of multiple independent reasoning paths is used, which statistically eliminates common "random" LLM errors.

---

## 💻 Code & Implementation

### Implementing Majority Voting for Logic

This script demonstrates the "Self-Consistency" pattern where we run the same logic task multiple times and take the majority consensus to eliminate one-off reasoning errors.

```python
import os
from collections import Counter
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_reliability_demo():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant
    model_name = "llama-3.1-8b-instant"

    # The Logic Task: A complex math or logic problem prone to one-off slips
    task = "A train leaves at 3pm traveling 60mph. Another at 4pm at 90mph. At what time do they meet?"

    # STRATEGY: Self-Consistency (Run N=3 times)
    results = []
    print(f"Task: {task}")
    print(f"Running 3 independent trials for reliability...")
    
    for i in range(3):
        # We use a higher temperature to allow for diverse reasoning paths
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": task + " Provide the answer as a single time (e.g. 6pm)."}],
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        results.append(answer)
        print(f"Trial {i+1} Output: {answer}")

    # STEP: Consensus / Majority Voting
    occurrence_count = Counter(results)
    final_consensus = occurrence_count.most_common(1)[0][0]

    print("-" * 50)
    print(f"FINAL CONSENSUS: {final_consensus}")
    print("-" * 50)

if __name__ == "__main__":
    run_reliability_demo()
```

---

## Reliability Defense Layers

| Layer | Technique | Goal |
|---|---|---|
| **Pre-Action** | Input Sanitization | Block malicious or nonsensical queries |
| **Intra-Action**| Loop Detection | Stop the agent if it's "spinning its wheels" |
| **Post-Action** | Output Verification | Ensure the JSON matches the expected schema |
| **Cross-Model** | Judge Agent | Use a larger model to grade a smaller model |

---

## Interview Questions & Model Answers

**Q: What is "Self-Consistency" and how does it differ from standard CoT?**
> **Answer:** Chain-of-Thought (CoT) provides a single path of reasoning. Self-Consistency generates *multiple* independent CoT paths and takes the majority vote. This catches "calculation slips" where the model understands the logic but makes a small mistake in a single turn.

**Q: How do you handle an agent that enters an "Infinite Loop"?**
> **Answer:** I implement two triggers: 1. A global `max_turns` limit. 2. A **Repetition Detector** that hashes tool calls; if the hashes repeat, the system forces a reset or asks for human intervention.

**Q: Why is "Graceful Degradation" important for enterprise AI?**
> **Answer:** Enterprise systems depend on external APIs. If a tool call fails, the agent must not hallucinate a fake result. It should retry with an exponential backoff or report the specific error to the user.

---

## Quick Reference

| Term | Role |
|---|---|
| **Guardrails** | Rules that block unsafe or invalid actions |
| **Majority Vote** | Using multiple runs to find the "Truth" |
| **Non-Deterministic**| AI potentially giving different answers every time |
| **Self-Correction** | The model fixing its own error after a feedback loop |
| **Backoff** | Waiting before retrying a failed tool call |
