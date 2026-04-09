# Topic 16: RAG Fundamentals (Retrieval Augmented Generation)

## 1. Scenario: The Corporate Knowledge Bot

You want to build an AI that knows everything about your company's proprietary 2024 tax strategy.
- **The Problem:** The AI's training cut off in 2023. It doesn't know your specific strategy. 
- **The Solution:** RAG. When the user asks a question, the system finds the relevant paragraphs in your PDF, adds them to the prompt, and says: "Answer using only this text."

## 2. The Concept: Retrieval vs. Generation

RAG consists of two distinct phases:
1. **Retrieval:** Searching your database for the right "context."
2. **Generation:** Passing that context to the LLM to write the final answer.

**The "Grounding" Effect:** 
By forcing the model to cite its sources from the retrieved context, you nearly eliminate "Hallucinations."

## 3. Workflow Diagram (Text)
User Query -> Search Database -> Found Context -> [Context + Query] -> LLM -> Grounded Answer.

## 4. Interview Corner

1. **"What is the difference between RAG and Fine-tuning?"**
   * Answer: RAG is like giving the model an open-book exam (up-to-date, easy to change). Fine-tuning is like teaching the model a new language or style (static, expensive).

2. **"How does RAG help with data privacy?"**
   * Answer: You don't send your whole database to the AI. You only send the specific 2-3 paragraphs needed for a single query.

3. **"Is RAG better for large datasets?"**
   * Answer: Yes. You can have millions of documents. The LLM only ever "sees" what the retrieval system finds.
