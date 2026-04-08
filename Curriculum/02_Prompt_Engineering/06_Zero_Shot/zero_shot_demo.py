# zero_shot_demo.py
# Topic 6: Zero-shot Prompting - Capabilities and Failure Modes

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_zero_shot_demo():
    """
    Demonstrates categorizing sentiment WITHOUT any previous examples.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set GEMINI_API_KEY in your .env file.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # A mixed review that requires 'intelligence' to categorize
    test_review = "The delivery was surprisingly fast, but honestly the product quality is average. Not sure if I'd buy again."

    # ⭐ THE ZERO-SHOT PROMPT
    # We provide the goal and the categories, but ZERO examples.
    prompt = f"""
    Categorize the following customer review into exactly one of these labels:
    - Positive
    - Negative
    - Mixed
    - Question

    Review: "{test_review}"
    
    Response (Category name only):
    """

    print("-" * 50)
    print(f"INPUT REVIEW: {test_review}")
    print("-" * 50)

    # Call the model
    response = model.generate_content(prompt)
    
    print(f"ZERO-SHOT CATEGORIZATION: {response.text.strip()}")
    print("-" * 50)

if __name__ == "__main__":
    run_zero_shot_demo()
