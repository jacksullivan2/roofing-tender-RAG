CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE roofing_chunks (
    id            SERIAL PRIMARY KEY,
    project_id    TEXT NOT NULL,
    doc_type      TEXT NOT NULL,
    chunk_type    TEXT,
    text          TEXT,
    image_path    TEXT,
    metadata      JSONB,
    embedding     vector(3072),  -- text-embedding-3-large dimension
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Fast similarity search index
CREATE INDEX ON roofing_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Fast metadata filtering
CREATE INDEX ON roofing_chunks USING GIN (metadata);
CREATE INDEX ON roofing_chunks (project_id);
CREATE INDEX ON roofing_chunks (doc_type);