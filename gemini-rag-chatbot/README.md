# RAG Chatbot with Gemini and Pinecone

A Retrieval-Augmented Generation (RAG) chatbot that uses Google's Gemini AI and Pinecone vector database to answer questions based on your documents. This project demonstrates how to build an intelligent chatbot that can understand and respond to questions about your specific content.

## What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that combines two powerful AI concepts:

1. **Retrieval**: Finding relevant information from a knowledge base (your documents)
2. **Augmented Generation**: Using that retrieved information to generate better, more accurate answers

Instead of relying solely on the AI's training data, RAG allows the AI to "look up" information from your specific documents before answering questions. This makes the chatbot more accurate and up-to-date for your particular use case.

## How This Project Works

### Step-by-Step Flow

1. **Document Processing**
   - Load PDF and text files from the `documents/` folder
   - Split documents into smaller chunks (default: 1000 characters with 200 character overlap)
   - Each chunk becomes a searchable piece of information

2. **Vector Embeddings**
   - Convert each text chunk into a numerical vector (embedding) using Gemini's embedding model
   - These vectors capture the semantic meaning of the text
   - Similar content will have similar vector representations

3. **Vector Storage**
   - Store all vectors in Pinecone, a specialized vector database
   - Each vector is associated with metadata (source file, chunk position, etc.)
   - Pinecone enables fast similarity search across all your documents

4. **Question Processing**
   - When you ask a question, convert it to a vector using the same embedding model
   - Search Pinecone for the most similar document chunks
   - Retrieve the top 4-5 most relevant chunks

5. **Answer Generation**
   - Send your question + retrieved context to Gemini's language model
   - Gemini generates an answer based on the specific information from your documents
   - The answer includes source citations for transparency

## Project Structure

```
gemini-rag-chatbot/
├── documents/                 # Place your PDF/text files here
│   └── 05-versions-space.pdf
├── src/
│   ├── config/
│   │   └── config.js         # Configuration and environment variables
│   ├── services/
│   │   ├── geminiService.js  # Handles Gemini AI interactions
│   │   ├── pineconeService.js # Manages vector database operations
│   │   └── ragService.js     # Main RAG orchestration logic
│   ├── utils/
│   │   └── documentLoader.js # Document processing and chunking
│   └── index.js              # Main application entry point
├── test/
│   └── data/                 # Test documents
├── index.html                # Web interface (optional)
├── package.json
└── README.md
```

## Prerequisites

Before you begin, you'll need:

1. **Node.js** (version 16 or higher)
2. **Google Gemini API Key** - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Pinecone API Key** - Sign up at [Pinecone](https://www.pinecone.io/)

## Installation

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd gemini-rag-chatbot
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment
   PINECONE_INDEX_NAME=your_index_name
   ```

4. **Add your documents**
   - Place PDF or text files in the `documents/` folder
   - The system will automatically process them when you run the indexing

## Usage

### Command Line Interface

1. **Start the application**
   ```bash
   npm start
   ```

2. **Follow the menu options**
   - **Option 1**: Index documents (required before first use)
   - **Option 2**: Start chatting
   - **Option 3**: View index statistics
   - **Option 4**: Exit

3. **First-time setup**
   - Choose option 1 to index your documents
   - Wait for the process to complete (this may take a few minutes)
   - Then choose option 2 to start asking questions

### Web Interface

1. **Open the web interface**
   - Open `index.html` in your web browser
   - This provides a more user-friendly interface

2. **Index documents**
   - Click "Index Documents" button
   - Wait for the indexing process to complete

3. **Start chatting**
   - Type your questions in the input field
   - View sources used for each answer

## Key Concepts Explained

### Vector Embeddings

Vector embeddings are numerical representations of text that capture semantic meaning. For example:
- "car" and "automobile" will have similar vectors
- "car" and "banana" will have very different vectors

This allows the system to find relevant information even if you use different words than the original document.

### Chunking Strategy

Documents are split into chunks because:
- Large documents don't fit in AI model context limits
- Smaller chunks allow more precise retrieval
- Overlap between chunks ensures no information is lost at boundaries

### Similarity Search

When you ask a question, the system:
1. Converts your question to a vector
2. Searches for the most similar document chunks
3. Uses cosine similarity to rank results
4. Returns the top matches with confidence scores

### Context Window Management

The system maintains conversation history but limits it to prevent:
- Exceeding AI model context limits
- Irrelevant old information affecting new answers
- Performance degradation

## Configuration Options

You can customize the system by modifying `src/config/config.js`:

```javascript
export const config = {
    gemini: {
        model: 'gemini-2.5-flash',        // AI model for generation
        embeddingModel: 'text-embedding-004', // Model for embeddings
    },
    pinecone: {
        dimension: 768,                    // Vector dimension
    },
    document: {
        chunkSize: 1000,                  // Characters per chunk
        chunkOverlap: 200,                // Overlap between chunks
    },
};
```

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Check your `.env` file exists and has all required keys
   - Ensure no extra spaces or quotes around the values

2. **"No documents found to index"**
   - Make sure you have files in the `documents/` folder
   - Supported formats: PDF and TXT files

3. **"Error generating embeddings"**
   - Check your Gemini API key is valid
   - Ensure you have sufficient API quota

4. **"Error initializing Pinecone"**
   - Verify your Pinecone API key and environment
   - Check if the index name exists in your Pinecone dashboard

### Performance Tips

1. **For large documents**: Increase chunk size to reduce total chunks
2. **For better accuracy**: Decrease chunk size for more precise retrieval
3. **For faster indexing**: Process documents in smaller batches
4. **For better answers**: Experiment with different topK values (number of chunks retrieved)

## API Reference

### RAGService Methods

- `initialize()`: Set up the RAG system
- `indexDocuments(path)`: Process and index documents from a folder
- `query(question, topK)`: Ask a question and get an answer
- `queryWithHistory(question, topK)`: Ask with conversation context
- `clearHistory()`: Reset conversation history
- `getStats()`: Get index statistics

### GeminiService Methods

- `generateEmbedding(text)`: Create vector for a single text
- `generateEmbeddings(texts)`: Create vectors for multiple texts
- `generateAnswer(question, context)`: Generate answer with context
- `generateConversationalAnswer(question, context, history)`: Generate with chat history

### PineconeService Methods

- `initialize()`: Set up Pinecone connection
- `upsertVectors(chunks, embeddings)`: Store vectors in database
- `query(embedding, topK)`: Search for similar vectors
- `getStats()`: Get database statistics

## Next Steps

Once you understand this basic RAG implementation, you can explore:
- More advanced retrieval strategies (hybrid search, reranking)
- Different embedding models and their trade-offs
- Fine-tuning language models for your specific domain
- Implementing conversation memory and context management
- Adding support for more document types and sources
