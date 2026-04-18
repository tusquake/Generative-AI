import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_system_prompt_demo():
    """
    Demonstrates the power of System Prompts in defining model behavior.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    genai.configure(api_key=api_key)

    # 1. Define the System Instruction (The 'Constitution' of the model)
    system_rules = """
    You are a professional Python Senior Engineer. 
    You only speak in clear, concise technical terms. 
    You are forbidden from being conversational or using emojis.
    Always provide a Big-O complexity analysis for every code snippet.
    """

    # Using gemini-2.5-flash for latest compatibility
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_rules
    )

    # 2. The User Input (The specific request)
    user_input = "Write a function to reverse a string."

    print("-" * 40)
    print(f"USER REQUEST: {user_input}")
    print("-" * 40)

    try:
        response = model.generate_content(user_input)
        print(f"ENGINEER RESPONSE:\n{response.text.strip()}")
    except Exception as e:
        print(f"Error during generation: {e}")

    print("-" * 40)
    print("INSIGHT:")
    print("Notice how the model completely skipped 'Hello!' or 'Sure!'")
    print("The system prompt forced it into a pure technical persona.")
    print("-" * 40)

if __name__ == "__main__":
    run_system_prompt_demo()
