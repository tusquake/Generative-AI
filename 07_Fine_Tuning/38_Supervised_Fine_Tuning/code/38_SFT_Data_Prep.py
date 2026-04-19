import json
import random
import os

def prepare_sft_dataset():
    """
    Demonstrates the preparation of a Supervised Fine-Tuning (SFT) dataset.
    1. Mapping raw knowledge into ChatML format.
    2. Splitting data into Training and Validation sets.
    3. Calculating token counts (simulated) for cost estimation.
    """
    
    # Raw domain knowledge (e.g., specific coding styles or internal rules)
    raw_knowledge = [
        {
            "instruction": "Convert this timestamp to ISO 8601.",
            "input": "April 19, 2026, 9:00 AM",
            "output": "2026-04-19T09:00:00Z"
        },
        {
            "instruction": "Explain the company policy on remote work.",
            "input": "",
            "output": "Our policy allows for 3 days of remote work per week with manager approval."
        },
        {
            "instruction": "Refactor this code to use a list comprehension.",
            "input": "result = []\nfor x in items:\n    result.append(x * 2)",
            "output": "result = [x * 2 for x in items]"
        },
        {
            "instruction": "What is the emergency protocol for server downtime?",
            "input": "",
            "output": "Contact the DevOps On-Call engineer and create a P0 incident ticket immediately."
        }
    ]

    print("-" * 50)
    print("SFT DATA PIPELINE: RAW TO CHATML")
    print("-" * 50)

    # 1. Transform to ChatML (The modern industry standard)
    formatted_dataset = []
    for entry in raw_knowledge:
        # Combine instruction and input if input exists
        user_content = entry["instruction"]
        if entry["input"]:
            user_content += f"\n\nInput: {entry['input']}"
            
        chat_entry = {
            "messages": [
                {"role": "system", "content": "You are a specialized enterprise assistant."},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": entry["output"]}
            ]
        }
        formatted_dataset.append(chat_entry)

    # 2. Validation Split (In real SFT, we need a 'Held-out' set to detect overfitting)
    random.shuffle(formatted_dataset)
    split_point = int(len(formatted_dataset) * 0.75) # 75/25 split
    
    train_set = formatted_dataset[:split_point]
    val_set = formatted_dataset[split_point:]

    # 3. Save to JSONL files
    files = {
        "sft_train.jsonl": train_set,
        "sft_validation.jsonl": val_set
    }

    for filename, data in files.items():
        with open(filename, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")
        print(f"CREATED: {filename} ({len(data)} samples)")

    print("-" * 50)
    print("SFT COST ESTIMATION:")
    # Rough estimate: ~100 tokens per sample
    total_samples = len(formatted_dataset)
    estimated_tokens = total_samples * 150 
    print(f"Total Samples: {total_samples}")
    print(f"Estimated Training Tokens: ~{estimated_tokens}")
    print("-" * 50)

    print("INSIGHT:")
    print("SFT is the 'Content Phase' of fine-tuning. Unlike RLHF,")
    print("which teaches the model 'preferences', SFT teaches it")
    print("the specific mapping between a prompt and a target output.")
    print("-" * 50)

if __name__ == "__main__":
    prepare_sft_dataset()
