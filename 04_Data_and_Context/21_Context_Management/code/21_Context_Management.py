import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_context_management_demo():
    """
    Demonstrates Context Management by simulating two strategies:
    1. Sliding Window: Keeping only the most recent interactions.
    2. Summarization Memory: Preserving key facts from early in the chat.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for state-aware generation
    model_name = "llama-3.1-8b-instant"

    # Simulation of a long conversation history.
    # Note how the 'Goal' (Tokyo trip) and 'Constraint' (Peanut allergy)
    # were established much earlier than the current turn.
    history = [
        {"role": "user", "content": "I want to plan a trip to Tokyo."},
        {"role": "assistant", "content": "Great! When are you going?"},
        # ... 50 messages of back-and-forth ...
        {"role": "user", "content": "Also, I am allergic to peanuts."},
        {"role": "assistant", "content": "Noted. I'll filter for peanut-free restaurants."},
    ]

    # STRATEGY 1: SLIDING WINDOW
    # We only take the last 2 turns to save tokens.
    short_context = history[-2:]

    # STRATEGY 2: SUMMARIZATION MEMORY
    # We carry a persistent summary of the most critical facts discovered.
    summary = "User is planning a Tokyo trip and has a severe peanut allergy."
    
    # We combine the summary with the recent window to provide high-signal context.
    current_prompt = f"""
    Summary of Conversation: {summary}
    Recent History: {short_context}
    
    Next User Query: "Suggest a good ramen spot near Shibuya."
    """

    print("-" * 50)
    print("PROCESSING QUERY WITH MANAGED CONTEXT")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": current_prompt}],
            temperature=0.7
        )
        print("ASSISTANT RESPONSE:")
        print("-" * 25)
        print(response.choices[0].message.content.strip())
        print("-" * 25)
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("Without Context Management, the model would forget the peanut")
    print("allergy or the Tokyo destination as they would be 'pushed out'")
    print("of the fixed context window. Combining a Summary with a ")
    print("Sliding Window creates a robust 'long-term memory'.")
    print("-" * 50)

if __name__ == "__main__":
    run_context_management_demo()
