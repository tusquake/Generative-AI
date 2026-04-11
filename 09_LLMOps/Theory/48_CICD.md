# 48. CI/CD for LLM Applications

> **Mentor note:** Standard software breaks when you change a line of code. AI software breaks when you change a single word in a prompt (Topic 36). **CI/CD for LLMs** is about automating the testing of your prompts and models. Every time you push code, an "Evaluation pipeline" should run 50 Judge-based tests (Topic 40) to ensure your "better" prompt doesn't secretly break 20 other use-cases.

---

## What You'll Learn

- The Evaluation Pipeline: Automated grading on every Commit
- Regression Testing for Prompts: Preventing "Prompt Drift"
- A/B Testing & Canary Deploys: Safely rolling out new models
- Dataset Management: Versioning your "Golden Sets"
- Shadow Deployments: Running a new model in the background against live data

---

## Theory & Intuition

### The Continuous Evaluation Loop

Unlike traditional CI (where you check for syntax), AI CI checks for **Semantic Quality**. You run your new prompt against a "Golden Set" and check if the Judge's score (Topic 40) remains high.

```mermaid
graph TD
    Git[Developer: git push] --> CI[CI Runner: GitHub Actions]
    CI --> Test[Run LLM-as-a-Judge Tests]
    
    subgraph Eval_Gate["The Quality Gate"]
        Test --> Pass{Score > 0.8?}
        Pass -->|Yes| Deploy[Deploy to Production]
        Pass -->|No| Fail[Alert: Regression Detected]
    end
    
    Deploy --> Shadow[Shadow Mode: Test on 5% live traffic]
    
    style Eval_Gate fill:#f9f,stroke:#333
    style Deploy fill:#dfd,stroke:#333
```

**Why it matters:** Safety. Without automated CI, you are just "guessing" if your prompt change is better. Automated evaluation gives you a mathematical "Quality Bar" that must be passed before any code touches the user.

---

## Deployment Strategies

| Strategy | How it works | Risk Level |
|---|---|---|
| **Direct Rollout** | Replace model immediately | High |
| **Canary** | Give 10% of users the new model | Low |
| **Shadow** | New model runs in parallel; result is hidden | **Zero** |
| **A/B Test** | Compare metrics (e.g., conversion) for both | Controlled |

---

## 💻 Code & Implementation

### A Basic Regression Test Script (Concept)

```python
import os

def run_regression_tests():
    # Golden Set: Inputs where we KNOW what the answer should look like
    golden_set = [
        {"input": "Hi", "expected": "Helpful Greeting"},
        {"input": "Reset my password", "expected": "Security Auth Link"}
    ]
    
    print("Starting CI Evaluation Pipeline...")
    
    for test in golden_set:
        # 1. Run the new prompt
        # response = call_llm(test['input'])
        
        # 2. Run the Judge to compare
        # score = judge_model(response, test['expected'])
        
        score = 0.95 # Simulated
        print(f"Test '{test['input']}': Score {score}")

    if score > 0.8:
        print("CI SUCCESS: Prompt quality maintained.")
    else:
        print("CI FAIL: Potential regression in response quality.")

if __name__ == "__main__":
    run_regression_tests()
```

---

## Interview Questions & Model Answers

**Q: What is 'Shadow Deployment' in LLMOps?**
> **Answer:** It's when you deploy a new model or prompt but don't show its results to the user. Instead, the system sends every user query to both the old "Live" model and the "Shadow" model. We then compare the outputs using a Judge model. If the shadow model performs better over 1,000 real requests, we "promote" it to live production.

**Q: Why is 'Versioning' prompts as important as versioning code?**
> **Answer:** Because prompts are effectively "Source Code" that dictates the AI's behavior. If you change a prompt without versioning it, and the AI starts making mistakes, you have no way to "Rollback" to the previous working version. I store prompts in separate `.txt` or `.yaml` files in Git.

**Q: How do you handle 'Non-Deterministic' tests in CI?**
> **Answer:** Since LLMs can give slightly different answers even for the same input, we don't use "Exact Match" tests. Instead, we use **Statistical Passing**. A test only "Fails" if the Judge's average score across 5 runs drops below a specific threshold (e.g., 80%).

---

## Quick Reference

| Term | Role |
|---|---|
| **Golden Set** | The curated list of test cases that must always work |
| **Regression** | When a change makes an existing feature worse |
| **Judge** | The model that automates your CI testing |
| **Rollback** | Reverting to a previous model version |
| **Metadata** | Tagging traces with the specific Prompt Version |
