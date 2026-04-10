# Topic 10: Role Prompting - Acting as a Specialist

## 1. Scenario: The Expert Explainer

You are building a learning platform for a tech company. You need to explain "Technical Debt" to different departments.

**The Problem:**
If you give the same explanation to the CEO and the Junior Developers, one will be confused and the other will be bored.

**Role Prompting** allows you to "skin" the AI's intelligence to match the specific expertise and needs of the person asking.

## 2. Implementation: Same Concept, Different Experts

This script demonstrates how much the output changes when we swap the "Persona."

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_role_prompting_demo():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    concept = "Microservices Architecture"

    # Persona 1: Simplified (for beginners)
    prompt_1 = f"You are a friendly 10-year veteran teacher. Explain {concept} using a LEGO analogy."

    # Persona 2: Professional (for developers)
    prompt_2 = f"You are a Senior Software Architect. Explain {concept} in terms of scalability, database sharding, and fault tolerance."

    print("--- PERSONA 1: TEACHER ---")
    print(model.generate_content(prompt_1).text.strip())

    print("\n" + "="*50 + "\n")

    print("--- PERSONA 2: ARCHITECT ---")
    print(model.generate_content(prompt_2).text.strip())

if __name__ == "__main__":
    run_role_prompting_demo()
```

## 3. Concept Breakdown

### The "Expert Filter"
When you give an LLM a role, you are providing it with a "frame of reference."
- **Tone & Style:** A teacher uses simple words and analogies; an architect uses jargon and data.
- **Assumed Knowledge:** The "Teacher" persona assumes you know nothing. The "Architect" persona assumes you already know basics like 'Servers' or 'APIs'.

**Why this matters for Engineers:**
Prompt Engineering isn't just about getting an answer; it's about getting an answer that is **useful for the specific context.** If you're building a tool for lawyers, the AI must speak like a lawyer.

## 4. Interview Corner

1. **"What is the 'persona' pattern in prompting?"**
   * Answer: It's the practice of starting a prompt with a phrase like "Act as a [Role]" or "You are a [Role]." This primes the model to use specific vocabulary and perspectives.

2. **"Does Role Prompting increase hallucinations?"**
   * Answer: Generally, no. In fact, it can decrease them by narrowing the model's "search space" to a specific field. However, if the persona is too detailed (e.g., a specific fictional character), the model might focus too much on 'acting' and less on 'accuracy'.

3. **"Where should you ideally put the Persona in your code?"**
   * Answer: In the **System Instruction** (from Topic 5). This makes the persona a foundation of the entire chat session.

4. **"How do you test if a persona is effective?"**
   * Answer: By comparing outputs across roles and checking for 'Lexical Density' (complexity of words) and 'Sentiment' to see if they match the desired role.

5. **"Can you ask the AI to play the 'Audience' instead of the 'Expert'?"**
   * Answer: Yes! You can say: "Write this for an audience of non-technical HR managers." This is often called "Audience Profiling."

## 5. Practical Insight

- **The 'Expert' Tier List:** Instead of just "Expert," use Staff, Principal, Fellow, or PhD to get deeper technical insights.
- **Strict Adherence:** Tell the model "Do not break character" to ensure it doesn't revert to a generic assistant middle-way through a long conversation.
- **When NOT to use:** For standard logic or data extraction tasks where a persona adds unnecessary "noise" to the output.
