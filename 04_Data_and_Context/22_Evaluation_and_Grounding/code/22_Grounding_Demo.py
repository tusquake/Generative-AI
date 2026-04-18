import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_grounding_demo():
    """
    Demonstrates Grounding by forcing the model to cite specific 
    sources from the provided context. This ensures the model 
    remains faithful to the retrieved data.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast grounded generation
    model_name = "llama-3.1-8b-instant"

    # Simulation: Data retrieved from a knowledge base
    retrieved_data = """
    Document 1: The refund policy for standard items is 30 days.
    Document 2: Custom items are non-refundable unless defective.
    Document 3: Customer support hours are 9 AM to 5 PM EST.
    """

    user_query = "Can I return a custom-made t-shirt?"

    # THE GROUNDING PROMPT
    # We use strict rules and source tags to anchor the model's logic.
    prompt = f"""
    You are a Customer Support Agent. Answer the question ONLY using the provided context.
    
    CONTEXT:
    {retrieved_data}

    RULES:
    1. If the info isn't in the context, say 'I cannot answer this with the current data.'
    2. Provide a source tag e.g. [Document X] for every claim you make.
    3. Be concise.

    USER QUERY: {user_query}
    
    GROUNDED ANSWER:
    """

    print("-" * 50)
    print("GENERATING GROUNDED ANSWER WITH CITATIONS")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("Grounding transforms a stochastic model into a verifiable engine.")
    print("By requiring citations (e.g., [Document 2]), we enable users")
    print("and developers to audit the AI's logic against source truths.")
    print("-" * 50)

if __name__ == "__main__":
    run_grounding_demo()
