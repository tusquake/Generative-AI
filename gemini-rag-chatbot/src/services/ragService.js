import GeminiService from './geminiService.js';
import PineconeService from './pineconeService.js';
import { loadDocuments, processDocuments } from '../utils/documentLoader.js';

class RAGService {
  constructor() {
    this.geminiService = new GeminiService();
    this.pineconeService = new PineconeService();
    this.chatHistory = [];
  }

  /**
   * Initialize the RAG system
   */
  async initialize() {
    console.log('\n=== Initializing RAG System ===\n');
    await this.pineconeService.initialize();
    console.log('✓ RAG System initialized\n');
  }

  /**
   * Index documents into the system
   */
  async indexDocuments(documentsPath) {
    console.log('\n=== Indexing Documents ===\n');

    try {
      // Step 1: Load documents
      console.log('Step 1: Loading documents...');
      const documents = await loadDocuments(documentsPath);

      if (documents.length === 0) {
        throw new Error('No documents found to index');
      }

      // Step 2: Process into chunks
      console.log('\nStep 2: Processing documents into chunks...');
      const chunks = processDocuments(documents);

      // Step 3: Generate embeddings
      console.log('\nStep 3: Generating embeddings...');
      const embeddings = await this.geminiService.generateEmbeddings(
        chunks.map(chunk => chunk.content)
      );

      // Step 4: Store in Pinecone
      console.log('\nStep 4: Storing in Pinecone...');
      await this.pineconeService.upsertVectors(chunks, embeddings);

      console.log('\n✓ Documents indexed successfully!');

      // Show stats
      const stats = await this.pineconeService.getStats();
      console.log(`\nIndex Statistics:
  - Total vectors: ${stats.totalRecordCount || 0}
  - Dimension: ${stats.dimension || 0}`);

    } catch (error) {
      console.error('\n✗ Error indexing documents:', error);
      throw error;
    }
  }

  /**
   * Query the RAG system
   */
  async query(question, topK = 4) {
    try {
      // Step 1: Generate query embedding
      const queryEmbedding = await this.geminiService.generateEmbedding(question);

      // Step 2: Retrieve relevant documents
      const results = await this.pineconeService.query(queryEmbedding, topK);

      if (results.length === 0) {
        return {
          answer: "I couldn't find any relevant information to answer your question.",
          sources: [],
        };
      }

      // Step 3: Build context from retrieved documents
      const context = results
        .map((result, idx) => `[Document ${idx + 1}] (Source: ${result.source}, Score: ${result.score.toFixed(3)})
${result.content}`)
        .join('\n\n');

      // Step 4: Generate answer
      const answer = await this.geminiService.generateAnswer(question, context);

      return {
        answer,
        sources: results,
      };
    } catch (error) {
      console.error('Error querying RAG system:', error);
      throw error;
    }
  }

  /**
   * Query with conversation history
   */
  async queryWithHistory(question, topK = 4) {
    try {
      // Generate embedding and retrieve documents
      const queryEmbedding = await this.geminiService.generateEmbedding(question);
      const results = await this.pineconeService.query(queryEmbedding, topK);

      if (results.length === 0) {
        return {
          answer: "I couldn't find any relevant information to answer your question.",
          sources: [],
        };
      }

      // Build context
      const context = results
        .map((result, idx) => `[${idx + 1}] ${result.content}`)
        .join('\n\n');

      // Generate answer with chat history
      const answer = await this.geminiService.generateConversationalAnswer(
        question,
        context,
        this.chatHistory
      );

      // Update chat history
      this.chatHistory.push(
        { role: 'user', content: question },
        { role: 'assistant', content: answer }
      );

      // Keep only last 10 messages
      if (this.chatHistory.length > 10) {
        this.chatHistory = this.chatHistory.slice(-10);
      }

      return {
        answer,
        sources: results,
      };
    } catch (error) {
      console.error('Error in conversational query:', error);
      throw error;
    }
  }

  /**
   * Clear chat history
   */
  clearHistory() {
    this.chatHistory = [];
    console.log('Chat history cleared');
  }

  /**
   * Get index statistics
   */
  async getStats() {
    return await this.pineconeService.getStats();
  }
}

export default RAGService;