import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_react_simulation():
    """
    Simulates the first turn of a ReAct loop. 
    The model explains its reasoning (Thought) and selects a tool (Action).
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for agentic tasks
    model_name = "llama-3.1-8b-instant"

    problem = "What is the account balance for user@example.com? If it's over $500, suggest a savings plan."

    # THE ReAct TEMPLATE
    # We teach the model to interleave reasoning with tool selection.
    prompt = f"""
    Solve the following problem. Use the following format:
    Thought: Explain why you are performing the next action.
    Action: The tool to call (one of [GetUserID, GetBalance, SuggestPlan]).
    Observation: The result of the action (I will provide this).
    ... (Repeat as needed)
    Final Answer: Your final conclusion to the user.

    Constraint: Do not hallucinate data. If you don't have an observation, you haven't done the action yet.

    Problem: {problem}
    """

    print("-" * 50)
    print("RUNNING ReAct AGENT SIMULATION...")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("ReAct prevents 'Action Drift' by forcing the model to reason")
    print("before every tool call. This Thought -> Action -> Observation")
    print("loop is the foundation of modern AI Agents.")
    print("-" * 50)

if __name__ == "__main__":
    run_react_simulation()
