from openai import OpenAI
import psycopg2
import numpy as np

client = OpenAI()

def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding

def store_chunk(chunk: dict, embedding: list[float], conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO roofing_chunks (
                project_id, doc_type, chunk_type, text,
                image_path, metadata, embedding
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            chunk["metadata"]["project_id"],
            chunk["metadata"]["doc_type"],
            chunk.get("chunk_type"),
            chunk["text"],
            chunk.get("image_path"),
            json.dumps(chunk["metadata"]),
            np.array(embedding).tolist()
        ))
    conn.commit()