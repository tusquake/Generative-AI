# sampling_demo.py
# Topic 3: Sampling parameters - Temperature, Top-p, Top-k, max_tokens

import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# 1. Load your API key from a .env file
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
    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = "Write a one-sentence catchphrase for a futuristic coffee shop."

    # --- CONFIG 1: The 'Strict' Bot ---
    # Low temperature = predictable, safe, repetitive.
    strict_config = genai.types.GenerationConfig(
        temperature=0.0,
        max_output_tokens=50 
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
    # Changed to 1 try as requested (usually 3 to show determinism)
    for i in range(1):
        try:
            response = model.generate_content(prompt, generation_config=strict_config)
            print(f"Output: {response.text.strip()}")
        except Exception as e:
            print(f"Request failed: {e}")
        time.sleep(1)

    print("\n[CREATIVE BOT - Temp 1.0]")
    # Changed to 1 try as requested (usually 3 to show variation)
    for i in range(1):
        try:
            response = model.generate_content(prompt, generation_config=creative_config)
            print(f"Output: {response.text.strip()}")
        except Exception as e:
            print(f"Request failed: {e}")
        time.sleep(1)

    print("\n" + "-" * 50)
    print("ENGINEERING INSIGHT:")
    print("Sampling parameters control the trade-off between stability and creativity.")
    print("-" * 50)

if __name__ == "__main__":
    explore_sampling_configs()
