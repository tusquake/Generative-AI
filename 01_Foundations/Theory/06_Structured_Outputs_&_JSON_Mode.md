# 06. Structured Outputs & JSON Mode

> **Mentor note:** If there's one topic that separates engineers who "use LLMs" from engineers who "build reliable LLM systems", it's this one. Unstructured text output is fine for chatbots. The moment you're building agents, pipelines, or any system where the LLM output feeds into code — you need structured outputs. Master this early.

---

## What You'll Learn

- Why free-form LLM output breaks production systems and how structured outputs fix that
- The spectrum of approaches: prompt-based → JSON mode → schema enforcement → constrained decoding
- How to use the Anthropic, OpenAI, and Gemini APIs to enforce structure
- Pydantic-first patterns used in real codebases
- When structured outputs are NOT the right tool
- Interview questions you'll actually get asked

---

## Theory & Intuition

### The Core Problem

LLMs are next-token predictors. They don't inherently "know" they should output valid JSON — they produce whatever token sequence is most probable given the prompt. Even with a perfect prompt like *"respond only in JSON"*, models occasionally:

- Add prose before or after the JSON block
- Use single quotes instead of double quotes (invalid JSON)
- Hallucinate extra fields
- Truncate output mid-object if the response is long

In a demo this is annoying. In a production agent pipeline, it crashes your app.

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

**2. JSON Mode** — A model-level flag that biases the token sampler to always produce valid JSON syntax. Doesn't enforce your specific schema, but guarantees parseable output.

**3. Function/Tool Calling** — You define a function signature with a typed schema. The model decides to "call" it and fills in the parameters. The API returns a structured object. This is the industry standard approach for agents.

**4. Schema Enforcement (Pydantic + Instructor)** — Wrap API calls with a library like `instructor` that parses the response into a Pydantic model, validates it, and automatically retries with the validation error on failure. Extremely robust.

**5. Constrained Decoding** — At inference time, mask out any token that would violate your schema. Only possible when running your own model (vLLM, llama.cpp). Every token produced is structurally valid by construction.

### Why Function Calling > JSON Mode

JSON mode guarantees syntactic validity. It does not guarantee semantic validity — the model can still return `{"age": "twenty-three"}` when you wanted an integer.

Function calling gives the model a typed contract. The API enforces the schema on the output before returning it to you. This is why most production agentic systems use tool/function calling even when they don't actually want to call a tool — they're using it purely as a structured output mechanism.

---

## 💻 Code & Implementation

### 1. JSON Mode (OpenAI)

```python
from openai import OpenAI
import json

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},  # JSON mode flag
    messages=[
        {
            "role": "system",
            "content": "You are a data extractor. Always respond with valid JSON."
        },
        {
            "role": "user",
            "content": "Extract: John Doe, 29 years old, lives in Berlin."
        }
    ]
)

data = json.loads(response.choices[0].message.content)
print(data)  # {"name": "John Doe", "age": 29, "city": "Berlin"}
```

> **Gotcha:** JSON mode requires at least one message containing the word "json" (system or user). The API will error without it. Always put it in your system prompt.

---

### 2. Function / Tool Calling (OpenAI)

```python
from openai import OpenAI
import json

client = OpenAI()

# Define your schema as a tool
extract_person_tool = {
    "type": "function",
    "function": {
        "name": "extract_person",
        "description": "Extract structured person information from text",
        "parameters": {
            "type": "object",
            "properties": {
                "name":       {"type": "string",  "description": "Full name"},
                "age":        {"type": "integer", "description": "Age in years"},
                "city":       {"type": "string",  "description": "City of residence"},
                "confidence": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Confidence in the extraction"
                }
            },
            "required": ["name", "age", "city", "confidence"]
        }
    }
}

response = client.chat.completions.create(
    model="gpt-4o",
    tools=[extract_person_tool],
    tool_choice={"type": "function", "function": {"name": "extract_person"}},
    messages=[
        {"role": "user", "content": "John Doe, 29, lives in Berlin. Pretty sure about this."}
    ]
)

tool_call = response.choices[0].message.tool_calls[0]
data = json.loads(tool_call.function.arguments)
print(data)
# {"name": "John Doe", "age": 29, "city": "Berlin", "confidence": "high"}
```

> **Senior tip:** Set `tool_choice` to force the specific function. Without it the model might respond in plain text when it "thinks" a tool call isn't needed.

---

### 3. Pydantic + Instructor (Recommended Pattern for Production)

`instructor` is the library most senior engineers reach for. It wraps any API client and handles schema enforcement, validation, and auto-retry with error feedback in a single clean interface.

```bash
pip install instructor pydantic
```

```python
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
from typing import Literal

# 1. Define your schema as a Pydantic model
class PersonExtraction(BaseModel):
    name:       str            = Field(description="Full name of the person")
    age:        int            = Field(description="Age in years", ge=0, le=150)
    city:       str            = Field(description="City of residence")
    confidence: Literal["high", "medium", "low"]

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip().title()

# 2. Patch your client with instructor
client = instructor.from_openai(OpenAI())

# 3. Call the API — response is already a validated Pydantic object
person = client.chat.completions.create(
    model="gpt-4o",
    response_model=PersonExtraction,
    max_retries=3,         # auto-retries with validation error as feedback
    messages=[
        {"role": "user", "content": "John doe, 29, lives in berlin. quite confident."}
    ]
)

print(person.name)        # "John Doe"    (validator applied .title())
print(person.age)         # 29
print(person.model_dump())
```

