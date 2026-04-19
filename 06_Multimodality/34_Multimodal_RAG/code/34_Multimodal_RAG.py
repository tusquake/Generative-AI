import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def run_multimodal_rag_demo():
    """
    Demonstrates Multimodal RAG (Retrieval-Augmented Generation).
    1. Retrieval: In a production app, we would use a Vector Database to 
       find images that match a user's text query (using CLIP or SigLIP).
    2. Augmentation: We pass the retrieved image + query to a Vision-LLM.
    3. Generation: The model 'Grounds' its answer in the specific pixels found.
    """
    # Setup Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env")
        return
        
    genai.configure(api_key=api_key)
    # Using Flash for speed and efficiency in RAG workflows
    model = genai.GenerativeModel('gemini-1.5-flash')

    # STEP 1: RETRIEVAL (Simulated)
    # We are simulating a search for 'High Protein / Low Sodium' products.
    # The Vector DB has retrieved our 'vision_sample.png' as the top match.
    image_path = "vision_sample.png"
    
    # Check if the asset from Topic 29 exists
    if not os.path.exists(image_path):
        print("-" * 50)
        print(f"ASSET MISSING: {image_path}")
        print("Please run Topic 29 (Vision Demo) first to generate the nutrition label.")
        print("-" * 50)
        return
        
    img = Image.open(image_path)

    # STEP 2: USER QUERY
    user_query = "Find me a heart-healthy snack. Is this retrieved product a good match?"

    # STEP 3: AUGMENTED PROMPT
    # We guide the model to perform 'Visual Grounding'
    prompt = f"""
    You are a Multimodal Search Evaluator.
    
    RETRIEVED ASSET: Nutrition Label Image
    USER INTENT: {user_query}
    
    TASK:
    1. Analyze the Sodium and Saturated Fat content in the image.
    2. Compare these values to heart-healthy standards (e.g., Sodium < 140mg per serving).
    3. Final Verdict: 'MATCH' or 'NO MATCH'.
    4. Explanation: Why did you make this choice?
    """

    print("-" * 50)
    print(f"SIMULATED RETRIEVAL: Found {image_path}")
    print(f"QUERY: {user_query}")
    print("-" * 50)
    print("AI EVALUATION (Visual Grounding)...")

    try:
        # Multi-modal input: list of [text, image]
        response = model.generate_content([prompt, img])
        
        print("-" * 50)
        print("MULTIMODAL RAG RESULT:")
        print(response.text.strip())
        print("-" * 50)
        
    except Exception as e:
        print(f"Error during Multimodal RAG: {e}")
        print("Note: Ensure your GOOGLE_API_KEY is valid and has vision quota.")

    print("\nINSIGHT:")
    print("Multimodal RAG solves the 'Dark Data' problem. Without it,")
    print("images and PDFs with charts are invisible to traditional search.")
    print("By indexing visual features, we can search by the 'Meaning'")
    print("of an image rather than just its filename.")
    print("-" * 50)

if __name__ == "__main__":
    run_multimodal_rag_demo()
