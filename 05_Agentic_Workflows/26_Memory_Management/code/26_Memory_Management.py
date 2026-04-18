import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Simulation of a persistent 'Long-term' database
# In a production system, this would be a SQL database or Redis store.
USER_DATABASE = {
    "user_123": {
        "name": "Alice", 
        "preference": "loves dark mode", 
        "diet": "vegan",
        "past_trips": ["Tokyo", "Berlin"]
    }
}

def run_agentic_memory_demo():
    """
    Demonstrates Agentic Memory by pulling persistent facts from 
    'Long-term' storage and injecting them into the 'Short-term' 
    context (RAM) to provide personalized reasoning.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # llama-3.1-8b-instant is excellent for fast, personalized responses
    model_name = "llama-3.1-8b-instant"

    user_id = "user_123"
    
    # STEP 1: Memory Retrieval (The 'Hard Drive' lookup)
    # We retrieve the user's permanent profile before starting the turn.
    user_facts = USER_DATABASE.get(user_id, {})
    
    # STEP 2: Context Augmentation
    # We inject these long-term facts into the system prompt or 
    # the start of the current context window.
    prompt = f"""
    You are a personalized assistant. 
    Use the provided USER FACTS to customize your answer.
    
    USER FACTS: {user_facts}
    
    USER QUERY: "Suggest a dinner recipe for my birthday party."
    
    ASSISTANT:
    """

    print("-" * 50)
    print(f"RETRIEVING MEMORY: Loading profile for {user_facts.get('name')}...")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        print("PERSONALIZED RESPONSE:")
        print("-" * 25)
        print(response.choices[0].message.content.strip())
        print("-" * 25)
    except Exception as e:
        print(f"Error during memory interaction: {e}")
        
    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("The agent 'remembers' the vegan diet and Alice's name without")
    print("the user repeating it. This is 'Declarative Memory' in action.")
    print("It allows the agent to maintain a consistent persona over time.")
    print("-" * 50)

if __name__ == "__main__":
    run_agentic_memory_demo()
