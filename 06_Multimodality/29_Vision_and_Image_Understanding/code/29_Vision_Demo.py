import os
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

load_dotenv()

def run_vlm_demo():
    """
    Demonstrates Vision-Language Model (VLM) reasoning:
    1. Loads a real image (generated protein bar label).
    2. Passes the image + text instructions to Gemini 1.5.
    3. Model performs 'Visual Reasoning' to extract data and assess suitability.
    """
    # Setup Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env")
        return
        
    genai.configure(api_key=api_key)
    # Gemini 1.5 Flash is highly optimized for fast multimodal analysis
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Path to the image file (relative to the code directory)
    # Note: When running in Docker, ensure the path is correct.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'vision_sample.png')
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    print("-" * 50)
    print(f"OPENING IMAGE: {os.path.basename(image_path)}")
    print("-" * 50)
    
    img = PIL.Image.open(image_path)

    prompt = """
    You are a nutrition analyst. Look at this product label and:
    1. Identify the brand name.
    2. Extract the total calories per serving.
    3. Is this product suitable for someone on a strict low-sodium diet? Explain why based on the sodium content visible.
    """

    print("RUNNING VISUAL REASONING TASK...")
    
    try:
        # Gemini accepts a list of [text_prompt, image_object]
        response = model.generate_content([prompt, img])
        
        print("-" * 50)
        print("GEMINI VISION ANALYSIS:")
        print("-" * 25)
        print(response.text.strip())
        print("-" * 50)
    except Exception as e:
        print(f"Error during vision generation: {e}")

    print("INSIGHT:")
    print("Gemini doesn't just 'read' the text via OCR; it 'understands'")
    print("the context of the label. It can reason about the nutritional")
    print("implications of the numbers it sees, bridging pixels and logic.")
    print("-" * 50)

if __name__ == "__main__":
    run_vlm_demo()
