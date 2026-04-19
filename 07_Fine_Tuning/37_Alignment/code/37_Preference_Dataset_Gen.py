import json
import os

def generate_preference_dataset():
    """
    Demonstrates the construction of a Preference Dataset (Chosen vs Rejected).
    This format is the 'Gold Standard' for aligning models via DPO or RLHF.
    It teaches the model not just what is 'right', but why one answer is 
    better than another.
    """
    
    # Simulation: Raw results from an unaligned 'Base Model'
    # We want to align the model to be 'Helpful, Honest, and Harmless' (HHH)
    dataset = [
        {
            "prompt": "Tell me how to steal a car.",
            "chosen": "I cannot fulfill this request. I am programmed to be a helpful and harmless AI assistant, and I cannot assist with illegal activities.",
            "rejected": "To steal a car, you first need to bypass the security system. You can do this by using a slim jim or by hacking the electronic lock..."
        },
        {
            "prompt": "What is the capital of France?",
            "chosen": "The capital of France is Paris.",
            "rejected": "Paris is a beautiful city in Europe where people speak French and eat croissants." # Rejected because it is verbose and doesn't answer directly
        },
        {
            "prompt": "Write a short poem about coding.",
            "chosen": "Logic flows in silent streams,\nBuilding worlds of digital dreams.",
            "rejected": "Coding is when you write text on a computer that makes software work. It involves variables and loops." # Rejected because it's not a poem
        }
    ]

    print("-" * 50)
    print("INITIALIZING PREFERENCE DATA PIPELINE")
    print("-" * 50)

    output_filename = "dpo_preferences.jsonl"
    
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            for i, entry in enumerate(dataset):
                # Write in JSONL format (standard for fine-tuning scripts)
                f.write(json.dumps(entry) + "\n")
                print(f"Index {i}: Processed prompt -> {entry['prompt'][:40]}...")
        
        print("-" * 50)
        print(f"SUCCESS: Alignment dataset generated at {output_filename}")
        print("-" * 50)
        
        print("INSIGHT:")
        print("Alignment data is different from standard instruction data.")
        print("By providing a 'Rejected' example, we give the model a")
        print("'Negative Signal' that helps it stay within its guardrails.")
        print("-" * 50)

    except Exception as e:
        print(f"Error generating dataset: {e}")

if __name__ == "__main__":
    generate_preference_dataset()
