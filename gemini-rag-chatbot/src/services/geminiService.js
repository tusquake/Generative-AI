import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from '../config/config.js';

class GeminiService {
    constructor() {
        this.genAI = new GoogleGenerativeAI(config.gemini.apiKey);
        this.model = this.genAI.getGenerativeModel({ model: config.gemini.model });
        this.embeddingModel = this.genAI.getGenerativeModel({
            model: config.gemini.embeddingModel
        });
    }

    /**
     * Generate embeddings for text using Gemini
     */
    async generateEmbedding(text) {
        try {
            const result = await this.embeddingModel.embedContent(text);
            return result.embedding.values;
        } catch (error) {
            console.error('Error generating embedding:', error);
            throw error;
        }
    }

    /**
     * Generate embeddings for multiple texts
     */
    async generateEmbeddings(texts) {
        console.log(`Generating embeddings for ${texts.length} chunks...`);
        const embeddings = [];

        // Process in batches to avoid rate limits
        const batchSize = 5;
        for (let i = 0; i < texts.length; i += batchSize) {
            const batch = texts.slice(i, i + batchSize);

            const batchEmbeddings = await Promise.all(
                batch.map(text => this.generateEmbedding(text))
            );

            embeddings.push(...batchEmbeddings);

            // Progress indicator
            if ((i + batchSize) % 20 === 0 || i + batchSize >= texts.length) {
                console.log(`  Progress: ${Math.min(i + batchSize, texts.length)}/${texts.length}`);
            }

            // Small delay to respect rate limits
            await new Promise(resolve => setTimeout(resolve, 200));
        }

        console.log('✓ Embeddings generated successfully');
        return embeddings;
    }

    /**
     * Generate answer using Gemini with context
     */
    async generateAnswer(query, context) {
        const prompt = `You are a helpful assistant that answers questions based on the provided context.
Use the following context to answer the question. If you cannot find the answer in the context, 
say so clearly. Always cite which part of the context you used.

Context:
${context}

Question: ${query}

Answer:`;

        try {
            const result = await this.model.generateContent(prompt);
            const response = await result.response;
            return response.text();
        } catch (error) {
            console.error('Error generating answer:', error);
            throw error;
        }
    }

    /**
     * Generate conversational response with chat history
     */
    async generateConversationalAnswer(query, context, chatHistory = []) {
        const historyText = chatHistory
            .map(msg => `${msg.role}: ${msg.content}`)
            .join('\n');

        const prompt = `You are a helpful assistant in a conversation. Use the context below to answer questions.

        Context:
        ${context}

        Chat History:
        ${historyText}

        Current Question: ${query}

        Answer:`;

        try {
            const result = await this.model.generateContent(prompt);
            const response = await result.response;
            return response.text();
        } catch (error) {
            console.error('Error generating conversational answer:', error);
            throw error;
        }
    }
}

export default GeminiService;