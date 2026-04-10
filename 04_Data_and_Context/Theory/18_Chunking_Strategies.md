# Topic 18: Chunking Strategies - Preparing Data for RAG

## 1. Scenario: The "Chopped-Up Mystery"
Imagine you are reading a mystery novel. Someone tears out pages 15-25 and gives them to you.
- **Problem:** Page 15 starts in the middle of a sentence: *"...murderer was actually the butler's..."*
- **Missing Context:** Who was the butler's what? Son? Wife? Dog? 
- **The Solution:** Better **Chunking**. If we include the last paragraph of the previous page, we get: *"It was revealed that the murderer was actually the butler's son."*

## 2. The Concept: Breaking Knowledge into Bite-Sized Pieces
LLMs have a limited "Context Window." We can't feed them a 500-page PDF at once. We must break it into "Chunks."

### Common Chunking Strategies:

1.  **Fixed-Size Chunking (The Basic):**
    *   **Method:** Every chunk is exactly 500 characters.
    *   **Pros:** Very fast, easy to implement.
    *   **Cons:** Breaks sentences in half; loses context.

2.  **Recursive Character Chunking (The Standard):**
    *   **Method:** Tries to split by double-newlines (paragraphs), then single-newlines, then spaces, then characters.
    *   **Pros:** Keeps most paragraphs and sentences intact.

3.  **Sliding Window / Overlap:**
    *   **Method:** Chunk 1: Lines 1-10. Chunk 2: Lines 5-15.
    *   **Why?** The "Overlap" ensures that if a concept spans two chunks, it's not lost.

4.  **Semantic Chunking (The Advanced):**
    *   **Method:** Uses embeddings to detect when a *topic* changes and splits there.
    *   **Pros:** Highest accuracy; chunks only contain one cohesive idea.

## 3. Workflow Diagram (Text)
[Large Document] -> [Splitter] -> [Chunk 1 + Overlap] -> [Chunk 2 + Overlap] -> Vector Embeddings

## 4. Key Metrics
- **Chunk Size:** How many tokens/characters per piece. (Usually 512 - 1024 tokens).
- **Chunk Overlap:** How much text to repeat from the previous chunk. (Usually 10-20%).

## 5. Interview Corner

1. **"What happens if my chunk size is too small?"**
   * Answer: The LLM won't have enough context to answer complex questions (the "Missing Context" problem).

2. **"What happens if my chunk size is too large?"**
   * Answer: You waste tokens, and the "Signal-to-Noise" ratio decreases. The LLM might find the relevant info but get distracted by the surrounding 2,000 words.

3. **"How do I choose the 'right' chunk size?"**
   * Answer: It depends on your data. Technical documentation (dense) might need smaller chunks. Narrative novels (spread out) might need larger ones. Use "A/B Testing" on your RAG pipeline to decide.

4. **"What is 'Metadata Filtering' in chunking?"**
   * Answer: When you chunk, you save metadata like `{"page": 12, "section": "Introduction"}`. This allows the search system to say: "Search for info ONLY in the 'Introduction' section."
