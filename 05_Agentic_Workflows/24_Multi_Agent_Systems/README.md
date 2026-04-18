# Multi-Agent Systems (MAS)

> **Mentor note:** A single LLM is a soloist. A Multi-Agent System is an orchestra. When a task is too complex for one prompt (e.g., "Build a full-stack app"), we split it into specialized roles: a Coder, a Reviewer, and a DevOps Engineer. By narrowing the "Persona" and "Context" for each agent, we significantly reduce hallucinations and increase the "ceiling" of what AI can build.

---

## What You'll Learn

- Orchestration Patterns: Sequential, Hierarchical (Manager), and Joint Collaboration
- The "Critic" Pattern: Improving quality via adversarial feedback loops
- Key Frameworks: CrewAI (Roles), AutoGen (Dialogues), and LangGraph (State Machines)
- Managing shared state and "Blackboard" communication between agents
- Handling MAS challenges: Infinite loops, token spikes, and consensus reaching

---

## Theory & Intuition

### The "Specialist" Advantage

In a single-agent setup, one model is expected to be a master of everything simultaneously. In a Multi-Agent setup, we exploit the model's ability to play a **Persona** to focus its attention on a specific subset of its knowledge.

```mermaid
graph TD
    User[User Goal: Market Research Report] --> Manager[Manager Agent: Planner]
    
    subgraph Workers["The Workforce"]
        A1[Agent: Browser Researcher]
        A2[Agent: Data Analyst]
        A3[Agent: Technical Writer]
    end
    
    Manager --> A1
    A1 -->|Research Results| Manager
    Manager --> A2
    A2 -->|Clean Data| Manager
    Manager --> A3
    A3 -->|Final Report| User
    
    style Manager fill:#f9f,stroke:#333
    style Workers fill:#dfd,stroke:#333
```

**Why it matters:** Modularity. If the research fails, the Writer never starts. If the Coder makes a bug, the Reviewer catches it before the user ever sees it. This "Human-in-the-loop" style automation is the state-of-the-art for Generative AI.

---

## 💻 Code & Implementation

### A Basic Hand-off Pattern (Sequential)

This simulation shows a "Writer" agent passing its work to a "Critic" agent for review. This "Adversarial" loop ensures higher quality before the output is finalized.

```python
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_mas_demo():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast multi-agent turns
    model_name = "llama-3.1-8b-instant"

    # AGENT 1: THE WRITER
    writer_prompt = "You are a creative writer. Write a 2-sentence story about a robot on Mars."
    
    try:
        response_1 = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": writer_prompt}]
        )
        story = response_1.choices[0].message.content.strip()
        print(f"WRITER OUTPUT:\n{story}\n")

        # AGENT 2: THE CRITIC
        # This agent has a different 'Mindset' - purely critical and technical.
        critic_prompt = f"""
        You are a Strict Editor. 
        Review the story below for scientific accuracy and narrative flow. 
        If there are errors, provide 1 specific fix.
        
        STORY: {story}
        """
        response_2 = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": critic_prompt}]
        )
        review = response_2.choices[0].message.content.strip()
        
        print(f"CRITIC REVIEW:\n{review}\n")
        print("-" * 50)
        print("[Senior Note] In a real MAS, Agent 1 would then rewrite the story "
              "based on Agent 2's feedback.")
    except Exception as e:
        print(f"Error during agent turn: {e}")

if __name__ == "__main__":
    run_mas_demo()
```

---

## Multi-Agent Orchestration Patterns

| Pattern | How it works | Best For |
|---|---|---|
| **Sequential** | A -> B -> C | Simple pipelines (e.g., Translate -> Summarize) |
| **Hierarchical** | Manager delegates to workers | Large projects with many sub-tasks |
| **Joint (Peer)** | Agents talk in a group chat | Creative brainstorming, complex debugging |
| **Broadcast** | One-to-many info sharing | Alerting systems, keeping state in sync |

---

## Interview Questions & Model Answers

**Q: When should you use a Multi-Agent System instead of just one very large prompt?**
> **Answer:** Use MAS when the task requires different, sometimes conflicting, "mindsets" or toolsets. For example, a "Security Auditor" agent should be pessimistic and look for flaws, while a "Feature Developer" should be optimistic. MAS also helps overcome context window limits by splitting a large task into smaller sub-contexts.

**Q: How do you prevent "Infinite Loops" in a Multi-Agent conversation?**
> **Answer:** You must implement a **Conversation Controller** with a hard "Max Turns" limit (e.g., 10 turns). You also monitor for "Stagnation"—if the last 3 messages have a high semantic similarity, the system should intervene.

**Q: What is the "Manager Agent" pattern and why is it useful?**
> **Answer:** It's a pattern where a central "Orchestrator" agent receives the goal, breaks it into a "Plan," delegates tasks to specialized workers, and verifies their output. This reduces complexity for the user and ensures a cohesive result.

---

## Quick Reference

| Term | Role | Framework Example |
|---|---|---|
| **Agent** | A model + A persona + Tools | CrewAI Agent |
| **Orchestrator**| The "Brain" that decides who talks | LangGraph Node |
| **Critic** | An agent that reviews work | Self-Correction Loop |
| **Consensus** | All agents agreeing on an answer | Group Chat |
| **Hand-off** | Passing the "Token" to the next agent| Sequential Chain |
