# Topic 19: Context Management - Handling AI Memory

## 1. Scenario: The "Goldfish Assistant"
You are chatting with an AI about a long legal contract. 
- **Message 1:** "Who are the parties in this contract?" -> AI answers correctly.
- **Message 40:** "And which one of them is responsible for the insurance?" 
- **The Problem:** By message 40, the AI has "forgotten" the contract because the previous 39 messages filled up its **Context Window**. To the AI, the contract was pushed out of its brain.

## 2. The Concept: The Context Window
Every LLM has a "hard limit" on how much text it can process at once (measured in tokens).
- **Gemini 1.5 Flash:** ~1 Million tokens (huge!)
- **Gemma/GPT-3.5:** ~8k - 32k tokens (small)

**Context Management** is the art of choosing *exactly* what to send in that window to get the best result without running out of space or spending too much money.

### Key Context Patterns:

1.  **Sliding Window / Buffer:**
    *   Only send the last 10 messages of the conversation.
    *   **Pros:** Keeps costs low. **Cons:** AI forgets early messages.

2.  **Summarization Memory:**
    *   As the chat gets long, an LLM summarizes the first 20 messages into a short paragraph and prepends it to the new prompt.
    *   **Pros:** Maintains long-term context compactly.

3.  **The "Lost in the Middle" Phenomenon:**
    *   Research shows LLMs are great at processing info at the very *beginning* and very *end* of a prompt, but can ignore info buried in the middle.
    *   **Solution:** Put the most important context (the retrieved RAG chunks) right before the user question.

## 3. Workflow Diagram (Text)
[User History] + [Retrieved Chunks] + [System Instruction] -> [Token Count Check] -> [Truncation/Summarization] -> [Final LLM Prompt]

## 4. Token Management Tips
- **Pruning:** Remove redundant sentences from RAG chunks.
- **Filtering:** Only include the highest-scoring search results.
- **System Instructions:** Keep instructions concise to save tokens for data.

## 5. Interview Corner

1. **"What is a 'Token' in LLM context?"**
   * Answer: A token is a fragment of a word (e.g., "apple" is 1 token, "friendship" might be 2). Roughly, 1,000 tokens ≈ 750 words. Models are billed and capped based on tokens, not characters.

2. **"How do you handle a conversation that exceeds the 1-million-token limit?"**
   * Answer: Even with huge windows, processing 1 million tokens is slow and expensive. I would use "Vector Memory" (Topic 17) to store old messages and only "search" for relevant past interactions instead of sending everything.

3. **"What is 'Windowing' in long documents?"**
   * Answer: It's the practice of breaking a long document into overlapping sections so the model can process segments without losing the "thread" of the narrative.

4. **"Why should I care about context management if Gemini 1.5 has a massive window?"**
   * Answer: **Latencey and Cost.** Processing 1 million tokens takes significantly longer than 1,000. For a fast UI, you want the smallest context that still provides a perfect answer.
