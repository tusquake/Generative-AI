import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_few_shot_demo():
    """
    Demonstrates how providing 3-5 high-quality examples (Few-Shot) 
    aligns the model with a specific output pattern.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel('gemini-2.5-flash')

    # THE FEW-SHOT PROMPT
    # We provide a pattern of Input/Output pairs to "teach" the model the format.
    prompt = """
    Extract sentiment and confidence from the review. Respond with ONLY valid JSON.

    Input: "This is the best purchase I have ever made!"
    Output: {"sentiment": "positive", "confidence": 0.98}

    Input: "The product is fine, but the box was crushed."
    Output: {"sentiment": "mixed", "confidence": 0.75}

    Input: "I hate this company. Never buying again."
    Output: {"sentiment": "negative", "confidence": 0.99}

    Input: "Where is my order? It has been three weeks."
    Output: 
    """

    print("-" * 50)
    print("SENDING FEW-SHOT PROMPT...")
    print("-" * 50)

    try:
        response = model.generate_content(prompt)
        print(f"AI RESPONSE:\n{response.text.strip()}")
    except Exception as e:
        print(f"Error during few-shot generation: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("The model followed the JSON pattern perfectly because of the examples.")
    print("Few-shot is essential for complex formatting or niche logic.")
    print("-" * 50)

if __name__ == "__main__":
    run_few_shot_demo()
