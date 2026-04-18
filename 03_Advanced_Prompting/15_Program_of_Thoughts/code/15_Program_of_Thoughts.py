import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_pot_demo():
    """
    Demonstrates Program-of-Thoughts (PoT) by forcing the model to 
    write a Python script to solve a complex math problem accurately.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for robust code generation
    model_name = "llama-3.1-8b-instant"

    problem = """
    A client has $500. They add $50 every month for 5 years at a 5.5% annual interest rate. 
    Exactly how much do they have at the end of 60 months?
    """

    # THE PoT PROMPT: We demand code, not just an answer.
    # Offloading logic to deterministic Python code ensures 100% accuracy.
    prompt = f"""
    Solve the financial problem below by writing a Python script. 
    The script should:
    1. Define all variables.
    2. Perform the calculation in a loop or using a formula.
    3. Print the final result.

    Problem: {problem}
    """

    print("-" * 50)
    print("GENERATING PROGRAM-OF-THOUGHTS (PoT) SCRIPT...")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        print("AI GENERATED CODE:")
        print("-" * 25)
        print(response.choices[0].message.content.strip())
        print("-" * 25)
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("LLMs are linguistic engines, not calculators.")
    print("PoT delegates logic to code, ensuring the model's stochastic")
    print("nature doesn't interfere with numeric precision.")
    print("-" * 50)

if __name__ == "__main__":
    run_pot_demo()
