import os

def get_efficient_model(user_query: str):
    """
    Simulates a logic-based router that decides between 
    a cheap 'Flash' model and a premium 'Pro' model.
    """
    # Heuristic: Complex tasks involving code or math are routed to Pro
    complex_keywords = ["analyze", "code", "debug", "architect", "math", "logic", "proof"]
    
    query_lower = user_query.lower()
    
    if any(k in query_lower for k in complex_keywords) or len(user_query) > 1000:
        return "gemini-1.5-pro"  # Higher reasoning, higher cost
    
    return "gemini-1.5-flash"   # Fast, extremely cheap

def run_routing_demo():
    print("-" * 50)
    print("🤖 INTELLIGENT MODEL ROUTER")
    print("-" * 50)
    
    test_queries = [
        "What is the weather in Paris?",
        "Write a Python script to handle recursive file deletions with error logging.",
        "Summarize this email.",
        "Solve for x: 3x^2 + 5x - 2 = 0"
    ]

    for q in test_queries:
        model = get_efficient_model(q)
        cost_savings = "90% cheaper" if "flash" in model else "Full cost"
        
        print(f"QUERY: '{q[:50]}...'")
        print(f"ROUTED TO: {model} ({cost_savings})")
        print("-" * 30)

    print("[Senior Note] Routing doesn't just save money; it also improves "
          "latency for simple queries by avoiding the overhead of large models.")

if __name__ == "__main__":
    run_routing_demo()
