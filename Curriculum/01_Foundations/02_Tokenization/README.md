# Topic 2: Tokens, Context Windows, and how LLMs "read"

## 1. Scenario: The "Currency" of AI

Imagine you are running a translation service. You notice that translating a 500-word article from English to Spanish is cheap, but translating the same article into a rare dialect is twice the price.

**The Problem:**
Model providers (OpenAI, Google, Anthropic) don't bill you by the word or the character. They bill you by the **Token**. If you don't understand how tokens work, you can't predict your costs or your model's limits.

## 2. Implementation: Seeing the "Chunks"

This script shows exactly how text is "chopped up" into pieces the model can understand.

```python
import tiktoken

def explore_tokens():
    # A mix of common words, rare words, and symbols
    text = "AI is amazing! Pomegranate is a long word."
    
    # Standard tokenizer used by GPT models
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # Convert text -> IDs
    tokens = encoding.encode(text)
    
    print(f"Original: {text}")
    print(f"Token Count: {len(tokens)}")
    print("-" * 30)

    # Decode back to see the individual pieces
    print(f"{'CHUNK':<15} | {'ID'}")
    for t_id in tokens:
        chunk = encoding.decode([t_id])
        print(f"'{chunk}':<15 | {t_id}")

if __name__ == "__main__":
    explore_tokens()
```

## 3. Concept Breakdown

### The "Lego Brick" Analogy
Think of text as a pre-built house. 
- **Characters** are individual grains of sand (Too small to work with).
- **Words** are whole rooms (Too specific—what if you want a room that doesn't exist yet?).
- **Tokens** are **Lego Bricks**. You have a standard set of bricks that can build *anything*. 

Common bricks (like "the", "and") are large pieces. Rare bricks (like "pomegranate") might need three or four smaller pieces to build.

**Why it matters:**
1.  **The Context Window:** This is the size of the "bucket" the model can hold. If your bucket holds 128,000 tokens, and you try to pour in 130,000, the "oldest" tokens spill out and are forgotten.
2.  **Multilingual Cost:** Some languages are "chunkier." English is very efficient in most tokenizers. Japanese or Hindi often require more tokens for the same meaning, making them more expensive to process.

**The #1 Mistake:**
Assuming **1 Word = 1 Token**. 
*Rule of thumb:* 1,000 tokens ≈ 750 words. Always budget for 25-30% more tokens than you have words.

## 4. Interview Corner

1. **"Why do some words take multiple tokens while others take only one?"**
   *   *Answer:* Tokenizers use frequency. Words like "the" appear billions of times, so they get one unique ID. Rare words or complex medical terms are split into smaller sub-words (like 'append' + 'icitis') to save space in the model's vocabulary.

2. **"What happens when a conversation exceeds the 'Context Window'?"**
   *   *Answer:* Most systems use a 'Sliding Window'. They simply drop the oldest messages to make room for new ones. If you don't handle this yourself, the model might "forget" its original instructions or the user's name.

3. **"How does the number of tokens in a response affect speed (latency)?"**
   *   *Answer:* LLMs are auto-regressive, meaning they generate one token at a time. If a model generates 10 words that equal 20 tokens, it takes twice as long as 10 words that equal 10 tokens. Token count is the primary driver of response time.

4. **"Why should you count tokens on the server-side before calling an API?"**
   *   *Answer:* To prevent 'Runaway Costs' and 'Context Overflows'. By counting tokens locally (using libs like `tiktoken`), you can reject a prompt that is too long *before* you pay the API provider for a failed or truncated request.

5. **"Why is 'pomegranate' more expensive to process than 'apple'?"**
   *   *Answer:* 'Apple' is a very common token (1 token). 'Pomegranate' is rarer and might be split into 3 tokens (`pome` + `gran` + `ate`). You pay for the 3 tokens, even though it's just one word.

## 5. Practical Insight

- **Cost Control:** If you are building a production app, set a `max_tokens` limit on every request. This acts as a "circuit breaker" to stop the model from writing a 10-page essay when you only wanted a 1-sentence summary.
- **Latency:** Streaming (Topic 39) helps mitigate the "wait time" for tokens, but the total time taken is always proportional to the token count.
- **When NOT to use:** If you're just measuring the length of a string for UI layout (like "Is this text too long for the button?"), use character count. Tokenizers are for AI logic and billing only.
