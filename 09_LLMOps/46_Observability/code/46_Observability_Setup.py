import os
from dotenv import load_dotenv

# Note: Integration is usually done via Environment Variables
# This script demonstrates the configuration pattern for LangSmith/Langfuse.

def setup_tracing():
    # Load environment variables
    load_dotenv()
    
    # These variables tell LangChain (and other SDKs) to automatically 
    # send traces to the cloud dashboard.
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "your_key_here")
    os.environ["LANGSMITH_PROJECT"] = "Generative-AI-Mastery"

    print("-" * 50)
    print("🔭 OBSERVABILITY LAYER ENABLED")
    print("-" * 50)
    print("Every LLM call will now be visible in the LangSmith dashboard.")
    print("\nKey metrics tracked:")
    print("1. Latency per step (Bottleneck detection)")
    print("2. Token count (Cost management)")
    print("3. Nested spans (Tool call debugging)")
    print("-" * 50)
    print("[Senior Note] Observability is the only way to debug 'Probabilistic' "
          "bugs that standard unit tests might miss.")

if __name__ == "__main__":
    setup_tracing()
