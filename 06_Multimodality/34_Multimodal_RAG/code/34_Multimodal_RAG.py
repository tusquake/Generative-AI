import os
import google.generativeai as genai
from groq import Groq
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def run_multimodal_rag_demo():
    """
    Demonstrates a Bridge Architecture for Multimodal RAG:
    1. Vision Provider (Gemini): 'Sees' the image and converts it to a structured description.
    2. Logic Provider (Groq): 'Reasons' about the text description with low latency.
    """
    # Setup Keys
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not google_key or not groq_key:
        print("Error: GOOGLE_API_KEY and GROQ_API_KEY must be in .env")
        return

    # Initialize Clients
    genai.configure(api_key=google_key)
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
    groq_client = Groq(api_key=groq_key)

    # Asset Check
    image_path = "vision_sample.png"
    if not os.path.exists(image_path):
        print(f"Asset {image_path} not found. Ensure it was copied to the root.")
        return
    img = Image.open(image_path)

    # 1. VISION PHASE (Gemini)
    print("-" * 50)
    print("PHASE 1: VISUAL FEATURE EXTRACTION (Gemini)")
    print("-" * 50)
    
    vision_prompt = "Extract all text and numerical values from this nutrition label into a clean summary."
    
    extracted_text = ""
    try:
        # We use Gemini as our 'Eyes'
        vision_response = vision_model.generate_content([vision_prompt, img])
        extracted_text = vision_response.text.strip()
        print("Success: Visual data extracted.")
    except Exception as e:
        print(f"Vision API Error: {e}")
        # Fallback for demo purposes if quota is hit
        extracted_text = "Brand: CyberFuel, Calories: 250, Sodium: 450mg, Protein: 20g"
        print("Using Fallback Metadata for reasoning demo.")

    # 2. REASONING PHASE (Groq)
    print("\n" + "-" * 50)
    print("PHASE 2: NATURAL LANGUAGE REASONING (Groq + Llama 3)")
    print("-" * 50)
    
    user_query = "Is this product suitable for a heart-healthy diet (Sodium < 140mg)?"
    
    reasoning_prompt = f"""
    USER QUERY: {user_query}
    EXTRACTED VISUAL DATA:
    ---
    {extracted_text}
    ---
    
    TASK: Based on the extracted data, determine if the product matches the user's intent.
    Provide a concise explanation.
    """

    try:
        # We use Groq as our 'Brain'
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": reasoning_prompt}]
        ).choices[0].message.content.strip()
        
        print(f"GROQ VERDICT:\n{response}")
        
    except Exception as e:
        print(f"Groq Reasoning Error: {e}")

    print("\n" + "-" * 50)
    print("INSIGHT:")
    print("This 'Bridge' pattern is used when your primary model")
    print("is text-only. By using a cheap, fast Vision model (Gemini Flash)")
    print("to generate descriptions, you can leverage high-performance")
    print("LLMs (Groq) for complex retrieval and decision logic.")
    print("-" * 50)

if __name__ == "__main__":
    run_multimodal_rag_demo()
