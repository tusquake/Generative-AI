import os
import json
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

def run_automated_judge():
    # Use v1 stable API version
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
        http_options={'api_version': 'v1'}
    )
    
    # The "Student" response we are grading
    student_answer = "The capital of France is Paris, which is home to the Eiffel Tower."
    reference_answer = "Paris is the capital of France."

    # The Rubric (Instruction for the Judge)
    judge_prompt = f"""
    You are an expert Professor. Grade the STUDENT ANSWER based on the REFERENCE ANSWER.
    
    CRITERIA:
    1. Accuracy: Is the fact correct? (Scale 1-5)
    2. Tone: Is it professional? (Scale 1-5)
    
    STUDENT ANSWER: {student_answer}
    REFERENCE ANSWER: {reference_answer}
    
    Return ONLY a JSON object: 
    {{"accuracy": 5, "tone": 5, "justification": "..."}}
    """

    print("Evaluating student response...")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=judge_prompt
        )
        
        print("-" * 50)
        print(f"REPORT CARD:\n{response.text.strip()}")
        print("-" * 50)
    except errors.ClientError as e:
        if "404" in str(e):
            print(f"\n❌ Error: {e.message}")
            print("Listing available models for your API key:")
            try:
                for m in client.models.list():
                    # Clean up the model name (remove 'models/' prefix for display)
                    name = m.name.replace("models/", "")
                    print(f" - {name}")
            except Exception as list_err:
                print(f"Could not list models: {list_err}")
        else:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_automated_judge()
