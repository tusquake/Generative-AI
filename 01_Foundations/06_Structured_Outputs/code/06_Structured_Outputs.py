import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()

def run_structured_output_demo():
    """
    Demonstrates how to force the LLM to return valid, schema-compliant JSON.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    genai.configure(api_key=api_key)
    
    # 1. Define the Schema
    # This acts as a contract that the LLM MUST follow.
    schema = {
        "description": "Product information extraction",
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "price": {"type": "number"},
            "currency": {"type": "string"},
            "in_stock": {"type": "boolean"},
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["product_name", "price", "currency", "in_stock"]
    }

    # 2. Configure the model with JSON Mode + Schema
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": schema
        }
    )

    raw_text = """
    We just launched the 'Zenith Pro' headphones for $199.99. 
    They are currently available in our warehouse. 
    Users love them for their noise-canceling and wireless features.
    """

    print("-" * 40)
    print("RAW TEXT:")
    print(raw_text.strip())
    print("-" * 40)

    try:
        # Generate the structured response
        response = model.generate_content(f"Extract product info from: {raw_text}")
        
        # 3. Parse the valid JSON
        data = json.loads(response.text)
        
        print("STRUCTURED DATA (JSON):")
        print(json.dumps(data, indent=2))
        print("-" * 40)
        
        # Accessing fields like a normal Python dictionary
        print(f"Product: {data['product_name']}")
        print(f"Status: {'Available' if data['in_stock'] else 'Out of Stock'}")
        
    except Exception as e:
        print(f"Failed to generate structured output: {e}")

    print("-" * 40)
    print("INSIGHT:")
    print("The model was forced to return JSON. Even if it wanted to use prose,")
    print("the 'response_mime_type' constraint prevented it.")
    print("-" * 40)

if __name__ == "__main__":
    run_structured_output_demo()
