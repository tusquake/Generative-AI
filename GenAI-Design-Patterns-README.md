# Generative AI Design Patterns — Complete Reference

> A structured guide to the recurring design patterns used when building real-world Generative AI systems — from a single prompt to a full multi-agent production architecture.

Every pattern here solves one of two fundamental problems:
1. **"The model doesn't know enough or reason well enough on its own"** → Prompting, Reasoning, RAG, and Memory patterns
2. **"The model can't be fully trusted to act alone, reliably, or at scale"** → Agentic, Reliability/Safety, and Orchestration patterns

Keep that lens as you read — it makes it obvious *why* each pattern exists, not just what it's called.

---

## 🗺️ Table of Contents

1. [Prompting & Reasoning Patterns](#1-prompting--reasoning-patterns)
2. [Agentic Patterns](#2-agentic-patterns)
3. [RAG Patterns](#3-rag-patterns)
4. [Memory Patterns](#4-memory-patterns)
5. [Reliability & Safety Patterns](#5-reliability--safety-patterns)
6. [Workflow & Orchestration Patterns](#6-workflow--orchestration-patterns)
7. [Pattern Selection Cheat Sheet](#7-pattern-selection-cheat-sheet)

---

## 1. Prompting & Reasoning Patterns

*How you get a single LLM call to think and respond better, without changing the model itself.*

### Zero-Shot Prompting
Ask the model to perform a task with **no examples** — just an instruction. Relies entirely on the model's pretrained knowledge.
> **Analogy:** Asking a new employee to do a task using only a one-line instruction, trusting their general training.

### Few-Shot Prompting
Provide **a handful of input-output examples** in the prompt before the actual task, so the model can infer the expected pattern/format.
> **Analogy:** Showing a new employee 2-3 completed sample forms before asking them to fill one out themselves.

### Chain-of-Thought (CoT) Prompting
Instruct the model to **show its reasoning step by step** before giving a final answer, which improves accuracy on multi-step problems.
> **Analogy:** Asking a student to "show your work" on a math problem instead of just writing the final number.

### Tree-of-Thought (ToT)
The model explores **multiple reasoning branches** in parallel (like a tree), evaluates them, and prunes weaker paths before settling on the best one.
> **Analogy:** A chess player considering several possible move sequences before committing to one, rather than just playing the first idea that comes to mind.

### ReAct (Reason + Act)
Interleave **reasoning** with **actions** (tool calls) — think, act, observe the result, think again, repeat until done.
> **Analogy:** A detective who investigates a lead, reviews the evidence, then decides the next lead to chase — not solving the case purely from the armchair.

### Self-Consistency
Generate **multiple independent reasoning paths** for the same question and take the majority/most common final answer.
> **Analogy:** Asking three different experts the same question separately and going with the answer most of them agree on.

### Self-Critique / Self-Reflection (Reflexion)
The model **reviews and critiques its own output**, then revises it — adding a feedback loop within a single task.
> **Analogy:** A writer who drafts an essay, then re-reads it critically as an editor, and revises before submitting.

### Least-to-Most Prompting
Break a complex problem into a sequence of **progressively harder sub-problems**, solving simpler ones first and using those results to tackle the next.
> **Analogy:** Teaching addition before multiplication, then using both to solve a word problem — building up complexity step by step.

### Prompt Chaining
**Output of one prompt becomes the input to the next**, decomposing a complex task into a sequence of smaller, focused LLM calls.
> **Analogy:** An assembly line where each station performs one specific job and passes the partially-finished product to the next station.

---

## 2. Agentic Patterns

*How you structure systems where the LLM decides what to do, not just what to say.*

### Tool Use / Function Calling
The LLM is given a set of callable tools (functions/APIs) with descriptions, and decides **when and how to invoke them** based on the task.
> **Analogy:** Giving an assistant a phone and a list of contacts — now they can act, not just talk.

### Planner-Executor Pattern
One component (the **Planner**) breaks a goal into a sequence of steps; another component (the **Executor**) carries out each step.
> **Analogy:** An architect who designs the blueprint (planner) versus the construction crew who builds it (executor).

### Supervisor (Orchestrator-Worker) Pattern
A central **Supervisor agent** routes tasks to specialized **worker agents** and aggregates their results.
> **Analogy:** A project manager assigning tasks to team members and compiling their work into one deliverable.

### Hierarchical Agents
Multiple levels of supervisors — supervisors of supervisors — for delegating across large, complex task trees.
> **Analogy:** A company org chart: CEO → Department Heads → Individual Contributors.

### Agent Swarm / Multi-Agent Network
Agents **hand off control directly to each other**, peer-to-peer, without a central coordinator.
> **Analogy:** A relay race where the baton passes directly between runners with no central referee managing each handoff.

### Sequential / Pipeline Pattern
A **fixed order** of agents/steps — Agent A's output always feeds Agent B, then Agent C.
> **Analogy:** A factory assembly line where each station has one job, always in the same order.

### Router Pattern
A classification step decides **which specialized agent, tool, or path** should handle a given input.
> **Analogy:** A call center's "press 1 for billing, press 2 for support" system, routing the caller before any real work begins.

### Human-in-the-Loop (HITL)
Execution **pauses to wait for human approval** before continuing — typically for high-stakes or irreversible actions.
> **Analogy:** A bank teller calling the manager over before approving a large withdrawal.

### Plan-and-Solve
The model **writes an explicit plan first**, then executes against that plan, revising it if new information emerges.
> **Analogy:** A contractor drafting a project plan with phases before picking up a single tool.

### Reflection Pattern
After acting, the agent **evaluates its own output/result** and loops back to improve if it falls short — similar to self-critique but applied across the whole agent loop, including tool results.
> **Analogy:** A chef tasting their own dish mid-cooking and adjusting the seasoning before serving.

### Sub-Agent Delegation
A primary agent **spawns specialized sub-agents** for specific sub-tasks (e.g., research, writing, critique), each working in its own focused context.
> **Analogy:** A general contractor hiring specialist plumbers and electricians instead of doing every trade themselves.

---

## 3. RAG Patterns

*How you get an LLM to answer using your own data instead of relying purely on what it memorized during training.*

### Naive RAG
The baseline pattern: retrieve relevant chunks via vector similarity, insert them into the prompt, generate an answer.
> **Analogy:** A librarian who always pulls a few "similar-sounding" books off the shelf for every question, regardless of how good the match really is.

### Adaptive RAG
The system first decides **whether retrieval is even needed** for a given query, skipping it for questions the model can answer directly.
> **Analogy:** A librarian who first asks "do I even need to check the shelves, or do I already know this?"

### Corrective RAG (CRAG)
**Evaluates the quality of retrieved documents**; if they're poor, it falls back to an alternative source like a live web search.
> **Analogy:** A researcher who double-checks if the books they grabbed actually answer the question, and goes to a different library if not.

### Self-RAG
The model **critiques its own retrieved context and generated answer**, re-retrieving or revising if something doesn't hold up.
> **Analogy:** A librarian who double-checks their own answer against the book before handing it to you.

### GraphRAG
Builds a **knowledge graph** of entities and relationships from documents, retrieving via graph traversal rather than pure vector similarity — better for multi-hop questions.
> **Analogy:** Following a family tree to answer "who is my cousin's grandfather" instead of searching for sentences that merely sound similar.

### HyDE (Hypothetical Document Embeddings)
The model first generates a **hypothetical answer**, embeds that instead of the raw question, and retrieves using that embedding.
> **Analogy:** Imagining what the perfect answer would look like before searching, so you search using the "shape" of the answer, not just the question.

### Re-ranking Pattern
A second, more precise model **re-scores** the initially retrieved chunks, pushing the most relevant ones to the top before they reach the LLM.
> **Analogy:** A librarian's assistant double-checking the stack of books the first pass pulled, removing the irrelevant ones.

### Contextual Compression
**Strips out irrelevant parts** of retrieved chunks before passing them to the LLM, keeping only what's actually relevant.
> **Analogy:** Highlighting just the relevant sentence on a page instead of handing over the whole page.

### Multi-Query Retrieval
Generates **several reworded versions** of the user's question to widen the search net and catch results a single phrasing might miss.
> **Analogy:** Asking the same question to a library catalog in several different phrasings to be thorough.

### Parent-Document Retrieval
Retrieves **small, precise chunks** for matching accuracy, but returns the **larger parent section** for full context.
> **Analogy:** Finding the right paragraph, then handing over the whole page it came from for context.

### Vectorless RAG / Structure-Based Retrieval (PageIndex-style)
Instead of embeddings, an LLM **reasons over a table-of-contents-like tree** of the document to navigate to the right section.
> **Analogy:** Using a book's table of contents and your own judgment to find the right chapter, instead of blending the book into a "meaning smoothie" and searching by taste.

### Hybrid Search
Combines **keyword search (e.g., BM25)** with **vector/semantic search** for better recall across both exact-match and meaning-based queries.
> **Analogy:** Searching a library by both exact title match and "books like this one" at the same time.

---

## 4. Memory Patterns

*How an inherently stateless LLM appears to "remember" things across turns or sessions.*

### Short-Term (Buffer) Memory
Keeps the **recent conversation history** in context, re-sent with every new call.
> **Analogy:** Remembering what was just said in the current conversation, but nothing from last week.

### Long-Term Memory
**Persists** information across sessions — facts, preferences, or history — so it's available in future conversations, not just the current one.
> **Analogy:** A doctor's patient file that's pulled up at every visit, not just remembered during one appointment.

### Summarization Memory
Periodically **condenses older conversation turns into a summary**, keeping context manageable instead of growing unbounded.
> **Analogy:** Taking meeting minutes instead of keeping a full word-for-word transcript of every meeting ever held.

### Episodic Memory
Stores memory of **specific past events or interactions** ("episodes") that can be recalled when relevant.
> **Analogy:** Remembering "the time the customer complained about shipping delays in March" as a distinct, retrievable event.

### Semantic Memory
Stores **general facts and knowledge** (not tied to a specific event) that the system has learned or been given, independent of when it occurred.
> **Analogy:** Knowing "Paris is the capital of France" without remembering *when* or *how* you learned it.

### Virtual File System (Deep Agents)
The agent **writes intermediate findings to files** it can read back later, instead of keeping everything in the active context window.
> **Analogy:** Keeping a project notebook to jot down findings, instead of trying to hold every detail in your head at once.

---

## 5. Reliability & Safety Patterns

*How you keep an LLM-powered system safe, controllable, and production-grade.*

### Guardrails (Input / Output / Tool-Level)
Validation and filtering checks applied **before the agent starts, around tool calls, or after the final response** to catch harmful, unsafe, or sensitive content.
> **Analogy:** Airport security checkpoints at check-in, the boarding gate, and customs — each catching different things at different stages.

### Middleware Pattern
**Hook-based interception** of agent execution at defined points, used to implement guardrails, logging, or approval steps without changing core agent logic.
> **Analogy:** Checkpoints along an assembly line that can inspect, modify, or halt the product without redesigning the whole factory.

### Defense in Depth
**Stacking multiple independent safety layers**, so if one fails to catch an issue, another layer downstream still might.
> **Analogy:** Airport security having ID checks, baggage scans, and random secondary screening — multiple independent nets, not just one.

### LLM-as-a-Judge
Using **one LLM to evaluate/score** the output of another system against a defined rubric, at scale.
> **Analogy:** Hiring an expert grader to review thousands of essays consistently, instead of one teacher reading every single one personally.

### Fallback Pattern
If a primary model, tool, or provider fails, **automatically switch to a backup** to keep the system running.
> **Analogy:** If your regular cab service has no cars, the dispatcher automatically books a different company — you don't have to do anything.

### Circuit Breaker
**Temporarily stops sending requests** to a failing component after repeated failures, to prevent cascading failures and allow recovery.
> **Analogy:** A home's electrical circuit breaker that trips to stop a surge from frying the whole system, instead of letting the fault spread.

### Caching (Semantic / Exact)
**Reuses previous responses** for identical or near-identical requests instead of paying for a fresh LLM call every time.
> **Analogy:** A call center playing a recorded answer for the hundredth "what are your hours" call of the day.

### Gateway / Provider Abstraction Pattern
A **unified interface** sits between your application and multiple LLM providers, abstracting away provider-specific details.
> **Analogy:** A universal remote control — same buttons work whether the TV is Sony or Samsung.

### Rate Limiting & Load Balancing
**Controls and distributes** request traffic to avoid overwhelming a provider or hitting usage limits.
> **Analogy:** A nightclub bouncer letting people in at a controlled pace instead of everyone rushing the door at once.

---

## 6. Workflow & Orchestration Patterns

*How you structure the control flow of a multi-step, possibly multi-agent system.*

### State Machine Pattern (LangGraph-style)
Models the application as a **graph of nodes and edges** sharing a common state object that updates as execution proceeds.
> **Analogy:** A board game with a shared scoreboard everyone can read and update as pieces move across the board.

### Fan-Out/Fan-In (Parallelization)
**Splits work across multiple parallel branches**, then merges (joins) their results back together before continuing.
> **Analogy:** Multiple chefs working on different dishes for the same order simultaneously, then plating them together for one table.

### Conditional Routing
**Branches execution** based on the current state — "if condition X, go this way; otherwise, go that way."
> **Analogy:** A fork in the road with a traffic light deciding which path to take based on current conditions.

### Checkpointing / Persistence
**Saves the full execution state** at each step, enabling resuming, replaying, or pausing for human input later.
> **Analogy:** A video game's save file — close the game and resume from the exact save point later.

### Map-Reduce Pattern
**Applies the same operation across many independent items in parallel** (map), then **combines the results** into a single output (reduce).
> **Analogy:** Having many people each summarize one chapter of a book simultaneously, then combining those summaries into one overall book summary.

### Event-Driven Orchestration
Steps are triggered by **events** (e.g., a new document uploaded, a webhook firing) rather than a fixed, predetermined sequence.
> **Analogy:** A fire alarm system that triggers a response only when smoke is actually detected, not on a fixed schedule.

---

## 7. Pattern Selection Cheat Sheet

| If your problem is... | Reach for... |
|---|---|
| The model needs to reason through a multi-step problem | Chain-of-Thought, Tree-of-Thought, Least-to-Most |
| The model needs to take real-world actions | Tool Use / Function Calling, ReAct |
| You need multiple specialized agents working together | Supervisor, Hierarchical Agents, Agent Swarm |
| A task is too long/complex for one reasoning pass | Plan-and-Solve, Sub-Agent Delegation, Virtual File System |
| The model needs your private/current data | Naive RAG → Adaptive/Corrective/Self-RAG as needs grow |
| Documents are long and hierarchically structured | Vectorless RAG, Parent-Document Retrieval |
| Multi-hop questions across relationships | GraphRAG |
| The model needs to "remember" things | Short-Term, Long-Term, Summarization, Episodic Memory |
| You need to prevent harmful or risky actions | Guardrails, Human-in-the-Loop, Defense in Depth |
| A provider/component might fail | Fallback Pattern, Circuit Breaker |
| Costs are too high from repeated queries | Caching, Router Pattern |
| You need complex branching/looping control flow | State Machine Pattern (LangGraph-style), Conditional Routing |
| Many independent items need processing fast | Fan-Out/Fan-In, Map-Reduce |
| A workflow needs to survive restarts or pause for a human | Checkpointing / Persistence |

---

## 📖 One-Line Summary of the Whole Landscape

> **Prompting patterns** make a single call smarter → **Agentic patterns** let the model act and coordinate → **RAG patterns** give it real knowledge → **Memory patterns** let it remember → **Reliability patterns** keep it safe and available → **Orchestration patterns** tie all of the above into a coherent, controllable system.
