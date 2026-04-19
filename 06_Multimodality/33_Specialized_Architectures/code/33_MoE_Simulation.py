import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_moe_simulation():
    """
    Simulates a Mixture of Experts (MoE) architecture logic.
    1. The Router (Gating Network) analyzes the input.
    2. The input is dispatched ONLY to the specialized 'Expert' weights.
    3. The response is generated without activating irrelevant parts of the brain.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast routing
    model_name = "llama-3.1-8b-instant"

    # Incoming request
    query = "Write a Python function to calculate the Fibonacci sequence."

    print("-" * 50)
    print("INCOMING TOKEN STREAM...")
    print(f"INPUT: '{query}'")
    print("-" * 50)

    # STEP 1: THE ROUTER (Sparse Gating)
    # This simulates the internal gating network that selects the top-K experts.
    routing_prompt = (
        "Classify this query into one of these three expert domains. "
        "Output ONLY the word: MATH, CODE, or CREATIVE.\n\n"
        f"Query: {query}"
    )
    
    print("ROUTING: Analyzing features for expert selection...")
    
    try:
        router_decision = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": routing_prompt}],
            temperature=0
        ).choices[0].message.content.strip()
        
        # Cleanup in case the model returns extra words
        router_decision = router_decision.upper().replace(".", "")
        print(f"GATING NETWORK: Top Expert Selected -> [{router_decision}]")
        print("-" * 50)

        # STEP 2: EXPERT ACTIVATION (Conditional Computation)
        expert_system_prompts = {
            "CODE": "You are a Senior Software Engineer. You write clean, performant Python code.",
            "MATH": "You are a Mathematician. You focus on algorithmic complexity and mathematical proofs.",
            "CREATIVE": "You are a Creative Writer. You use poetic analogies to explain technical concepts."
        }

        # Select the 'Sparse' path
        system_prompt = expert_system_prompts.get(router_decision, "You are a helpful assistant.")

        print(f"ACTIVATING EXPERT: {router_decision}")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.2
        ).choices[0].message.content.strip()
        
        print("EXPERT RESPONSE:")
        print("-" * 25)
        print(response)
        print("-" * 25)

    except Exception as e:
        print(f"Error during MoE simulation: {e}")

    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("In a real MoE model (like GPT-4 or Mixtral), this routing")
    print("happens at EVERY layer for EVERY token. Only a fraction of the")
    print("parameters are active at any time, which is why massive models")
    print("can be surprisingly fast and cheap to run.")
    print("-" * 50)

if __name__ == "__main__":
    run_moe_simulation()
