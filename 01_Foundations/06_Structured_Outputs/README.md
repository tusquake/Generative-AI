# Structured Outputs & JSON Mode

> **Mentor note:** If there's one topic that separates engineers who "use LLMs" from engineers who "build reliable LLM systems", it's this one. Unstructured text output is fine for chatbots. The moment you're building agents, pipelines, or any system where the LLM output feeds into code — you need structured outputs. Master this early.

---

## What You'll Learn

- Why free-form LLM output breaks production systems and how structured outputs fix that
- The spectrum of approaches: prompt-based → JSON mode → schema enforcement → constrained decoding
- How to use the Gemini API to enforce structure
- Pydantic-first patterns used in real codebases
- When structured outputs are NOT the right tool

---

## Theory & Intuition

### The Core Problem

LLMs are next-token predictors. They don't inherently "know" they should output valid JSON — they produce whatever token sequence is most probable given the prompt. Even with a perfect prompt like *"respond only in JSON"*, models occasionally:

- Add prose before or after the JSON block
- Use single quotes instead of double quotes (invalid JSON)
- Hallucinate extra fields
- Truncate output mid-object if the response is long

### The Spectrum of Solutions

Think of structured output as a spectrum of increasing reliability and decreasing flexibility:

```
Weakest                                                        Strongest
   │                                                               │
   ▼                                                               ▼
Prompt       JSON Mode     Function/Tool     Schema        Constrained
only         (hint)        Calling           Enforcement   Decoding
                           (contract)        (validation)  (token-level)
```

**1. Prompt-only** — "Respond in JSON with keys: name, age, city." Works ~80% of the time. Not acceptable in production.

**2. JSON Mode** — A model-level flag that biases the token sampler to always produce valid JSON syntax.

**3. Function/Tool Calling** — You define a function signature with a typed schema. The API enforces the schema on the output. This is the industry standard for agents.

**4. Schema Enforcement (Pydantic)** — Parsing the response into a Pydantic model for validation and automatic correction.

---

## 💻 Code & Implementation

### Enforcing JSON Schema with Gemini

Modern APIs allow you to specify the **Response MIME Type** and a **Response Schema**. This guarantees that the model will return valid JSON that matches your exact specification.

```python
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_structured_output_demo():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # 1. Define the schema (What we want to extract)
    # This is equivalent to a Pydantic model
    schema = {
        "description": "Information about a book",
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "author": {"type": "string"},
            "genre": {"type": "string"},
            "rating": {"type": "number", "description": "Rating out of 10"}
        },
        "required": ["title", "author", "rating"]
    }

    # 2. Configure the model with Structured Output
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": schema
        }
    )

    prompt = "Extract info: 'The Great Gatsby' by F. Scott Fitzgerald. A classic novel, 9.5/10."
    
    response = model.generate_content(prompt)
    
    # 3. Parse and use the data
    data = json.loads(response.text)
    print(f"Title: {data['title']}")
    print(f"Author: {data['author']}")
    print(f"Rating: {data['rating']}")

if __name__ == "__main__":
    run_structured_output_demo()
```

---

## When NOT to Use Structured Outputs

- **Creative Content:** If you want the AI to write a story or an explanation, forcing JSON will ruin the flow.
- **Real-time Streaming:** Streaming partial JSON blocks is technically complex and often unnecessary for simple UI rendering.
- **Unclear Schemas:** If you don't know what you're looking for yet, start with a prompt and tighten the schema later.

---

## Interview Questions & Model Answers

**Q: What's the difference between JSON mode and function calling for structured output?**
> **Answer:** JSON mode is a syntactic guarantee — the model will always return parseable JSON, but the shape is up to the model. Function calling is a semantic contract — you define a typed schema, and the API enforces that the response conforms to it.

**Q: A model keeps returning the right fields but with wrong types (e.g., age as a string). How do you fix this?**
> **Answer:** This is a schema enforcement problem. In production, I would use Pydantic validation. The validation catches the mismatch, and the system can automatically retry with the error feedback to the model.

---

## Quick Reference

| Approach | Reliability | Best For |
|---|---|---|
| Prompt only | ~80% | Prototypes only |
| JSON mode | Syntactic 100% | When schema varies |
| Tool calling | ~95% | Agents, pipelines |
| Pydantic | ~99% (with retry) | Production extraction |
