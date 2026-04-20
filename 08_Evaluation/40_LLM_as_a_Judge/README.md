# LLM-as-a-Judge (Self-Evaluation)

> **Mentor note:** How do you test a model that generates creative text? You can't use simple string matching. If the AI says "The sky is azure" and the ground truth is "The sky is blue," a computer says it's 0% correct, but a human says it's 100% correct. **LLM-as-a-Judge** is the pattern where we use a larger, more capable model (like Gemini 1.5 Pro) to act as a "Professor" and grade the responses of smaller models. It is the only way to scale evaluation for Generative AI.

---

## What You'll Learn

- The Evaluator Pattern: Reference-based vs. Reference-free grading
- Scoring Rubrics: Creating clear "Grading Criteria" for the Judge
- Pairwise Comparison: Asking the Judge to pick the better of two outputs
- Frameworks: Ragas (for RAG), DeepEval, and LangSmith
- Mitigation: Handling "Position Bias" and "Verbosity Bias" in Judges

---

## Theory & Intuition

### The Grading Loop

Instead of binary "Right/Wrong," the Judge model provides a **Likert Scale** (1-5) and a **Justification**.

```mermaid
graph TD
    Prompt[User Prompt] --> Student[Student Model: Flash]
    Student --> Answer[Generated Answer]
    
    subgraph Evaluation_Suite["The Judge"]
        Answer --> Judge[Judge Model: Pro]
        Criteria[Rubric: Accuracy, Tone, Safety] --> Judge
        Reference[Ground Truth Answer] -->|Optional| Judge
    end
    
    Judge --> Score[Final Score: 4/5]
    Judge --> Detail[Reason: 'Factually correct but a bit too long.']
    
    style Evaluation_Suite fill:#f9f,stroke:#333
    style Judge fill:#dfd,stroke:#333
```

**Why it matters:** It allows for **Continuous Integration (CI)**. Every time you change your prompt, the Judge automatically re-grades 100 test cases, ensuring your "fix" didn't break something else.

---

## 💻 Code & Implementation

### Implementing an Automated Judge (JSON Output)

This script demonstrates how to use a high-capability model to evaluate a "Student" model's response based on accuracy, tone, and a reference ground truth.

```python
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

def run_automated_judge():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # The "Student" response we are grading
    student_answer = "The capital of France is Paris, which is home to the Eiffel Tower."
    reference_answer = "Paris is the capital of France."

    # The Rubric (Instruction for the Judge)
    judge_prompt = f"""
    You are an expert Professor. Grade the STUDENT ANSWER based on the REFERENCE ANSWER.
    
    CRITERIA:
    1. Accuracy: Is the fact correct? (Scale 1-5)
    2. Tone: Is it professional? (Scale 1-5)
    
    STUDENT ANSWER: {student_answer}
    REFERENCE ANSWER: {reference_answer}
    
    Return ONLY a JSON object: 
    {{"accuracy": 5, "tone": 5, "justification": "..."}}
    """

    print("Evaluating student response...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=judge_prompt
    )
    
    print("-" * 50)
    print(f"REPORT CARD:\n{response.text.strip()}")
    print("-" * 50)

if __name__ == "__main__":
    run_automated_judge()
```

---

## Judge Bias Checklist

| Bias | Problem | Solution |
|---|---|---|
| **Position Bias** | Judge favors the first answer it sees | Swap order and run evaluation twice |
| **Verbosity Bias** | Judge favors longer, wordier answers | Hard constraint on length in rubric |
| **Self-Preference**| Judge favors its own writing style | Use a different provider for the Judge |
| **Numeric Bias** | Judge hates giving "1" or "5" | Use a 3-point scale or binary Pass/Fail |

---

## Interview Questions & Model Answers

**Q: Why use LLM-as-a-Judge instead of BLEU or ROUGE scores?**
> **Answer:** BLEU and ROUGE are based on N-gram overlaps (word matching). They can't understand synonyms. An LLM-as-a-Judge understands that "Azure" and "Blue" mean the same thing, avoiding false penalties.

**Q: What is 'Reference-Free' Evaluation?**
> **Answer:** It's when the Judge grades a response without knowing the "Correct" answer. This is useful for creative writing or open-ended reasoning where there is no single "Golden" answer.

---

## Quick Reference

| Term | Role |
|---|---|
| **Rubric** | The specific rules the Judge must follow |
| **Golden Set** | A curated table of "Perfect" Q&A pairs |
| **RAGAS** | A framework specifically for grading RAG pipelines |
| **Hallucination Rate**| How many times the Judge flags a factual error |
