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
        print("Error: GEMINI_API_KEY not found in .env")
        return

    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel('gemini-2.5-flash')

    # A mixed review that requires 'intelligence' to categorize
    test_review = "The delivery was surprisingly fast, but honestly the product quality is average. Not sure if I'd buy again."

    # THE ZERO-SHOT PROMPT
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

    try:
        # Call the model
        response = model.generate_content(prompt)
        print(f"ZERO-SHOT CATEGORIZATION: {response.text.strip()}")
    except Exception as e:
        print(f"Error during categorization: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("Zero-shot works best with large models like Gemini 2.5 Flash.")
    print("It saves cost by avoiding expensive examples in the prompt.")
    print("-" * 50)

if __name__ == "__main__":
    run_zero_shot_demo()
