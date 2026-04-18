from typing import List

def recursive_chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Implements a recursive character splitter logic.
    It attempts to split the text into chunks of roughly 'chunk_size' 
    while preserving 'overlap' characters between adjacent chunks to 
    maintain context.
    
    It prioritizes splitting at clean boundaries like newlines or spaces.
    """
    chunks = []
    start = 0
    
    # Clean up whitespace but keep structure
    text = text.strip()
    
    while start < len(text):
        # Initial end point based on chunk size
        end = start + chunk_size
        
        # If we aren't at the end of the document, find a clean break point
        if end < len(text):
            # Prioritize breaking at a newline to keep paragraphs/sentences intact
            break_point = text.rfind('\n', start, end)
            
            # If no newline, break at a space to keep words intact
            if break_point == -1 or break_point <= start:
                break_point = text.rfind(' ', start, end)
            
            # If a clean break point was found, update the 'end'
            if break_point != -1 and break_point > start:
                end = break_point
        
        # Extract the chunk and add to list
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # The 'Sliding Window' logic: 
        # Move the start pointer to (end - overlap)
        start = end - overlap
        
        # Safety checks to prevent infinite loops or negative indexes
        if start < 0:
            start = 0
        
        # If the start pointer hasn't moved forward, force it forward to prevent loop
        if start <= (end - chunk_size) and end < len(text):
            start = end
            
        # Stop if we've reached or passed the end of the text
        if end >= len(text):
            break

    return chunks

def run_chunking_demo():
    """
    Demonstrates recursive chunking on a sample text.
    Observe how the 'overlap' preserves context between chunks.
    """
    sample_text = """
    Phase 1: Retrieval. This involves searching a database for context.
    Phase 2: Augmentation. This involves adding the context to the prompt.
    Phase 3: Generation. This involves the model writing the final answer.
    
    Without chunking, long documents would exceed the context window.
    Without overlap, a sentence might be cut in half, losing its meaning.
    """

    # Using a small chunk size to force multiple splits for the demo
    CHUNK_SIZE = 80
    OVERLAP = 20

    print("-" * 50)
    print(f"RUNNING RECURSIVE CHUNKER (Size: {CHUNK_SIZE}, Overlap: {OVERLAP})")
    print("-" * 50)

    chunks = recursive_chunk_text(sample_text, chunk_size=CHUNK_SIZE, overlap=OVERLAP)

    for i, chunk in enumerate(chunks):
        print(f"CHUNK {i+1}:")
        print(f"'{chunk}'")
        print("-" * 25)

    print("\nINSIGHT:")
    print("Notice how the end of CHUNK 1 and the start of CHUNK 2")
    print("share some text. This 'Overlap' ensures that the embedding")
    print("model has enough surrounding context to understand the chunk.")
    print("-" * 50)

if __name__ == "__main__":
    run_chunking_demo()
