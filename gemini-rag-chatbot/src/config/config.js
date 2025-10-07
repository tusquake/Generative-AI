import dotenv from 'dotenv';

dotenv.config();

export const config = {
    gemini: {
        apiKey: process.env.GEMINI_API_KEY,
        // Using the faster, more cost-effective Gemini Flash for RAG generation
        model: 'gemini-2.5-flash',
        // Using the high-quality, recommended model for embeddings
        embeddingModel: 'text-embedding-004',
    },
    pinecone: {
        apiKey: process.env.PINECONE_API_KEY,
        environment: process.env.PINECONE_ENVIRONMENT,
        indexName: process.env.PINECONE_INDEX_NAME,
        // NOTE: text-embedding-004 uses a 768-dimensional vector, 
        // but we keep the environment variable check as a fallback
        dimension: parseInt(process.env.EMBEDDING_DIMENSION) || 768,
    },
    document: {
        chunkSize: parseInt(process.env.CHUNK_SIZE) || 1000,
        chunkOverlap: parseInt(process.env.CHUNK_OVERLAP) || 200,
    },
};

// Validate configuration
export function validateConfig() {
    const required = [
        'GEMINI_API_KEY',
        'PINECONE_API_KEY',
        'PINECONE_ENVIRONMENT',
        'PINECONE_INDEX_NAME',
    ];

    const missing = required.filter(key => !process.env[key]);

    if (missing.length > 0) {
        throw new Error(
            `Missing required environment variables: ${missing.join(', ')}`
        );
    }

    console.log('✓ Configuration validated successfully');
}
