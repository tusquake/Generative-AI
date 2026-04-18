import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_rag_fundamentals_demo():
    """
    Demonstrates the core RAG (Retrieval Augmented Generation) cycle:
    1. Retrieval: Finding relevant information from a local 'database'.
    2. Generation: Using that information to ground the model's response.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast grounded generation
    model_name = "llama-3.1-8b-instant"

    # PHASE 1: RETRIEVAL (Reading from external .md file)
    kb_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base.md")
    
    try:
        with open(kb_path, "r") as f:
            kb_content = f.read()
    except FileNotFoundError:
        print(f"Error: {kb_path} not found")
        return

    user_query = "What is the policy on home office deductions and Vacations policy?"

    print("-" * 50)
    print(f"QUERY: {user_query}")
    print("ACTION: Retrieving context from external file...")
    
    # Simple 'retrieval' logic: Find the line containing the keyword
    retrieved_context = "Information not found."
    for line in kb_content.split("\n"):
        if "TAX_POLICY" in line:
            retrieved_context += line.strip("- ").strip() + "\n"
        elif "VACATION_POLICY" in line:
            retrieved_context += line.strip("- ").strip() + "\n"
        elif "REMOTE_WORK" in line:
            retrieved_context += line.strip("- ").strip() + "\n"
            
    print(f"RETRIEVED CONTEXT: {retrieved_context}")
    print("-" * 50)

    # PHASE 2: GENERATION (Grounded)
    # We pass the retrieved context into the prompt to ensure the model 
    # answers based on our facts, not its training data.
    prompt = f"""
    You are a corporate HR assistant. 
    Use the provided CONTEXT to answer the USER QUERY.
    If the answer is not in the context, say 'I do not know.'
    
    CONTEXT: {retrieved_context}
    USER QUERY: {user_query}
    
    Answer:
    """

    print("ACTION: Generating grounded response...")
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0 # Setting to 0.0 minimizes creative 'drift'
        )
        print("-" * 50)
        print(f"HR RESPONSE: {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("RAG bridges the gap between the model's static training data")
    print("and your dynamic, private business facts.")
    print("By 'grounding' the answer in retrieved text, we eliminate")
    print("hallucinations and provide verifiable information.")
    print("-" * 50)

if __name__ == "__main__":
    run_rag_fundamentals_demo()
