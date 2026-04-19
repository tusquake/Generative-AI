import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_ai_architecture(scenario_title, scenario_text):
    """
    Simulates an architectural decision engine to choose between RAG and Fine-Tuning.
    RAG = External Knowledge (Open Book)
    Fine-Tuning = Internal Skill (Studied)
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    model_name = "llama-3.1-8b-instant"

    print("-" * 50)
    print(f"EVALUATING SCENARIO: {scenario_title}")
    print(f"DETAILS: {scenario_text}")
    print("-" * 50)

    prompt = f"""
    You are a Senior AI Architect. Analyze the following scenario and recommend 
    either RAG (Retrieval-Augmented Generation), Fine-Tuning (FT), or a Hybrid approach.
    
    SCENARIO: {scenario_text}
    
    Structure your answer as follows:
    1. RECOMMENDED PATTERN: [Selection]
    2. ARCHITECTURAL RATIONALE: [Why this fits the data dynamics]
    3. DATA REQUIREMENT: [What kind of dataset is needed?]
    4. PRIMARY RISK: [What is the biggest technical challenge?]
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        ).choices[0].message.content.strip()
        
        print(response)
        
    except Exception as e:
        print(f"Error during architectural analysis: {e}")

    print("\n" + "-" * 50)
    print("MINTOR INSIGHT:")
    print("RAG is best for FACTS that change daily.")
    print("Fine-Tuning is best for STYLE or FORMAT that is static.")
    print("-" * 50)

if __name__ == "__main__":
    # Case 1: Dynamic Knowledge
    analyze_ai_architecture(
        "Financial News Bot", 
        "The bot needs to answer questions about stock price movements happening every hour."
    )
    
    print("\n")
    
    # Case 2: Specialized Formatting
    analyze_ai_architecture(
        "Legal Document Formatter", 
        "The AI must convert standard text into a highly specific, proprietary legal XML schema used by our 1980s mainframe."
    )
