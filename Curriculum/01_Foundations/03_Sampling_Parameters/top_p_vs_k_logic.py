# top_p_vs_k_logic.py
# Topic 3: Comparison of Top-P and Top-K logic

def simulate_sampling_logic():
    """
    Shows how Top-K (fixed count) and Top-P (dynamic probability)
    filter the list of possible next words.
    """
    
    # Mock probabilities for the next word after "I would like to eat..."
    # (In a real LLM, these are calculated by the model)
    candidates = [
        ("pizza", 0.45),
        ("pasta", 0.30),
        ("sushi", 0.15),
        ("tacos", 0.08),
        ("rocks", 0.02)
    ]
    
    print("-" * 50)
    print("PROMPT: 'I would like to eat...'")
    print("-" * 50)
    print("CANDIDATES AND SCORES:")
    for word, prob in candidates:
        print(f"- {word:8}: {prob*100:>2.0f}%")
    print("-" * 50)

    # 1. TOP-K = 2
    # Rule: Take exactly the top 2 words, no matter what their scores are.
    k = 2
    top_k_pool = [c[0] for c in candidates[:k]]
    print(f"TOP-K ({k}):")
    print(f"Pool = {top_k_pool}")
    print("Result: Only 'pizza' and 'pasta' can be picked.")

    print("\n" + "-" * 50)

    # 2. TOP-P = 0.80 (80%)
    # Rule: Add words one by one until their total score hits 80%.
    p_threshold = 0.80
    current_sum = 0
    top_p_pool = []
    
    for word, prob in candidates:
        top_p_pool.append(word)
        current_sum += prob
        if current_sum >= p_threshold:
            break
            
    print(f"TOP-P ({p_threshold*100:.0f}%):")
    print(f"Pool = {top_p_pool}")
    print(f"Calculation: pizza(45%) + pasta(30%) + sushi(15%) = {current_sum*100:.0f}%")
    print("Result: 'sushi' is included because we needed it to cross the 80% line.")

    print("\n" + "-" * 50)
    print("SUMMARY FOR THE ENGINEER:")
    print("Top-K is a HARD LIMIT on word count.")
    print("Top-P is a DYNAMIC LIMIT based on probability confidence.")
    print("-" * 50)

if __name__ == "__main__":
    simulate_sampling_logic()
