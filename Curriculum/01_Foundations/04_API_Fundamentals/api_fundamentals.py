# api_fundamentals.py
# Topic 4: API Fundamentals - Calling LLMs and Managing Costs

import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Load your API key from a .env file
# Create a .env file in the root with GEMINI_API_KEY=your_key_here
load_dotenv()

def run_production_api_demo():
    """
    Demonstrates a robust API call with latency and cost tracking.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set GEMINI_API_KEY in your .env file.")
        return

    # Initialize the model
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Explain why token counting is important for a production AI application."

    print("-" * 50)
    print(f"PROMPT: {prompt}")
    print("-" * 50)

    try:
        # Start timer for latency tracking
        start_time = time.time()
        
        # ⭐ KEY 1: The standard API call
        response = model.generate_content(prompt)
        
        end_time = time.time()
        latency = end_time - start_time

        # ⭐ KEY 2: Extracting usage metadata (Tokens)
        usage = response.usage_metadata
        prompt_tokens = usage.prompt_token_count
        completion_tokens = usage.candidates_token_count
        total_tokens = prompt_tokens + completion_tokens

        # ⭐ KEY 3: Estimated Cost Calculation (Gemini 1.5 Flash rates)
        # Rates (Estimated): $0.075 / 1M input tokens, $0.30 / 1M output tokens
        estimated_cost = (prompt_tokens * 1.5e-7) + (completion_tokens * 6.0e-7)

        print(f"RESPONSE:\n{response.text.strip()}")
        print("-" * 50)
        
        # ⭐ KEY 4: Production metrics
        print(f"METRICS:")
        print(f"- Latency        : {latency:.2f} seconds")
        print(f"- Tokens (In/Out): {prompt_tokens} / {completion_tokens}")
        print(f"- Total Tokens   : {total_tokens}")
        print(f"- Estimated Cost : ${estimated_cost:.6f}")
        print("-" * 50)

    except Exception as e:
        print(f"Production Error captured: {e}")
        print("Tip: In a real app, you would log this to a service like Sentry or LangSmith.")

if __name__ == "__main__":
    run_production_api_demo()
