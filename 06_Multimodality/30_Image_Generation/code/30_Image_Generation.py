import os
from PIL import Image
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

def run_image_gen_demo():
    """
    Demonstrates Image Generation using Stable Diffusion XL.
    This script uses the Hugging Face Inference API to:
    1. Send a text prompt to a Diffusion model.
    2. Receive a generated image (Reverse Diffusion process).
    3. Save the result locally for inspection.
    """
    # Setup HF Client
    # We use the token from .env to authenticate with the Inference API
    hf_token = os.getenv("HUGGING_FACE_API_KEY")
    if not hf_token:
        print("Error: HUGGING_FACE_API_KEY not found in .env")
        return
        
    client = InferenceClient(api_key=hf_token)

    # A detailed prompt helps the diffusion model 'sculpt' the noise effectively
    prompt = "A high-tech research lab on the moon, large glass windows looking at Earth, cinematic lighting, 8k resolution."

    print("-" * 50)
    print("STARTING IMAGE GENERATION (STABLE DIFFUSION XL)")
    print(f"PROMPT: {prompt}")
    print("-" * 50)
    
    try:
        # The text_to_image function sends the prompt to the HF API
        # and returns a PIL Image object upon completion.
        print("Requesting pixels from the model...")
        image = client.text_to_image(
            prompt,
            model="runwayml/stable-diffusion-v1-5"
        )
        
        # Save the image relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "moon_lab.png")
        image.save(output_path)
        
        print("-" * 50)
        print(f"SUCCESS: Image saved to {output_path}")
        print("-" * 50)
        
    except Exception as e:
        print(f"Error during image generation: {e}")
        print("Note: Ensure your HUGGING_FACE_API_KEY is valid and has access.")

    print("INSIGHT:")
    print("Diffusion models don't 'look up' images; they use a")
    print("learned probability distribution to turn random noise into")
    print("coherent structures that match your text description.")
    print("-" * 50)

if __name__ == "__main__":
    run_image_gen_demo()
