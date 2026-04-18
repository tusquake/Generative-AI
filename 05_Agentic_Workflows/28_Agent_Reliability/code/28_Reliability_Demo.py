import os
from collections import Counter
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def run_reliability_demo():
    """
    Demonstrates the 'Self-Consistency' (Majority Voting) pattern.
    Probabilistic models can make 'slips' in complex reasoning.
    By running the task multiple times (N=3) and taking the 
    most frequent answer, we statistically improve reliability.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = Groq(api_key=api_key)
    # llama-3.1-8b-instant is fast enough for parallel/multiple runs
    model_name = "llama-3.1-8b-instant"

    # A classic logic puzzle that requires multi-step math
    task = """
    A train leaves Station A at 3:00 PM traveling at 60 mph. 
    Another train leaves Station A at 4:00 PM traveling at 90 mph in the same direction. 
    At what time will the second train overtake the first train?
    
    Format your answer as a single time string (e.g. '6:00 PM').
    """

    print("-" * 50)
    print("STARTING SELF-CONSISTENCY CHECK (N=3)")
    print("-" * 50)

    results = []
    
    for i in range(3):
        print(f"Trial {i+1}: Generating reasoning path...")
        try:
            # We use a moderate temperature (0.7) to allow for 
            # variations in reasoning.
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": task}],
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()
            
            # Simple cleanup to isolate the time if the model provides extra text
            # In production, you would use Regex or a JSON schema.
            results.append(answer)
            print(f"Output: {answer}")
        except Exception as e:
            print(f"Error during trial {i+1}: {e}")

    # CONSENSUS PHASE
    # If the model makes a math error in 1 out of 3 runs, 
    # the majority vote will suppress it.
    if results:
        occurrence_count = Counter(results)
        final_consensus, count = occurrence_count.most_common(1)[0]

        print("-" * 50)
        print(f"CONSENSUS ANSWER: {final_consensus}")
        print(f"CONFIDENCE SCORE: {count}/3")
        print("-" * 50)
    else:
        print("No results generated.")

    print("INSIGHT:")
    print("Self-consistency is the 'Swiss Cheese' model of AI engineering.")
    print("If a mistake slips through one reasoning path, the other")
    print("two independent runs act as a safety net.")
    print("-" * 50)

if __name__ == "__main__":
    run_reliability_demo()
