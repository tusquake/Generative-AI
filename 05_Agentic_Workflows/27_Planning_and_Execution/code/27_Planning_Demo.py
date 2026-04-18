import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_planning_demo():
    """
    Demonstrates the 'Planner-Executor' pattern:
    1. The Planner: Decomposes a fuzzy goal into a discrete task list.
    2. The Executor: (Simulated) Performs the steps.
    
    This separation prevents the model from rushing into execution 
    without a strategy, which reduces logic errors.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast, logical decomposition
    model_name = "llama-3.1-8b-instant"

    user_goal = "Plan a 3-day trip to Tokyo, find a hotel near Shibuya, and check ramen spots."

    print("-" * 50)
    print("PHASE 1: THE ARCHITECT (PLANNING)")
    print("-" * 50)

    # We force the model to 'Think' before it acts by asking for a Plan first.
    planning_prompt = f"""
    You are a Strategic Planner Agent. 
    Task: Break the user's high-level goal into a numbered list of executable steps.
    Each step must be a single, discrete action that can be performed by a worker.
    
    USER GOAL: {user_goal}
    
    DETAILED PLAN:
    """
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": planning_prompt}],
            temperature=0.0 # High determinism for planning
        )
        plan = response.choices[0].message.content.strip()
        print(plan)
        
        print("\n" + "-" * 50)
        print("PHASE 2: THE BUILDER (EXECUTION)")
        print("-" * 50)

        # In a real system, we would parse the plan and iterate through steps.
        # Here we simulate the first logical action.
        print("STEP 1: INITIALIZING SYSTEM STATE")
        print("ACTION: Fetching user travel preferences and budget constraints...")
        print("RESULT: User budget is $2500. Travel dates: Nov 1st - Nov 4th.")
        print("-" * 50)

        print("STEP 2: SHIBUYA ACCOMMODATION SEARCH")
        print("ACTION: Searching for hotels within 1km of Shibuya Crossing...")
        print("RESULT: Found 3 candidates: Shibuya Stream, Excel Hotel, Hotel En.")
        print("-" * 50)

    except Exception as e:
        print(f"Error during planning interaction: {e}")

    print("INSIGHT:")
    print("By creating a Plan first, the Agent has a 'Source of Truth' to")
    print("measure progress. If an execution step fails (e.g., all hotels")
    print("are booked), the Planner can re-route the strategy without")
    print("losing sight of the original goal.")
    print("-" * 50)

if __name__ == "__main__":
    run_planning_demo()
