# sampling_demo.py
# Topic 3: Sampling parameters - Temperature, Top-p, Top-k, max_tokens

import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load your API key from a .env file
# Create a .env file with GEMINI_API_KEY=your_key_here
load_dotenv()

def explore_sampling_configs():
    """
    Demonstrates how different sampling configurations affect LLM outputs.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set GEMINI_API_KEY in your .env file.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Write a one-sentence catchphrase for a futuristic coffee shop."

    # --- CONFIG 1: The 'Strict' Bot ---
    # Low temperature = predictable, safe, repetitive.
    strict_config = genai.types.GenerationConfig(
        temperature=0.0,
        max_symbols=50 # Stop after a short amount
    )

    # --- CONFIG 2: The 'Creative' Bot ---
    # High temperature = risky, unusual, varied.
    creative_config = genai.types.GenerationConfig(
        temperature=1.0,
        top_p=0.95,
        top_k=40
    )

    print("-" * 50)
    print(f"PROMPT: {prompt}")
    print("-" * 50)

    print("\n[STRICT BOT - Temp 0.0]")
    # Generate 3 times to see if it changes
    for i in range(3):
        response = model.generate_content(prompt, generation_config=strict_config)
        print(f"Try {i+1}: {response.text.strip()}")

    print("\n[CREATIVE BOT - Temp 1.0]")
    # Generate 3 times to see the variation
    for i in range(3):
        response = model.generate_content(prompt, generation_config=creative_config)
        print(f"Try {i+1}: {response.text.strip()}")

    print("\n" + "-" * 50)
    print("ENGINEERING INSIGHT:")
    print("Notice how the 'Strict' bot likely gave the exact same answer 3 times,")
    print("while the 'Creative' bot explored different ideas.")
    print("-" * 50)

if __name__ == "__main__":
    explore_sampling_configs()
