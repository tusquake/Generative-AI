import os
import uuid
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = FastAPI(
    title="SentryNode RAG Engine",
    description="Vector search microservice for retrieving incident resolution runbooks."
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secretpassword@localhost:5432/sentrynode")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class RunbookDoc(BaseModel):
    title: str
    content: str

class QueryPayload(BaseModel):
    query: str
    top_k: int = 3

def get_embedding(text: str) -> list[float]:
    """
    Generates a 768-dimensional vector embedding.
    Uses Google GenAI API if GOOGLE_API_KEY is present; otherwise falls back to a deterministic local mock.
    """
    if GOOGLE_API_KEY:
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding API error: {e}. Falling back to mock embeddings.")
            
    # Deterministic mock embedding: 768 float values derived from the text hash
    rng = np.random.default_rng(hash(text) & 0xffffffff)
    vector = rng.random(768).tolist()
    return vector

def rerank_results(query: str, results: list[dict]) -> list[dict]:
    """
    Simulates a Cross-Encoder Reranking pass.
    Adjusts the vector similarity score based on term coverage (keyword intersections).
    """
    query_words = set(query.lower().split())
    for item in results:
        chunk_text = item["chunk_text"].lower()
        # Find intersection
        matched_words = len(query_words.intersection(chunk_text.split()))
        # Boost score proportionally
        item["rerank_score"] = item["similarity"] + (matched_words * 0.05)
        
    # Re-sort based on the updated rerank score
    results.sort(key=lambda x: x["rerank_score"], reverse=True)
    return results

@app.post("/index")
def index_runbook(doc: RunbookDoc):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        runbook_id = str(uuid.uuid4())
        
        # 1. Store the raw runbook
        cur.execute(
            "INSERT INTO runbooks (runbook_id, title, markdown_content) VALUES (%s, %s, %s)",
            (runbook_id, doc.title, doc.content)
        )
        
        # 2. Chunking strategy: split by paragraphs
        paragraphs = [p.strip() for p in doc.content.split("\n\n") if p.strip()]
        for i, chunk in enumerate(paragraphs):
            embedding = get_embedding(chunk)
            embedding_id = str(uuid.uuid4())
            cur.execute(
                """
                INSERT INTO runbook_embeddings (embedding_id, runbook_id, chunk_index, chunk_text, embedding_vector)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (embedding_id, runbook_id, i, chunk, embedding)
            )
            
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "runbook_id": runbook_id, "chunks_indexed": len(paragraphs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@app.post("/search")
def search_runbooks(payload: QueryPayload):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        query_vector = get_embedding(payload.query)
        
        # SQL execution using Cosine distance operator '<=>'
        cur.execute(
            """
            SELECT runbook_id, chunk_index, chunk_text, 1 - (embedding_vector <=> %s::vector) AS similarity
            FROM runbook_embeddings
            ORDER BY embedding_vector <=> %s::vector
            LIMIT %s
            """,
            (query_vector, query_vector, payload.top_k * 2) # Get double to allow reranking pool
        )
        
        raw_results = cur.fetchall()
        cur.close()
        conn.close()
        
        results = []
        for r in raw_results:
            results.append({
                "runbook_id": r[0],
                "chunk_index": r[1],
                "chunk_text": r[2],
                "similarity": float(r[3])
            })
            
        # Apply Reranker pass
        reranked = rerank_results(payload.query, results)
        
        # Slice to requested top_k
        return {"results": reranked[:payload.top_k]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
