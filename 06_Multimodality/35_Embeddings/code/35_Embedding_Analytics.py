import os
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

def cosine_similarity(a, b):
    """Calculates the cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(client, text):
    """Helper to extract the embedding vector from a single string."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def run_embedding_analytics_demo():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env")
        return

    client = genai.Client(api_key=api_key)

    print("-" * 50)
    print("TASK 1: ZERO-SHOT CLASSIFICATION")
    print("-" * 50)

    ticket = "I need to reset my password, the login screen is frozen."
    categories = ["Billing", "Technical Support", "Shipping", "Security"]

    ticket_vec = get_embedding(client, ticket)
    category_vecs = {cat: get_embedding(client, cat) for cat in categories}

    print(f"Ticket: '{ticket}'")
    best_match = None
    highest_score = -1

    for cat, vec in category_vecs.items():
        score = cosine_similarity(ticket_vec, vec)
        print(f"  > Similarity to '{cat}': {score:.4f}")
        if score > highest_score:
            highest_score = score
            best_match = cat

    print(f"\nRESULT: Classification -> [{best_match}]")
    print("-" * 50)

    print("\nTASK 2: SEMANTIC ANOMALY DETECTION")
    print("-" * 50)

    dataset = [
        "The cat sat on the mat.",
        "A kitten is resting on the rug.",
        "Feline companions enjoy sleeping on carpets.",
        "Quantum entanglement occurs at subatomic levels."  # THE ANOMALY
    ]

    vecs = [get_embedding(client, text) for text in dataset]
    centroid = np.mean(vecs, axis=0)

    print("Calculating semantic distance from group average...")
    for i, text in enumerate(dataset):
        score = cosine_similarity(vecs[i], centroid)
        is_anomaly = " [ANOMALY DETECTED]" if score < 0.6 else ""
        print(f"  > Score: {score:.4f} | Text: '{text[:40]}...'{is_anomaly}")

    print("-" * 50)
    print("INSIGHT:")
    print("Embeddings allow us to perform classification and")
    print("anomaly detection without any training. By calculating")
    print("distances in vector space, we can identify things that")
    print("simply 'don't belong' in a conversation.")
    print("-" * 50)

if __name__ == "__main__":
    run_embedding_analytics_demo()