> **Why this is better:** If the model returns `"age": "twenty-nine"`, Pydantic raises a `ValidationError`, instructor feeds that error back to the model automatically ("age must be an integer, got 'twenty-nine'"), and retries. You get a valid object or a clean exception — never a silent bad state.

---

### 4. Structured Outputs with Anthropic Claude

```python
import anthropic
import json

client = anthropic.Anthropic()

# Claude uses tool calling for structured output — same pattern
extract_tool = {
    "name": "extract_person",
    "description": "Extract person information from text",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age":  {"type": "integer"},
            "city": {"type": "string"}
        },
        "required": ["name", "age", "city"]
    }
}

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "extract_person"},
    messages=[
        {"role": "user", "content": "Extract: Sarah Chen, 34, based in Singapore."}
    ]
)

tool_use_block = next(b for b in response.content if b.type == "tool_use")
data = tool_use_block.input
print(data)  # {"name": "Sarah Chen", "age": 34, "city": "Singapore"}
```

---

### 5. Nested & Complex Schemas

Real-world extraction is rarely flat. Here's how to handle nested structures:

```python
from pydantic import BaseModel
from typing import Optional
import instructor
from openai import OpenAI

class Address(BaseModel):
    street:  Optional[str] = None
    city:    str
    country: str

class Company(BaseModel):
    name:     str
    industry: str

class PersonProfile(BaseModel):
    name:    str
    age:     int
    address: Address
    company: Optional[Company] = None
    skills:  list[str]

client = instructor.from_openai(OpenAI())

profile = client.chat.completions.create(
    model="gpt-4o",
    response_model=PersonProfile,
    messages=[{
        "role": "user",
        "content": """
            Priya Sharma, 31, works at Stripe as a senior engineer.
            She's in San Francisco, USA. Skills include Python, Kafka, and distributed systems.
        """
    }]
)

print(profile.model_dump_json(indent=2))
```

---

## When NOT to Use Structured Outputs

> This is the nuance that distinguishes senior engineers from juniors. Structured outputs are not always the answer.

**Don't force structure when:**

- The output is open-ended creative content (stories, summaries, explanations). Structure adds overhead with zero benefit.
- You need streaming and want to display tokens in real time. Streaming structured JSON is possible but complex — only do it if latency matters and you have a good reason.
- The schema is unclear at design time. Don't over-engineer your schema upfront. Start with a loose extraction, observe real outputs, then tighten the schema iteratively.
- You're using a weak/small model (< 7B params). Constrained decoding is your friend here — tool calling reliability degrades significantly on smaller models.

---

## Interview Questions & Model Answers

---

**Q: What's the difference between JSON mode and function calling for structured output?**

> JSON mode is a syntactic guarantee — the model will always return parseable JSON, but the shape is up to the model. Function calling is a semantic contract — you define a typed schema, and the API enforces that the response conforms to it. For production systems where you're feeding LLM output into downstream code, function calling is far more reliable.

---

**Q: A model keeps returning the right fields but with wrong types — for example, age as a string instead of an integer. How do you fix this?**

> This is a schema enforcement problem, not a prompt problem. I'd use the `instructor` library with a Pydantic model. Pydantic catches the type mismatch on validation, and instructor automatically retries the call with the validation error injected back into the conversation. The model sees "age must be an integer, got 'twenty-nine'" and corrects itself. You get a valid typed object or a clean exception after N retries — never a silent bad state.

---

**Q: How would you handle structured output from an LLM in a high-throughput pipeline where retries are expensive?**

> Three things: First, use constrained decoding if you control the inference stack (vLLM with guided generation) — this eliminates structural errors at the token level. Second, use few-shot examples in the prompt showing correct structured output — this dramatically reduces schema errors on the first attempt. Third, add a lightweight post-processing layer that catches and corrects common mistakes (string → int coercion, key name normalization) before hitting the validation layer, so you only retry on genuinely malformed responses.

---

**Q: What are the tradeoffs between Pydantic schema validation vs. prompt-only instruction for structured output?**

> Prompt-only is fast to implement but brittle — ~80% reliability on good models, much worse on smaller ones, and it silently fails rather than raising errors. Pydantic validation catches failures explicitly and enables automatic retry with error feedback. The tradeoff is latency: a retry costs a full API round-trip. For low-volume, high-stakes extractions, always validate. For high-volume, cost-sensitive pipelines, invest in constrained decoding or a highly tuned prompt + lightweight validation instead.

---

**Q: Can you stream structured output?**

> Yes, but it's a deliberate tradeoff. OpenAI supports streaming with function calls — you get partial JSON that you accumulate and parse once complete. `instructor` also has streaming support via `create_partial()` which streams a partial Pydantic model, useful for progressive UI rendering. The main gotcha is you can't validate until the stream completes, so errors only surface at the end. Use streaming structured output when UX latency matters more than early validation guarantees.

---

## Quick Reference

| Approach | Reliability | Setup | Best For |
|---|---|---|---|
| Prompt only | ~80% | Zero | Prototypes only |
| JSON mode | Syntactic 100% | 1 flag | When schema varies |
| Tool calling | ~95% | Schema def | Agents, pipelines |
| Instructor + Pydantic | ~99% (with retry) | Pydantic model | Production extraction |
| Constrained decoding | 100% | Infra change | Self-hosted, high volume |
