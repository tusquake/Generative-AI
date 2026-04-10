# Topic 3: Sampling parameters - Temperature, Top-p, Top-k, max_tokens

## 1. Scenario: The Creative vs. The Factual

Imagine you are building two different apps:
1. A "Sci-Fi Story Writer" that needs to surprise the reader with unexpected plot twists.
2. A "Medical Dosage Calculator" that must be 100% consistent and never take risks.

You are using the exact same LLM for both. How do you make one creative and the other incredibly strict? You use Sampling Parameters.

## 2. Implementation: Testing Temperature

This script demonstrates how changing the "heat" of the model changes its output.

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_sampling():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "The most interesting thing about space is..."

    # 1. Low Temperature (The "Safe" choice)
    config_low = genai.types.GenerationConfig(temperature=0.1)
    
    # 2. High Temperature (The "Creative" choice)
    config_high = genai.types.GenerationConfig(temperature=1.0)

    print("--- Low Temp (0.1) ---")
    print(model.generate_content(prompt, generation_config=config_low).text)
    
    print("\n--- High Temp (1.0) ---")
    print(model.generate_content(prompt, generation_config=config_high).text)

if __name__ == "__main__":
    test_sampling()
```

## 3. Concept Breakdown

### The Dice Analogy (Temperature)
LLMs choose words by calculating probabilities (e.g., "mat" is 80% likely, "moon" is 5%).
- Temperature 0.0: The model always picks the word with the highest probability.
- Temperature 1.0: The model picks words proportional to their probability.
- Temperature 2.0: The model starts giving chance to even the most unlikely words.

### Top-K vs. Top-P: The Concrete Example
Imagine the model is predicting the next word for: "The capital of France is..."
Scores: Paris (94%), Lyon (2%), Marseille (1%), London (0.5%), Bread (0.1%).

- Top-K = 3 (Fixed Count):
  Always takes the top 3 words: [Paris, Lyon, Marseille].
- Top-P = 0.95 (Dynamic Threshold):
  Adds scores until they hit 0.95. 
  Paris (94%) is not enough. Adding Lyon (2%) makes it 96%.
  The pool stops at [Paris, Lyon]. Marseille is excluded because the threshold was already hit.

Why this matters: Top-P adapts. If the model is sure, the pool is small. If the model is confused, the pool grows.

## 4. Interview Corner

1. "Why use Top-P instead of Top-K?"
   * Answer: Top-P is dynamic. It adjusts the number of candidate words based on how confident the model is. Top-K is a rigid limit that might include nonsense words if the fixed number is too high.

2. "Does a high temperature increase the cost of a request?"
   * Answer: No. It doesn't change the number of tokens, only which tokens are chosen.

3. "What happens if you set temperature to 0.0 in a production chatbot?"
   * Answer: The bot becomes very predictable and repetitive. This is good for technical tasks but bad for natural conversation.

4. "How does 'max_tokens' affect the model's behavior?"
   * Answer: It is a hard cutoff. If the model hits the limit mid-sentence, the response just stops.

5. "Describe a scenario where you would use a Temperature of 0.8 but a Top-P of 0.1."
   * Answer: Top-P 0.1 will likely force the model to pick only the single most likely word, making the high temperature irrelevant.

## 5. Practical Insight

- The Sweet Spot: Most bots use temperature=0.7 and top_p=0.9.
- Safety: Always set a max_tokens limit to prevent runaway costs.
- When NOT to use: Don't use high temperature when outputting structured data like JSON, as it might hallucinate incorrect brackets or quotes.
