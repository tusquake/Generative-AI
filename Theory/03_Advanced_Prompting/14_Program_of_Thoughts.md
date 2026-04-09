# Topic 14: Program-of-Thoughts (PoT) - Delegating Math to Code

## 1. Scenario: The Interest Rate Disaster

You are building a Financial Advisor AI. A client asks: *"I have $500. I add $50 every month for 5 years at a 5.5% annual interest rate. How much do I have at the end?"*

**The Problem:**
If you ask an LLM to solve this, it will likely:
- Miscalculate the compound interest.
- Round numbers incorrectly at every step.
- Make a human-like arithmetic error.

**Program-of-Thoughts** solves this by asking the AI to write a Python script to do the math.

## 2. The Concept: Python as the Backbone

In PoT, the AI's "Thought Process" is the **Code**. 
- LLMs are 100x better at writing Python than they are at doing mental math. 
- A computer is 1,000,000x better at running Python than a human (or an AI) is at doing long multiplication.

**Why this matters for Engineers:**
Instead of trying to "fine-tune" a model to be better at math, you just give it a calculator (Python). This is the secret behind tools like ChatGPT's "Advanced Data Analysis."

## 3. The PoT Workflow

1. **User asks a question.**
2. **AI writes the solution as Code.**
3. **Your Application executes the code** (ideally in a safe sandbox).
4. **The Code's output is shown to the user.**

## 4. Interview Corner

1. **"What is the main risk of Program-of-Thoughts?"**
   * Answer: **Security.** If you allow an AI to generate code and run it, it might try to delete files or access environment variables. You must use a "Sandbox" (e.g., a locked-down Docker container) to run the code.

2. **"Is PoT faster than normal prompting?"**
   * Answer: No. It involves generating code, shipping it to an executor, waiting for a result, and sending it back. It is slower but infinitely more accurate for math.

3. **"Can PoT help with non-math tasks?"**
   * Answer: Yes! Sorting lists, manipulating large strings, or parsing huge JSON objects are all things Python handles better than a raw LLM.

4. **"What happens if the generated code has a bug?"**
   * Answer: You catch the error and send it back to the AI (Self-Correction) saying "This code failed with [Error]. Please fix it."

5. **"Can small models do PoT?"**
   * Answer: Surprisingly, yes. Many 7B models (like Mistral/Llama-3) are highly trained on code and can write simple PoT scripts even if they aren't 'smart' enough for complex logic.

## 5. Practical Insight

- **The 'Main' Function:** Always ask the model to put its result in a specific variable or print it out clearly so your execution script can find it.
- **Python Standard Library only:** Tell the model to "Only use the Python standard library" to avoid it trying to import `pandas` or `numpy` if you haven't installed them in your sandbox.
- **When NOT to use:** For creative writing, summarization, or simple facts. Use it only when the "Logic" can be expressed mathematically or algorithmically.
