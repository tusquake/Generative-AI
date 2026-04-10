# Topic 13: Directional Stimulus Prompting (DSP) - Guiding with Hints

## 1. Scenario: The Specialized Summarizer

You are building an AI tool for a Legal firm. They have 50-page contracts, but different lawyers care about different things. 
- **Lawyer A** only cares about "Liability and Indemnity."
- **Lawyer B** only cares about "Payment Milestones."

**The Problem:**
Generic summaries are too broad. If you ask for a "summary," it tries to cover everything, and misses the deep details the specific lawyer needs.

**Directional Stimulus Prompting** gives the model a "Hint" or "Focus Area" to guide its attention.

## 2. The Concept: The Spotlight

DSP is like putting a spotlight on a specific part of a dark room. 
The room (the input text) is full of information, but the "Stimulus" tells the AI: *"Look here, ignore the rest."*

- **Instruction:** "Summarize the contract."
- **Stimulus:** "Focus on Section 4: Termination Clauses."

**Why this matters for Engineers:**
You can build a dynamic UI where the user selects a "Focus Mode." Your code then injects different "Stimuli" into the same template prompt to give the user exactly what they want.

## 3. The DSP Prompt Pattern

> "Input Text: [Full Contract Content]
> 
> Directional Stimulus Keywords: Termination, Fees, Notice Period, Penalties.
> 
> Task: Based on the input text and focusing ONLY on the areas related to the stimulus keywords, provide a bulleted summary."

## 4. Interview Corner

1. **"Does DSP help with the 'Lost in the Middle' problem?"**
   * Answer: Yes. LLMs often forget information placed in the middle of long prompts. By providing a Directional Stimulus, you effectively "remind" the model's attention mechanism to specifically look for those details no matter where they are in the text.

2. **"Can the 'Stimulus' be automatically generated?"**
   * Answer: Yes! A common pattern is using a cheap, fast model to extract keywords (Stimuli), and then passing those to a smarter model for the final work.

3. **"How does DSP improve accuracy?"**
   * Answer: It reduces 'Noise.' By telling the model what *not* to focus on, you decrease the chances of it including irrelevant or confusing information in its response.

4. **"What happens if the Stimulus isn't in the text?"**
   * Answer: A good model should say "No information regarding [Stimulus] found." This is actually a great way to build "Search" functionality.

5. **"Is it better to put the Stimulus at the start or end?"**
   * Answer: Research suggests putting the "Stimulus" near the "Instruction" (usually at the end) works best for longer inputs.

## 5. Practical Insight

- **Dynamic Hints:** In production apps, the "Stimulus" is often a variable that changes based on user preferences.
- **Semantic Search + DSP:** You can use a Vector Database to find relevant chunks of text, and then use the *search query* itself as the Directional Stimulus in the final prompt.
- **When NOT to use:** If you need a completely unbiased, broad overview of a text.
