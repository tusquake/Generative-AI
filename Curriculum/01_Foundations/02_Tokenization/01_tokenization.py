import tiktoken
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key (Optional for this part)
load_dotenv()

def explore_tokenization():
    """
    Demonstrates how text is split into tokens using Tiktoken (CL100K) and Gemini.
    """
    text = "Generative AI is amazing! 🚀"
    
    print("="*40)
    print(f"Original Text: {text}")
    print("="*40)

    # 1. Byte Pair Encoding (BPE) with Tiktoken (OpenAI standard)
    # Most modern models (GPT-4, Claude 3, etc.) use CL100K base
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        
        print(f"\n--- Tiktoken (CL100K Base) ---")
        print(f"Token IDs: {tokens}")
        print(f"Total Token Count: {len(tokens)}")
        
        # Decoding back to see what each token represents
        print("\nToken breakdown:")
        for token_id in tokens:
            # We convert each token back to its visual string representation
            # Note: Some tokens might be spaces or sub-words!
            decoded_token = encoding.decode([token_id])
            print(f"ID {token_id:6} -> '{decoded_token}'")
    except Exception as e:
        print(f"Tiktoken error (likely not installed): {e}")

    # 2. Gemini Token Counting (Requires API Key)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.count_tokens(text)
            print(f"\n--- Gemini 1.5 Flash Analysis ---")
            print(f"Gemini Total Tokens: {response.total_tokens}")
        except Exception as e:
            print(f"\nGemini counting failed (check API key): {e}")
    else:
        print("\n--- Gemini Analysis ---")
        print("Skipping Gemini token count (GEMINI_API_KEY not found in .env)")

    print("\n" + "="*40)
    print("PRACTICAL TAKEAWAY:")
    print("Notice how '🚀' might consume more than one token depending on the tokenizer.")
    print("Always calculate tokens before sending to an LLM to manage cost and limits.")
    print("="*40)

if __name__ == "__main__":
    explore_tokenization()
