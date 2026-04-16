def retrieve_for_estimation(query: str, filters: dict, top_k: int = 12) -> list[dict]:
    query_embedding = embed_text(query)

    # Build metadata filter from job context
    # e.g. filters = {"roof_type": "flat", "region": "North West"}
    metadata_filter = " AND ".join([
        f"metadata->>{k!r} = {v!r}" for k, v in filters.items()
    ])

    sql = f"""
        SELECT text, image_path, metadata, doc_type,
               1 - (embedding <=> %s::vector) AS similarity
        FROM roofing_chunks
        WHERE {metadata_filter}
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """
    results = db.execute(sql, [query_embedding, query_embedding, top_k])
    return results