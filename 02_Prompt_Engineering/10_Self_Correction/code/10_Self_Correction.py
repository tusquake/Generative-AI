import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_self_correction_demo():
    """
    Demonstrates a multi-pass workflow where the model acts as its own critic
    to harden and improve generated code.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)

    initial_prompt = "Write a Python function to read 'data.txt' and print each line."

    print("-" * 50)
    print("STEP 1: GENERATING INITIAL ANSWER...")
    print("-" * 50)

    try:
        initial_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ corrected model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": initial_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        initial_code = initial_response.choices[0].message.content
        print(initial_code.strip())

    except Exception as e:
        print(f"Error during step 1: {e}")
        return

    critique_prompt = f"""
You are a Senior Security & Performance Engineer. 
Review the Python code below and find at least 3 vulnerabilities or missing safety checks.

Code to review:
{initial_code}

Provide an IMPROVED, production-ready version of the code that handles:
1. Standard I/O error handling (Missing files)
2. Resource management (Context managers)
3. Performance (Memory efficiency for large files)
"""

    print("\n" + "-" * 50)
    print("STEP 2: RUNNING SELF-CORRECTION (CRITIQUE PASS)...")
    print("-" * 50)

    try:
        final_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ corrected model name
            messages=[
                {"role": "system", "content": "You are a Senior Security & Performance Engineer."},
                {"role": "user", "content": critique_prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )

        print(final_response.choices[0].message.content.strip())

    except Exception as e:
        print(f"Error during self-correction: {e}")

    print("-" * 50)
    print("INSIGHT:")
    print("The first pass was functional but fragile.")
    print("The second pass used the model as a 'critic' to add security and robustness.")
    print("Multi-pass pipelines are the standard for production-grade AI code.")
    print("-" * 50)


if __name__ == "__main__":
    run_self_correction_demo()