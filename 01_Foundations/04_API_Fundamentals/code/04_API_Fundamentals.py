import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

def production_api_call():
    """
    Demonstrates a production-grade API call with latency and cost tracking.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    # Setup
    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = "Explain why API monitoring is critical for LLMs in 2 sentences."
    
    print("-" * 40)
    print(f"PROMPT: {prompt}")
    print("-" * 40)

    start_time = time.time()
    
    try:
        # 1. Call the API
        response = model.generate_content(prompt)
        end_time = time.time()
        
        # 2. Extract usage metadata (The "Bill")
        usage = response.usage_metadata
        in_tokens = usage.prompt_token_count
        out_tokens = usage.candidates_token_count
        
        # 3. Calculate Cost (Approximate rates for Gemini 1.5 Flash)
        # Rates: $0.075 per 1M input tokens, $0.30 per 1M output tokens
        cost = (in_tokens * 0.000000075) + (out_tokens * 0.00000030)
        
        print(f"Response: {response.text.strip()}")
        print("-" * 40)
        print("METRICS:")
        print(f"Latency: {end_time - start_time:.2f} seconds")
        print(f"Token Speed: {(in_tokens + out_tokens)/(end_time - start_time):.2f} tokens/sec")
        print(f"Total Tokens: {in_tokens + out_tokens} (In: {in_tokens}, Out: {out_tokens})")
        print(f"Estimated Cost: ${cost:.6f}")
        print("-" * 40)

    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    production_api_call()
