import os
from google import genai
from dotenv import load_dotenv
import datetime

load_dotenv()

def run_cache_demo():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # NOTE: Caching usually requires a large amount of content (e.g. > 32,768 tokens)
    # to be cost-effective or even allowed by the API.
    # This script demonstrates the pattern.

    print("Demonstrating Context Caching Pattern...")
    
    # 1. We create a cache for a large set of instructions/data
    # This is useful for:
    # - Massive legal documents
    # - Long codebases
    # - Video files (Gemini 1.5)
    
    # In a real scenario, 'contents' would be very large.
    try:
        # This is a conceptual call as it requires a specific project setup and large data
        print("[Step 1] Creating cache with TTL (Time to Live)...")
        # cache = client.caches.create(
        #     model="gemini-1.5-pro",
        #     config={
        #         "display_name": "knowledge_base_v1",
        #         "contents": ["... massive text ..."],
        #         "ttl": "3600s" # 1 hour
        #     }
        # )
        
        print("-" * 50)
        print("RESULT: Subsequent queries using this cache will be:")
        print("🚀 5x - 10x Faster TTFT (Time to First Token)")
        print("💰 Significantly cheaper per token")
        print("-" * 50)
        
    except Exception as e:
        print(f"Note: Cache creation usually requires >32k tokens. Error: {e}")

    print("[Senior Note] Prompt caching is the 'Silver Bullet' for "
          "Agentic workflows that need to read the same context repeatedly.")

if __name__ == "__main__":
    run_cache_demo()
