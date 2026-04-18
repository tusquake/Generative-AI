import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_tot_demo():
    """
    Demonstrates the Tree of Thoughts (ToT) approach by simulating 
    a multi-expert discussion to solve a strategic problem.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for speed and reasoning
    model_name = "llama-3.1-8b-instant"

    problem = """
    A startup has $10,000 left in its bank account. 
    It needs to choose between:
    1. Hiring a freelance developer to fix 5 critical bugs.
    2. Investing in a 1-month marketing campaign to get 100 new users.
    3. Buying specialized hardware to speed up data processing by 50%.
    Which choice ensures the startup survives the next 3 months?
    """

    # THE ToT PROMPT: Simulated Expert Discussion
    # We force the model to explore 3 paths, critique them, and prune.
    prompt = f"""
    Solve the following problem using a Tree of Thoughts approach:
    
    1. Imagine three different expert advisors (a CTO, a CMO, and a CFO) each offering one distinct strategy.
    2. For each strategy, have the experts critique each other's ideas and identify one fatal flaw.
    3. Based on the critiques, prune the failing paths and provide the final, most robust strategy.

    Problem: {problem}
    """

    print("-" * 50)
    print("RUNNING TREE OF THOUGHTS (ToT) SIMULATION...")
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
    print("ToT allows the model to explore 'parallel universes' of reasoning.")
    print("By critiquing its own paths, it avoids 'greedy' mistakes that linear")
    print("reasoning often makes in complex planning tasks.")
    print("-" * 50)

if __name__ == "__main__":
    run_tot_demo()
