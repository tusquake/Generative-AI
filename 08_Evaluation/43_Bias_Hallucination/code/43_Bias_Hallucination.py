import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def run_grounding_verification_demo():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    context = "The company revenue in 2023 was $4.5 Million, a 10% increase from 2022."
    
    # ⭐ THE GROUNDED PROMPT
    prompt = f"""
    Answer the following question ONLY using the context provided.
    If the answer is not in the context, say 'Information not found.'
    
    CONTEXT: {context}
    QUESTION: What was the revenue in 2021?
    
    ANSWER:
    """

    print("Gemini is checking the data for factual grounding...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    
    print("-" * 50)
    print(f"AI Response: {response.text.strip()}")
    print("-" * 50)
    print("[Senior Note] By providing a 'Negative Constraint', "
          "we successfully prevented the model from 'Guiding' an answer "
          "about 2021.")

if __name__ == "__main__":
    run_grounding_verification_demo()
