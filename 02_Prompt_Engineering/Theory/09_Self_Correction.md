# Topic 9: Self-Correction - Asking the Model to Catch Its Own Errors

## 1. Scenario: The Overconfident Coder

You are using AI to write a Python script that reads a CSV file and calculates a sum.

**The Problem:**
AI often writes "Happy Path" code. It ignores what happens if the file is missing, if the numbers are actually strings, or if the file is 10GB large. 

**Self-Correction** allows the AI to "Review" its own code and add the safety nets it forgot.

## 2. Implementation: The Code Review Pattern

This script shows how to trigger a "Self-Critique" to graduate from "Junior" to "Senior" output.

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_self_correction_demo():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Step 1: The "Naive" Request
    task = "Write a Python function to read 'data.txt' and print each line."
    
    print("STEP 1: Getting Initial (Naive) Answer...")
    response_1 = model.generate_content(task)
    initial_code = response_1.text
    print("-" * 30 + " INITIAL CODE " + "-" * 30)
    print(initial_code.strip())

    # Step 2: The Self-Correction Prompt
    # We ask the model to act as a CRITIC
    critique_prompt = f"""
    You are a Senior Security Engineer. Review the Python code below for:
    1. Error handling (what if the file doesn't exist?)
    2. Resources (does it close the file properly?)
    3. Performance (is it efficient for large files?)

    Code to review:
    {initial_code}

    Provide an IMPROVED version of the code that fixes these issues.
    """

    print("\n\nSTEP 2: Running Self-Correction...")
    response_2 = model.generate_content(critique_prompt)
    
    print("-" * 30 + " CRITIQUE & IMPROVED CODE " + "-" * 30)
    print(response_2.text.strip())

if __name__ == "__main__":
    run_self_correction_demo()
```

## 3. Concept Breakdown

### The "Double-Check" Loop
When a model generates text, it's just predicting the next most likely token. It doesn't actually "know" it made a mistake until it reads the mistake.
By feeding the mistake back into the model as input, you allow the model to process its own output as if it were someone else's work.

- **Objective Criticism:** Models are often better critics than they are creators.
- **Improved Safety:** This is the primary way we prevent "hallucinations" in production—we ask a second model (or the same one) to verify the data.

**Why this matters for Engineers:**
Manual testing is slow. You can build "Self-Correcting Pipelines" where the AI validates its own JSON, checks its own code for syntax errors, and retires until it passes a high bar.

## 4. Interview Corner

1. **"Why is a model often able to correct an error it just made?"**
   * Answer: Because the "Reasoning" capability required to detect a pattern violation is different from the "Generation" capability. When reviewing, the model's objective is shifted to pattern matching against rules rather than creative creation.

2. **"Does Self-Correction increase the cost of your application?"**
   * Answer: Yes. You are essentially paying for two or more API calls instead of one. You must decide if the increased accuracy is worth the 2x cost.

3. **"What is 'Zero-Shot' Self-Correction?"**
   * Answer: It's simply adding "Check your work for errors and redo it if necessary" to the end of a single prompt.

4. **"How do you prevent the AI from being 'too critical' and changing correct code?"**
   * Answer: Give the AI strict criteria. Instead of "Fix this code," say "Fix this code ONLY if it has a security vulnerability or a performance bottleneck."

5. **"Can you use a smaller, cheaper model to correct a larger model?"**
   * Answer: Yes! This is a common pattern. Use a "smart" model (GPT-4) to generate, and a "fast/cheap" model (Gemini Flash) to check for basic formatting or syntax errors.

## 5. Practical Insight

- **The "Second Brain" Pattern:** Many companies use Model A to generate and Model B to verify. This prevents the bias where a model might "agree" with its own mistakes.
- **Iterative Refinement:** You can run this loop 3 or 4 times for extremely critical tasks (like code that will run in production).
- **When NOT to use:** For low-stakes tasks like creative writing or brainstorming where there is no "wrong" answer.
