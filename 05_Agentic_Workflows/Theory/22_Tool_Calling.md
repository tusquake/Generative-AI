# Topic 22: Tool Calling & Function Binding - The AI's Hands

## 1. Scenario: The "Blind Accountant"
You are chatting with a powerful LLM. 
- **User:** "What is the stock price of Google right now?"
- **The Problem:** The LLM was trained in 2023. It can't see the internet. It can only "guess" or say it doesn't know.
- **The Solution:** Give the AI a "Calculator" and an "API Fetcher" tool.
- **Result:** The AI says, *"I don't know the price, but I have a tool called `get_stock_price`. I will call it."* It gets the data and gives you the real answer.

## 2. The Concept: Function Calling
**Tool Calling** (or Function Calling) is the ability of an LLM to output a structured JSON object containing a function name and arguments, instead of a text response.

### How it works:
1.  **Declaration:** You provide the AI with a list of functions it *could* use (name, description, and parameters).
2.  **Model Decision:** The AI reads the user query and decides: "I need to call function X with argument Y."
3.  **External Execution:** THE AI DOES NOT RUN THE CODE. **Your application** reads the JSON, runs the actual Python/JS function, and sends the result back to the AI.
4.  **Final Answer:** The AI reads the function output and writes a natural language response to the user.

## 3. Workflow Diagram (Text)
[User: "Check weather in Delhi"] -> 
[AI: "{ 'function': 'get_weather', 'args': {'city': 'Delhi'} }"] -> 
[App: (runs API call, returns '32 degrees')] -> 
[AI: "The weather in Delhi is currently 32 degrees."]

## 4. Key Concepts
- **JSON Schema:** The "language" used to describe tools to the AI.
- **Tool Choice:** Forcing the AI to use a tool (`tool_choice: 'required'`) or letting it decide (`'auto'`).
- **Parallel Tool Calling:** The ability of the AI to call multiple functions at once (e.g., "Check weather in Delhi *and* Mumbai").

## 5. Interview Corner

1. **"Does the LLM actually execute the function?"**
   * Answer: No. The LLM only "signs the request." It generates the JSON. It is the responsibility of the client (your code) to execute the function and return the data.

2. **"What happens if the AI generates the wrong JSON for a tool?"**
   * Answer: This is a "Schema Violation." You should catch the error and send a system message back to the AI: *"Error: The argument 'city' was missing. Please try again."*

3. **"Why use Tool Calling instead of just letting the AI write Python code?"**
   * Answer: Tool Calling is safer and more structured. You control exactly what the AI can do (e.g., `read_only_db` instead of `full_access`). It also makes it easier to integrate with existing REST APIs.

4. **"What is 'Zero-shot Tool Selection'?"**
   * Answer: The model's ability to pick the right tool from a list of hundreds of descriptions without needing specific examples of how to use them.
