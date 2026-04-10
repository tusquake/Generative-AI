# Topic 20: Evaluation & Grounding - Trusting the AI

## 1. Scenario: The "Confident Liar"
You ask an AI for your bank balance. 
- **AI Answer:** "Your balance is $42,000." (Confidence: 100%)
- **Reality:** Your balance is $4.20. 
- **The Problem:** The AI "Hallucinated." It generated a realistic-looking number because the prompt didn't force it to check the source data correctly.
- **The Solution:** **Grounding.** We force the AI to say: "According to the last statement on page 3, your balance is $4.20."

## 2. The Concept: Grounding vs. Faithfulness
**Grounding** is the process of linking model output to specific real-world facts or data (usually provided in the prompt context).

### The "RAG Triad" for Evaluation:
To trust a RAG system, we measure three things:

1.  **Faithfulness (Groundedness):** Is the answer derived *only* from the retrieved context? If the context says the sky is green, and the AI says green, it is "Faithful" (even if reality says blue).
2.  **Answer Relevance:** Does the answer actually address the user's question?
3.  **Context Precision:** Did the retrieval system find the *right* information to answer the question?

### Citation & Attribution:
A premium RAG system doesn't just give an answer; it gives **Sources**.
- Example: *"The refund policy is 30 days [Source: FAQ.pdf, Page 12]."*

## 3. Workflow Diagram (Text)
User Query -> Retrieval -> Context -> [LLM + "Answer ONLY using context"] -> Answer + Citations -> [Evaluator Bot checks for Hallucinations]

## 4. Evaluation Metrics & Frameworks
- **RAGAS (RAG Assessment):** A framework that uses an LLM to "grade" your RAG pipeline automatically.
- **G-Eval:** Using a powerful model (like Gemini 1.5 Pro) to act as a judge for a smaller model (like Gemini 1.5 Flash).
- **Human-in-the-loop:** The ultimate test—having experts verify the grounding.

## 5. Interview Corner

1. **"How do you stop an AI from hallucinating?"**
   * Answer: You can't 100% stop it, but you can significantly reduce it by:
     1. Providing the right data (Retrieval).
     2. Using "Negative Constraints" in the prompt (e.g., "If you don't know the answer, say you don't know. Do not make things up.").
     3. Forcing the model to "Cite its sources."

2. **"What is 'Faithfulness' in RAG?"**
   * Answer: It measures how much the LLM's answer is supported by the context. If the LLM uses its personal training data (prior knowledge) instead of the provided context, the faithfulness score drops.

3. **"Is a high RAGAS score enough to go to production?"**
   * Answer: No. Automated metrics are great for iteration, but you always need manual user testing to ensure the AI "vibe" and accuracy meet real-world expectations.

4. **"What is the difference between Verification and Evaluation?"**
   * Answer: Verification is checking if the system meets requirements (e.g., does it respond in under 2 seconds?). Evaluation is checking if the output is *good* (e.g., is the answer correct and helpful?).
