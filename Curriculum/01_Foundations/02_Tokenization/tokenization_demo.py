# tokenization_demo.py
# Topic 2: Tokens, Context Windows, and how LLMs "read"

import tiktoken

def explore_tokenization_mechanics():
    """
    Shows how different types of text are converted into tokens.
    Notice how emojis and complex words are handled differently.
    """
    
    # 1. A mix of text types
    # - "Hello" (very common)
    # - "pomegranate" (less common)
    # - "🚀" (emoji)
    sample_text = "Hello! 🚀 The pomegranate was delicious."
    
    # 2. Setup the tokenizer (using the standard GPT-4/Claude encoding)
    # cl100k_base is the industry standard for modern LLMs
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # 3. Convert text into Token IDs
    token_ids = encoding.encode(sample_text)
    
    print("-" * 50)
    print(f"Original Text: {sample_text}")
    print(f"Word Count   : {len(sample_text.split())}")
    print(f"Token Count  : {len(token_ids)}")
    print("-" * 50)

    # 4. Break it down to see the 'Lego bricks'
    print(f"{'TEXT PIECE':<15} | {'TOKEN ID':<10}")
    print("-" * 30)
    
    for t_id in token_ids:
        # Decode one ID at a time back into visible text
        piece = encoding.decode([t_id])
        print(f"'{piece}':<15 | {t_id:<10}")

    print("-" * 50)
    print("PRACTICAL TIP:")
    print("Notice how 'pomegranate' or '🚀' might consume more than one token.")
    print("In production, budget for 1,000 tokens per 750 words.")
    print("-" * 50)

if __name__ == "__main__":
    explore_tokenization_mechanics()
