import { Pinecone } from '@pinecone-database/pinecone';
import { config } from '../config/config.js';

class PineconeService {
  constructor() {
    this.client = null;
    this.index = null;
  }

  /**
   * Initialize Pinecone client and index
   */
  async initialize() {
    try {
      console.log('Initializing Pinecone...');

      this.client = new Pinecone({
        apiKey: config.pinecone.apiKey,
      });

      // Check if index exists
      const indexes = await this.client.listIndexes();
      const indexExists = indexes.indexes?.some(
        idx => idx.name === config.pinecone.indexName
      );

      if (!indexExists) {
        console.log(`Creating index: ${config.pinecone.indexName}`);
        await this.client.createIndex({
          name: config.pinecone.indexName,
          dimension: config.pinecone.dimension,
          metric: 'cosine',
          spec: {
            serverless: {
              cloud: 'aws',
              region: 'us-east-1'
            }
          }
        });

        // Wait for index to be ready
        console.log('Waiting for index to be ready...');
        await new Promise(resolve => setTimeout(resolve, 60000));
      }

      this.index = this.client.index(config.pinecone.indexName);
      console.log('✓ Pinecone initialized successfully');
    } catch (error) {
      console.error('Error initializing Pinecone:', error);
      throw error;
    }
  }

  /**
   * Upsert vectors to Pinecone
   */
  async upsertVectors(chunks, embeddings) {
    if (chunks.length !== embeddings.length) {
      throw new Error('Chunks and embeddings length mismatch');
    }

    console.log(`Upserting ${chunks.length} vectors to Pinecone...`);

    const vectors = chunks.map((chunk, idx) => ({
      id: chunk.id,
      values: embeddings[idx],
      metadata: {
        content: chunk.content,
        source: chunk.metadata.source,
        chunkIndex: chunk.metadata.chunkIndex,
        totalChunks: chunk.metadata.totalChunks,
      },
    }));

    // Upsert in batches
    const batchSize = 100;
    for (let i = 0; i < vectors.length; i += batchSize) {
      const batch = vectors.slice(i, i + batchSize);
      await this.index.upsert(batch);
      console.log(`  Upserted: ${Math.min(i + batchSize, vectors.length)}/${vectors.length}`);
    }

    console.log('✓ Vectors upserted successfully');
  }

  /**
   * Query similar vectors
   */
  async query(queryEmbedding, topK = 5) {
    try {
      const queryResponse = await this.index.query({
        vector: queryEmbedding,
        topK: topK,
        includeMetadata: true,
      });

      return queryResponse.matches.map(match => ({
        id: match.id,
        score: match.score,
        content: match.metadata.content,
        source: match.metadata.source,
        chunkIndex: match.metadata.chunkIndex,
      }));
    } catch (error) {
      console.error('Error querying Pinecone:', error);
      throw error;
    }
  }

  /**
   * Delete all vectors from index
   */
  async deleteAll() {
    try {
      console.log('Deleting all vectors from index...');
      await this.index.deleteAll();
      console.log('✓ All vectors deleted');
    } catch (error) {
      console.error('Error deleting vectors:', error);
      throw error;
    }
  }

  /**
   * Get index statistics
   */
  async getStats() {
    try {
      const stats = await this.index.describeIndexStats();
      return stats;
    } catch (error) {
      console.error('Error getting stats:', error);
      throw error;
    }
  }
}

export default PineconeService;