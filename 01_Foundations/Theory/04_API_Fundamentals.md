# Topic 4: API Fundamentals - Calling LLMs and Managing Costs

## 1. Scenario: Scaling the Newsroom

Imagine you are a developer at a news startup. Initially, you had 10 beta testers, and everything was fine. But this morning, your app went viral, and you now have 10,000 users.

**The Problem:**
1. Your API costs are skyrocketing.
2. The AI is taking a long time to respond, making the app feel slow.
3. Your backend is crashing because the AI provider is telling you to "slow down" (Rate Limits).

You need to move from "hobbyist" code to "production-grade" API handling.

## 2. Implementation: The Production-Ready Call

This script demonstrates how to call an LLM while calculating cost and handling potential errors.

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

def production_api_call():
    # Setup
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Explain how a microwave works in two sentences."
    
    start_time = time.time()
    
    try:
        # Call the API
        response = model.generate_content(prompt)
        end_time = time.time()
        
        # Track Usage
        usage = response.usage_metadata
        in_tokens = usage.prompt_token_count
        out_tokens = usage.candidates_token_count
        
        # Calculate Cost (Approx rates for Gemini 1.5 Flash)
        # $0.075 per Million input tokens / $0.30 per Million output tokens
        cost = (in_tokens * 0.000000075) + (out_tokens * 0.00000030)
        
        print(f"Response: {response.text.strip()}")
        print("-" * 40)
        print(f"Latency: {end_time - start_time:.2f} seconds")
        print(f"Cost: ${cost:.6f}")
        print(f"Total Tokens: {in_tokens + out_tokens}")
        print("-" * 40)

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    production_api_call()
```

## 3. Concept Breakdown

### The Restaurant Analogy
LLM APIs are not like standard databases. They are like ordering at a high-end restaurant.
- **The Order (Input Tokens):** You pay for the chef to read your order.
- **The Meal (Output Tokens):** You pay for the chef to cook the meal. This is usually more expensive.
- **The Queue (Rate Limit):** If too many people order at once, the kitchen stops taking new orders (Error 429).

**Why this matters:**
In production, every "word" has a price. If you don't track your token usage, you might get a massive bill at the end of the month.

**The #1 Mistake:**
**Not setting timeouts.** LLMs can sometimes take 30+ seconds to respond. If your server waits forever, it will hang and crash for all users.

## 4. Interview Corner

1. **"How do you handle a 429 (Rate Limit) error in code?"**
   - Answer: We use Exponential Backoff. We wait 1 second, then 2, then 4, before trying again. This gives the API provider time to "breathe" without overwhelming them.

2. **"Why is Cost Tracking important at the app level?"**
   - Answer: LLM providers bill you in bulk. Without app-level tracking, you don't know which specific feature or user is costing you the most money.

3. **"What is the difference between Synchronous and Streaming calls?"**
   - Answer: Synchronous waits for the whole answer. Streaming gives you the answer word-by-word. Streaming is essential for a good user experience so they don't stare at a loading spinner.

4. **"How do you reduce costs without switching to a different model?"**
   - Answer: Prompt Compression. You remove unnecessary words from your instructions to make the "Input" as small as possible.

5. **"What is a 'Cold Start' in the context of LLM APIs?"**
   - Answer: The first request to a model can sometimes be slower as the provider "wakes up" the specialized hardware (TPU/GPU) to handle your request.

## 5. Practical Insight

- **Caching:** If two users ask the same question, save the answer in Redis! Don't pay for the same AI response twice.
- **Monitoring:** Always log the "Latency per Token". It tells you how fast your AI "types" for your users.
- **When NOT to use:** Don't use a high-powered LLM for a task that a simple regex or 10 lines of Python can solve.
