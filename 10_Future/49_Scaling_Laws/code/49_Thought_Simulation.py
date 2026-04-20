import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def simulate_system_2_thinking():
    """
    Demonstrates the 'Thinking Time' pattern (System 2) 
    where a model is encouraged to think before answering.
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    # The prompt encourages 'Internal Monologue' or 'Chain of Thought'
    # This is how frontier models (like o1) operate internally.
    thought_prompt = """
    Solve this complex logic puzzle. 
    
    PUZZLE: 
    Three boxes are labeled 'Apples', 'Oranges', and 'Mixed'. 
    Every label is incorrect. 
    You pick one fruit from the 'Mixed' box and it is an Apple. 
    Label the boxes correctly.
    
    INSTRUCTIONS:
    1. First, show your step-by-step thinking inside <thought> tags.
    2. Then, provide the final answer.
    """

    print("Simulating Frontier Reasoning (System 2)...")
    
    response = client.models.generate_content(
        model="gemini-1.5-pro", # Using Pro for higher reasoning
        contents=thought_prompt
    )
    
    print("-" * 50)
    print(f"AI OUTPUT:\n{response.text.strip()}")
    print("-" * 50)
    print("[Senior Note] Scaling laws apply not just to training, but "
          "to 'Inference Time'. Giving the model 'Time to Think' "
          "is the current frontier of AI engineering.")

if __name__ == "__main__":
    simulate_system_2_thinking()
