import fs from 'fs';
import path from 'path';
import pdfParse from 'pdf-parse';
import { config } from '../config/config.js';

/**
 * Load text file
 */
function loadTextFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    return {
        content,
        metadata: {
            source: path.basename(filePath),
            type: 'text',
        },
    };
}

/**
 * Load PDF file
 */
async function loadPDFFile(filePath) {
    const dataBuffer = fs.readFileSync(filePath);
    const data = await pdfParse(dataBuffer);

    return {
        content: data.text,
        metadata: {
            source: path.basename(filePath),
            type: 'pdf',
            pages: data.numpages,
        },
    };
}

/**
 * Load all documents from directory
 */
export async function loadDocuments(dirPath) {
    const documents = [];

    if (!fs.existsSync(dirPath)) {
        throw new Error(`Directory not found: ${dirPath}`);
    }

    const files = fs.readdirSync(dirPath);

    for (const file of files) {
        const filePath = path.join(dirPath, file);
        const ext = path.extname(file).toLowerCase();

        try {
            let doc;

            if (ext === '.txt') {
                doc = loadTextFile(filePath);
            } else if (ext === '.pdf') {
                doc = await loadPDFFile(filePath);
            } else {
                console.log(`Skipping unsupported file: ${file}`);
                continue;
            }

            documents.push(doc);
            console.log(`✓ Loaded: ${file}`);
        } catch (error) {
            console.error(`✗ Error loading ${file}:`, error.message);
        }
    }

    console.log(`\nTotal documents loaded: ${documents.length}`);
    return documents;
}

/**
 * Split text into chunks with overlap
 */
export function chunkText(text, chunkSize = config.document.chunkSize, overlap = config.document.chunkOverlap) {
    const chunks = [];
    let start = 0;

    while (start < text.length) {
        const end = start + chunkSize;
        const chunk = text.slice(start, end);
        chunks.push(chunk);
        start = end - overlap;
    }

    return chunks;
}

/**
 * Process documents into chunks
 */
export function processDocuments(documents) {
    const processedChunks = [];
    let chunkId = 0;

    for (const doc of documents) {
        const chunks = chunkText(doc.content);

        for (let i = 0; i < chunks.length; i++) {
            processedChunks.push({
                id: `chunk_${chunkId++}`,
                content: chunks[i].trim(),
                metadata: {
                    ...doc.metadata,
                    chunkIndex: i,
                    totalChunks: chunks.length,
                },
            });
        }
    }

    console.log(`\nTotal chunks created: ${processedChunks.length}`);
    return processedChunks;
}