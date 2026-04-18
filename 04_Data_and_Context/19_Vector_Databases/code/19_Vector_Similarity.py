import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def cosine_similarity(v1, v2):
    """Calculates the cosine similarity between two vectors."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def run_embeddings_demo():
    """
    Demonstrates how embeddings represent semantic meaning using Gemini.
    If the API is unavailable, it falls back to a mathematical simulation.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    use_simulation = False

    if not api_key:
        print("Warning: GEMINI_API_KEY not found. Switching to Simulation Mode.")
        use_simulation = True
    else:
        genai.configure(api_key=api_key)

    sentences = [
        "The weather is beautiful today.",           # Index 0
        "It's a sunny and lovely day outside.",       # Index 1 (Similar to 0)
        "Artificial Intelligence is changing the world.", # Index 2
        "Deep learning models require massive data."  # Index 3 (Similar to 2)
    ]

    print("-" * 50)
    print("VECTOR SIMILARITY DEMO")
    print("-" * 50)

    embeddings = []

    if not use_simulation:
        try:
            print("Generating embeddings via Gemini API...")
            # Using text-embedding-004
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=sentences,
                task_type="retrieval_document"
            )
            embeddings = result['embedding']
        except Exception as e:
            print(f"API Error: {e}")
            print("Switching to Mathematical Simulation Mode...")
            use_simulation = True

    if use_simulation:
        # SIMULATION: We create synthetic vectors where specific dimensions 
        # represent 'Weather' vs 'Tech' topics.
        print("SIMULATION MODE: Generating synthetic semantic vectors...")
        # Weather Vector: [Weather_Signal, Tech_Signal, Random_Noise...]
        embeddings = [
            [0.9, 0.1, 0.05], # Weather 1
            [0.85, 0.15, 0.02], # Weather 2 (Close to Weather 1)
            [0.1, 0.95, 0.01], # Tech 1
            [0.2, 0.88, 0.08]  # Tech 2 (Close to Tech 1)
        ]

    # Test 1: Similar weather sentences
    score_1 = cosine_similarity(embeddings[0], embeddings[1])
    print(f"\nComparing: '{sentences[0]}'")
    print(f"With:      '{sentences[1]}'")
    print(f"Similarity Score: {score_1:.4f} (High Similarity)")

    # Test 2: Similar Tech sentences
    score_2 = cosine_similarity(embeddings[2], embeddings[3])
    print(f"\nComparing: '{sentences[2]}'")
    print(f"With:      '{sentences[3]}'")
    print(f"Similarity Score: {score_2:.4f} (High Similarity)")

    # Test 3: Unrelated sentences
    score_3 = cosine_similarity(embeddings[0], embeddings[2])
    print(f"\nComparing: '{sentences[0]}'")
    print(f"With:      '{sentences[2]}'")
    print(f"Similarity Score: {score_3:.4f} (Low Similarity)")

    print("-" * 50)
    print("INSIGHT:")
    print("Standard databases search for EXACT matches (Keyword).")
    print("Vector databases search for PROXIMITY (Meaning).")
    print("This allows us to find 'Sunny Day' even if we searched for 'Weather'.")
    print("-" * 50)

if __name__ == "__main__":
    run_embeddings_demo()
