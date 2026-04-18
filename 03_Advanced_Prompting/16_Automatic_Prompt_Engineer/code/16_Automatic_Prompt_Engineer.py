import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_ape_refiner_demo():
    """
    Simulates the 'Meta-Prompting' phase of an Automatic Prompt Engineer (APE).
    The model analyzes failure cases and proposes optimized prompt variants.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast meta-prompting
    model_name = "llama-3.1-8b-instant"

    original_prompt = "Summarize this data."
    failure_cases = """
    1. Input: [JSON of 100 items] -> Output: Too short, missed key IDs.
    2. Input: [Medical report] -> Output: Hallucinated a diagnosis.
    """

    # THE META-PROMPT (The "Prompt Engineer" Persona)
    # We ask the model to act as an optimizer for its own instructions.
    meta_prompt = f"""
    You are an Automatic Prompt Engineer.
    
    Current Prompt: "{original_prompt}"
    Failure Cases: {failure_cases}

    Analyze why the current prompt failed and generate 3 NEW prompt variations 
    that are more robust, concise, and explicit about following constraints.
    Inject techniques like Chain-of-Thought or Directional Stimulus if appropriate.
    """

    print("-" * 50)
    print("RUNNING APE REFINEMENT PASS...")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": meta_prompt}],
            temperature=0.7
        )
        print("OPTIMIZED PROMPT CANDIDATES:")
        print("-" * 25)
        print(response.choices[0].message.content.strip())
        print("-" * 25)
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("APE treats Prompt Engineering as an optimization problem.")
    print("By feeding failure cases back into a Meta-Model, we can discover")
    print("instruction variants that specifically mitigate observed errors.")
    print("-" * 50)

if __name__ == "__main__":
    run_ape_refiner_demo()
