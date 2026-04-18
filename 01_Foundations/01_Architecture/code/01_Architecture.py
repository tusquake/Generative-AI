# architecture_intuition.py
# Topic 1: Architecture Intuition - The Engine of LLMs

def simulate_attention_logic():
    """
    A simplified simulation of 'Self-Attention'.
    This shows how the model 'prioritizes' certain words to understand others.
    """
    
    # Scenario: Trying to understand the word 'it'
    # "The bank denied the loan because it was too risky."
    
    sentence = "The bank denied the loan because it was too risky"
    words = sentence.split()
    
    # These scores represent how much the model 'attends' to each word 
    # when processing the word 'it' (index 6)
    # In a real model, these are calculated using math (Dot Products)
    attention_scores = {
        "The": 0.05,
        "bank": 0.15,
        "denied": 0.05,
        "loan": 0.55,    # KEY: 'it' refers most strongly to the 'loan'
        "because": 0.02,
        "it": 0.00,      # A word doesn't usually attend to itself
        "was": 0.03,
        "too": 0.05,
        "risky": 0.10    # KEY: 'risky' provides the reason *why* 'it' is the subject
    }

    print(f"Target Word context analysis: 'it'")
    print("=" * 45)
    print(f"{'WORD':<12} | {'IMPORTANCE SCORE'}")
    print("-" * 45)
    
    for word in words:
        score = attention_scores.get(word, 0.01)
        # Create a visual bar for the score
        bar = "█" * int(score * 20)
        print(f"{word:<12} | {bar} ({score*100:>2.0f}%)")

    print("\n" + "=" * 45)
    print("ENGINEERING TAKEAWAY:")
    print("This 'Attention' mechanism is why LLMs don't get lost in long")
    print("sentences. They can 'link' words regardless of distance.")
    print("=" * 45)

if __name__ == "__main__":
    simulate_attention_logic()
