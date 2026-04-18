# Memory Management (Agentic)

> **Mentor note:** A stateless AI is a chatbot; a stateful AI is an Agent. While Topic 21 focused on the mechanics of the "Context Window," this topic covers the persistent identity of an agent. How does an agent remember your preferences from three months ago? How does it maintain a "World State" during a 4-hour task? Masterful memory management is what turns a one-off prompt into a truly intelligent partner.

---

## What You'll Learn

- The Memory Hierarchy: Short-term (RAM) vs. Long-term (Disk) analogies
- Semantic Memory: Using Vector DBs to recall past interactions
- Procedural Memory: Helping agents remember *how* to perform tasks
- "MemGPT" concepts: Paging and swapping context in/out of the window
- Privacy & Policy: Implementing GDPR-compliant "Right to be Forgotten" in AI systems

---

## Theory & Intuition

### The RAM vs. Disk Analogy

In agentic architecture, we treat the **Context Window** as RAM (fast, expensive, limited) and the **Vector Database/SQL** as the Hard Drive (slow, cheap, infinite).

```mermaid
graph LR
    User[User Query] --> Agent[The Agent Brain]
    
    subgraph Short_Term["RAM (Context Window)"]
        Chat[Recent 10 Messages]
    end
    
    subgraph Long_Term["Disk (External Store)"]
        Vector[(Vector DB: Past Years)]
        Entity[(SQL: User Preferences)]
    end
    
    Agent <-->|Read/Write| Short_Term
    Agent -.->|Search| Vector
    Agent -.->|Lookup| Entity
    
    style Short_Term fill:#bbf,stroke:#333
    style Long_Term fill:#dfd,stroke:#333
```

**Why it matters:** Accuracy and Personalization. If the user said "I am allergic to peanuts" in January, the agent should retrieve that specific memory when suggesting a recipe in June, without having to keep that sentence in the expensive "RAM" the whole time.

---

## 💻 Code & Implementation

### Implementing a "Persistent Preference" Memory

This script demonstrates how to inject "Long-term" facts (from a database) into the "Short-term" context to create a personalized, stateful experience.

```python
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Simulation of a persistent database (Long-term Store)
USER_DATABASE = {
    "user_123": {"name": "Alice", "preference": "loves dark mode", "diet": "vegan"}
}

def run_agentic_memory_demo():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast personalized turns
    model_name = "llama-3.1-8b-instant"

    user_id = "user_123"
    
    # STEP 1: Memory Retrieval (Lookup from 'Disk')
    user_facts = USER_DATABASE.get(user_id, {})
    
    # STEP 2: Context Augmentation (Injecting facts into 'RAM')
    prompt = f"""
    You are a personalized culinary assistant. 
    Use the USER FACTS to tailor your recommendation.
    
    USER FACTS: {user_facts}
    
    RECENT CHAT:
    User: "Suggest a dinner recipe for my birthday party."
    
    ASSISTANT:
    """

    print(f"Generating personalized response for {user_facts.get('name')}...")
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        print("-" * 50)
        print(response.choices[0].message.content.strip())
        print("-" * 50)
    except Exception as e:
        print(f"Error during memory demo: {e}")

if __name__ == "__main__":
    run_agentic_memory_demo()
```

---

## The Memory Spectrum

| Type | Persistance | Storage | Best For |
|---|---|---|---|
| **Chat Buffer** | Volatile (Current session) | RAM / Context | Keeping track of the current topic |
| **Semantic** | Permanent | Vector Database | Recalling "vibes" or related past chats |
| **Episodic** | Permanent | Timelined Logs | Remembering specific past events |
| **Declarative**| Permanent | SQL / Key-Value | Hard facts (e.g., API keys, Birthdays) |

---

## Interview Questions & Model Answers

**Q: What is "Semantic Memory" in the context of an AI Agent?**
> **Answer:** It's the use of embeddings to store every interaction. When a user asks a question, the system searches the history for "concepts" related to the query. This allows an agent to have "long-term associations" without bloating the context window.

**Q: How do you handle "Conflicting Memories"?**
> **Answer:** This is a "State Conflict" problem. I implement **Temporal Weighting**, where more recent memories are prioritized. I also use **Summarization Agents** to periodically reconcile the memory, keeping the most current state as the primary "Truth."

**Q: What is the "Right to be Forgotten" for an AI agent?**
> **Answer:** It's a compliance requirement where a user can request that the AI "forgets" them. Technically, this means deleting their specific vectors from the Vector DB and their rows from the SQL state.

---

## Quick Reference

| Term | Role |
|---|---|
| **Short-term** | What the AI is literally looking at right now |
| **Long-term** | What the AI can go look up in the library |
| **Fact Extraction**| The task of converting chat text into "Declarative" SQL data |
| **MemGPT** | An architecture where an AI manages its own memory paging |
| **State Drift** | When the AI's "Internal world model" no longer matches reality |
