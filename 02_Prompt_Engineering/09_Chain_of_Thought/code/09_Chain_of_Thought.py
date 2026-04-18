import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_cot_demo():
    """
    Demonstrates how Chain-of-Thought (CoT) improves accuracy 
    by forcing the model to show its work.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel('gemini-2.5-flash')

    # A complex multi-step inventory problem
    problem = """
    A warehouse has 100 units of 'AI Chips'. 
    1. They send 20 units to a client. 
    2. The client returns 5 of those units.
    3. The warehouse sells HALF of their current stock in a flash sale.
    4. They receive a new shipment of 10 units.
    How many units are in the warehouse now?
    """

    # THE CoT PROMPT
    # By demanding a step-by-step breakdown, we reduce arithmetic errors.
    prompt = f"""
    Solve the inventory problem below. 
    IMPORTANT: Think through this STEP-BY-STEP. List your calculations for each step level.
    End your response with 'Final Result: [number]'.
    
    Problem: {problem}
    """

    print("-" * 50)
    print("RUNNING CHAIN-OF-THOUGHT (CoT) DEMO...")
    print("-" * 50)

    try:
        response = model.generate_content(prompt)
        print(f"AI RESPONSE:\n{response.text.strip()}")
    except Exception as e:
        print(f"Error during CoT generation: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("By forcing the model to 'show its work', we turn the output tokens")
    print("into a temporary scratchpad. This significantly improves accuracy")
    print("on multi-step logic problems.")
    print("-" * 50)

if __name__ == "__main__":
    run_cot_demo()
