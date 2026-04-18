import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_dsp_demo():
    """
    Demonstrates Directional Stimulus Prompting (DSP) by using 
    specific keywords to steer the model's attention toward 
    particular sections of a long text.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # Using llama-3.1-8b-instant for rapid focused extraction
    model_name = "llama-3.1-8b-instant"

    contract_text = """
    SECTION 1: PARTIES. This agreement is between AI Corp and User Inc...
    SECTION 2: PAYMENT. User Inc shall pay $500/month on the 1st of every month...
    SECTION 3: LIABILITY. AI Corp is not liable for data loss caused by solar flares...
    SECTION 4: TERMINATION. Either party can cancel with 30 days notice...
    """

    # We can change this 'stimulus' based on the user's focus
    current_stimulus = "Termination, cancellation, and notice periods"

    # THE DSP PATTERN
    # We provide the stimulus separately to 'prime' the attention mechanism.
    prompt = f"""
    Document: {contract_text}
    
    Directional Stimulus Keywords: {current_stimulus}
    
    Task: Summarize the document above. 
    IMPORTANT: Provide deep detail ONLY for sections related to the stimulus keywords. 
    Ignore all other sections.
    """

    print("-" * 50)
    print(f"RUNNING DSP SUMMARIZER (Focus: {current_stimulus})")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error during generation: {e}")
        
    print("-" * 50)
    print("INSIGHT:")
    print("DSP acts like a 'spotlight' on a large block of text.")
    print("It ensures the model doesn't suffer from 'Primacy Bias' or")
    print("'Recency Bias' by explicitly telling it what keywords matter.")
    print("-" * 50)

if __name__ == "__main__":
    run_dsp_demo()
