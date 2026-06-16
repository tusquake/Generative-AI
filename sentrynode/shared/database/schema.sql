-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Sessions Table
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY,
    repo_url TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'initialized',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks Table (Sub-tasks created by the Architect planner)
CREATE TABLE IF NOT EXISTS tasks (
    task_id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Actions Table (Command/Tool execution history)
CREATE TABLE IF NOT EXISTS actions (
    action_id UUID PRIMARY KEY,
    task_id UUID REFERENCES tasks(task_id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    arguments JSONB,
    console_output TEXT,
    exit_code INTEGER,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Runbooks Reference Table
CREATE TABLE IF NOT EXISTS runbooks (
    runbook_id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    markdown_content TEXT NOT NULL
);

-- Runbook Embeddings Table (Vector matching)
CREATE TABLE IF NOT EXISTS runbook_embeddings (
    embedding_id UUID PRIMARY KEY,
    runbook_id UUID REFERENCES runbooks(runbook_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding_vector vector(768) NOT NULL -- Using 768 dimensions (typical for local/google models)
);

-- Apply HNSW Index for fast vector retrieval
CREATE INDEX IF NOT EXISTS runbook_hnsw_idx 
ON runbook_embeddings 
USING hnsw (embedding_vector vector_cosine_ops);
