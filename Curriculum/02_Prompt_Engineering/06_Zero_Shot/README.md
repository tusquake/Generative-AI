# Topic 6: Zero-shot Prompting - Capabilities and Failure Modes

## 1. Scenario: The Fresh Product Launch

Imagine you work for a company that just launched a new product. You have thousands of tweets coming in every hour. You need to know if people are happy, mad, or just asking questions.

**The Problem:**
You don't have time to "teach" the AI with a bunch of examples because the product is so new. You need to see if the AI can just "guess" the sentiment correctly using its general intelligence.

## 2. Implementation: No Examples Needed

This script tests the model's ability to categorize text with zero prior training or examples.

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_zero_shot_demo():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    # A tricky review that has both good and bad things
    test_review = "The delivery was fast, but the product arrived broken. Very disappointed."

    # The Zero-Shot Prompt: Instructions ONLY, no examples.
    prompt = f"""
    Categorize the following customer review into one of these labels:
    - Positive
    - Negative
    - Mixed
    - Question

    Review: "{test_review}"
    
    Response:
    """

    print("Analyzing review...")
    response = model.generate_content(prompt)
    
    print("-" * 40)
    print(f"Review: {test_review}")
    print(f"AI Categorization: {response.text.strip()}")
    print("-" * 40)

if __name__ == "__main__":
    run_zero_shot_demo()
```

## 3. Concept Breakdown

### The "Genius Intern" Analogy
Imagine you hire a super-smart intern who has read every book in the world but has never worked at your office. 
- **Zero-Shot** is like asking them: "Hey, categorize these emails." They know what a 'complaint' is in general, so they can do a pretty good job even on their first day without any training.

**Why this matters:**
It's the simplest and cheapest way to use AI. You don't have to gather data or write complex examples.

**Trade-offs:**
- **Gain:** Speed and lower token costs (you aren't paying for examples).
- **Sacrifice:** Consistency. Sometimes the model might use a word you didn't ask for (like "Disgruntled" instead of "Negative") because it wasn't "locked in" by examples.

## 4. Interview Corner

1. **"What does 'Zero-Shot' mean in LLM prompting?"**
   * Answer: It means providing a prompt that contains a task description but zero examples of how to complete that task.

2. **"Why is Zero-Shot prompting cheaper than Few-Shot prompting?"**
   * Answer: Because tokens cost money. By not sending examples in every prompt, you reduce the total number of input tokens, which lowers your bill.

3. **"What is the most common failure mode for Zero-Shot prompted models?"**
   * Answer: Format instability. The model might understand the task but fail to deliver the output in the exact format (like JSON or a single word) that your code expects.

4. **"How can you make a Zero-Shot prompt more reliable?"**
   * Answer: Be extremely explicit with constraints. Use phrases like "Respond with EXACTLY one of these four words" or "Do not provide any explanation."

5. **"When should you move from Zero-Shot to Few-Shot (adding examples)?"**
   * Answer: When the task is subjective, when the output format must be 100% perfect, or when the model is consistently choosing the wrong category for your specific business case.

## 5. Practical Insight

- **The Baseline:** Always start with Zero-Shot. It's your "Control Case."
- **Model Strength Matters:** Huge models (GPT-4, Gemini Pro) are amazing at Zero-Shot. Smaller models (Llama 8B, Phi-3) often struggle and *need* examples to understand what you want.
- **When NOT to use:** For complex logic or math. AI often needs to be "Walked through" a problem with examples before it can do it correctly.
