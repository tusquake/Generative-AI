# Topic 7: Few-shot Prompting - Structured Examples

## 1. Scenario: The Dashboard Data Problem

You are building an AI logic for a customer service dashboard. The dashboard code expects data in a very specific JSON format: `{"sentiment": "xxx", "confidence": 0.xx}`.

**The Problem:**
If you just tell the AI to "Return JSON," it might occasionally add extra words or use capitalized labels (e.g., `Sentiment`). This causes your dashboard to crash because it can only read the exact format you programmed.

To solve this, we give the model 3-5 "shots" (examples) so it understands the pattern perfectly.

## 2. Implementation: The Show-and-Tell Script

This script demonstrates how to "force" a specific format using examples.

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_few_shot_demo():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    # The Few-Shot Prompt: Providing a clear pattern for the model to follow
    prompt = """
    Extract sentiment and confidence from the review. Respond with ONLY valid JSON.

    Input: "This is the best purchase I have ever made!"
    Output: {"sentiment": "positive", "confidence": 0.98}

    Input: "The product is fine, but the box was crushed."
    Output: {"sentiment": "mixed", "confidence": 0.75}

    Input: "I hate this company. Never buying again."
    Output: {"sentiment": "negative", "confidence": 0.99}

    Input: "Where is my order? It has been three weeks."
    Output: 
    """

    print("Sending few-shot prompt...")
    response = model.generate_content(prompt)
    
    print("-" * 40)
    print(f"AI Response: {response.text.strip()}")
    print("-" * 40)

if __name__ == "__main__":
    run_few_shot_demo()
```

## 3. Concept Breakdown

### The "Pattern Matching" Brain
Large Language Models are essentially giant pattern-matching machines. If you show them:
`A -> B`
`C -> D`
`E -> ?`
They will almost always provide `F`.

- **Input/Output Mapping:** By providing clear labels like `Input:` and `Output:`, you create a structure that the model can easily latch onto.
- **Consistency:** Few-shot prompting is the single best way to ensure the model uses the same words (like "positive" vs "happy") every time.

**Why this matters for Engineers:**
In production, you often have a "Pipeline." One step's output is the next step's input. If the format changes even slightly, the whole pipeline breaks. Few-shot is your best tool for "Format Insurance."

## 4. Interview Corner

1. **"What is 'In-Context Learning'?"**
   * Answer: It's the formal term for Few-shot prompting. It refers to the model's ability to learn how to do a task based only on the examples provided in the prompt, without being retrained.

2. **"Does adding more examples always make the model more accurate?"**
   * Answer: No. There is a point of "diminishing returns." Usually, 3-5 examples are enough. Adding 50 examples will mostly just make the request slower and more expensive without helping the accuracy much.

3. **"What is the risk of using biased examples in few-shot prompting?"**
   * Answer: If all your examples show a specific bias (e.g., all your 'Positive' examples are about food), the model might struggle to identify 'Positive' sentiment in non-food reviews.

4. **"How do few-shot examples affect your token budget?"**
   * Answer: Every word in your examples counts as an input token. You are charged for those tokens on every single API call. This is why you should keep your examples short and meaningful.

5. **"What is a 'Reasoning Shot'?"**
   * Answer: It's an example where you don't just give the answer, but you show the "thinking process" (e.g., Input -> Step 1 -> Step 2 -> Output). This helps the model solve complex logic problems.

## 5. Practical Insight

- **Ordering Matters:** Sometimes the model is biased toward the *last* example you gave. Make sure your samples are in a random order.
- **Diversity:** If your task is sentiment analysis, give one Positive, one Negative, and one Mixed example. Don't just give three Positives.
- **When NOT to use:** If you are using a very smart model (like GPT-4) for a very common task (like title generation), Zero-shot is often enough. Save your tokens!
