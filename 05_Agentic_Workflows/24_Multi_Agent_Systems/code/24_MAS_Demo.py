import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_mas_demo():
    """
    Demonstrates a basic Multi-Agent System (MAS) pattern:
    1. Agent 1 (Writer): Generates initial content.
    2. Agent 2 (Critic): Reviews the content for accuracy/quality.
    
    This simulates the 'Specialist' advantage where different models 
    focus on specific aspects of a task.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for fast multi-agent turns
    model_name = "llama-3.1-8b-instant"

    print("-" * 50)
    print("STARTING MULTI-AGENT COLLABORATION")
    print("-" * 50)

    # TURN 1: THE WRITER
    writer_prompt = "You are a creative writer. Write a 2-sentence story about a robot on Mars."
    
    print("AGENT 1 (Writer): Generating story...")
    try:
        response_1 = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": writer_prompt}],
            temperature=0.8
        )
        story = response_1.choices[0].message.content.strip()
        print(f"STORY:\n{story}\n")

        # TURN 2: THE CRITIC
        # We pass the Writer's output to the Critic for a 'Second Opinion'
        critic_prompt = f"""
        You are a Strict Editor. 
        Review the story below for scientific accuracy and narrative flow. 
        If there are errors, provide 1 specific fix.
        
        STORY: {story}
        """
        
        print("AGENT 2 (Critic): Reviewing story...")
        response_2 = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": critic_prompt}],
            temperature=0.0 # Setting to 0.0 for objective critique
        )
        review = response_2.choices[0].message.content.strip()
        
        print(f"REVIEW:\n{review}")
        print("-" * 50)
        
    except Exception as e:
        print(f"Error during agent interaction: {e}")

    print("INSIGHT:")
    print("By splitting 'Writing' and 'Critiquing' into two different agents,")
    print("we reduce the 'Primacy bias' where a single model is afraid to")
    print("correct its own mistakes. This adversarial loop drives quality.")
    print("-" * 50)

if __name__ == "__main__":
    run_mas_demo()
