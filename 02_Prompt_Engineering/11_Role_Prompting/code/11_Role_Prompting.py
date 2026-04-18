import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_role_prompting_demo():
    """
    Demonstrates how assigning different roles changes the model's 
    vocabulary, tone, and focus for the same technical concept.
    Uses Groq as a fallback for the leaked Gemini key.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model_name = "llama-3.1-8b-instant"

    concept = "Microservices Architecture"

    # Persona 1: The Educator (Focus on Analogies)
    prompt_1 = f"You are a friendly 10-year veteran teacher. Explain {concept} using a LEGO analogy."

    # Persona 2: The Architect (Focus on Trade-offs)
    prompt_2 = f"You are a Principal Software Architect. Explain {concept} in terms of scalability, database sharding, and fault tolerance."

    print("-" * 50)
    print("CONCEPT: " + concept)
    print("-" * 50)

    try:
        print("PERSONA: TENURED TEACHER")
        print("-" * 25)
        response_1 = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt_1}]
        )
        print(response_1.choices[0].message.content.strip())
        
        print("\n" + "=" * 50 + "\n")

        print("PERSONA: PRINCIPAL ARCHITECT")
        print("-" * 25)
        response_2 = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt_2}]
        )
        print(response_2.choices[0].message.content.strip())
        
    except Exception as e:
        print(f"Error during generation: {e}")

    print("-" * 50)
    print("INSIGHT:")
    print("The Teacher used LEGOs to explain modularity.")
    print("The Architect used technical jargon like 'sharding' and 'fault tolerance'.")
    print("Roles effectively filter the model's vast knowledge for specific audiences.")
    print("-" * 50)

if __name__ == "__main__":
    run_role_prompting_demo()
