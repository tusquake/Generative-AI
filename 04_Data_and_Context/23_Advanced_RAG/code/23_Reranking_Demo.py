import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_advanced_rag_demo():
    """
    Simulates an Advanced RAG 'Reranking' pass. 
    Standard RAG retrieves candidates based on vector similarity. 
    Advanced RAG re-ranks those candidates using a smarter model 
    (Cross-Encoder) to ensure the highest-signal chunk is at the top.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant to act as a fast auditor
    model_name = "llama-3.1-8b-instant"

    query = "What are the rules for returning custom t-shirts?"

    # Simulation of diverse (noisy) retrieval results from a Vector DB.
    # Note that Document B and D are relevant to t-shirts/shipping but 
    # don't answer the specific question about 'custom' returns.
    candidates = [
        "Document A: Refunds for standard items are 30 days.",
        "Document B: Our t-shirts are made of 100% organic cotton.",
        "Document C: Custom items cannot be returned unless the print is defective.",
        "Document D: We ship globally from our warehouse in Texas."
    ]

    # THE RERANKING PROMPT
    # We ask the model to analyze the semantic relevance of each candidate.
    rerank_prompt = f"""
    You are a Reranking Auditor in a RAG pipeline.
    
    User Query: {query}
    
    Retrieved Candidates:
    {candidates}

    Task:
    1. Re-order these candidates from 1 to 4 (most relevant to least relevant).
    2. Identify the 'Winning' document.
    3. Explain why the winner is more relevant than the other documents.
    """

    print("-" * 50)
    print("EXECUTING RERANKING PASS (Simulated Cross-Encoder)")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": rerank_prompt}],
            temperature=0.0
        )
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("Vector similarity often returns 'relevant-ish' noise.")
    print("A Reranker pass ensures the LLM generator receives only")
    print("the absolute best context, reducing distractions and cost.")
    print("-" * 50)

if __name__ == "__main__":
    run_advanced_rag_demo()
