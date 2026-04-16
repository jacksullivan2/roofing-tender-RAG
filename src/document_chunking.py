from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(parsed_pages: list[dict], doc_type: str) -> list[dict]:
    chunks = []

    if doc_type in ["condition_report", "scope_of_works", "product_spec"]:
        # Narrative text: semantic chunks with overlap
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=40,
            separators=["\n\n", "\n", ". ", " "]
        )
        for page in parsed_pages:
            for chunk_text in splitter.split_text(page["text"]):
                chunks.append({**page, "text": chunk_text, "chunk_type": "narrative"})

    elif doc_type in ["pricing_sheet", "labour_rates", "self_gen_prices"]:
        # Structured rows: keep each row as its own chunk with the header repeated
        for page in parsed_pages:
            data = json.loads(page["text"])
            header = list(data.keys())
            chunks.append({
                **page,
                "text": f"Header: {header}\nRow: {json.dumps(data)}",
                "chunk_type": "structured_row"
            })

    elif doc_type == "photograph":
        # Image chunks: caption + image path as a pair
        for page in parsed_pages:
            chunks.append({
                **page,
                "text":       page["text"],       # LLM-generated caption
                "image_path": page["image_path"], # raw image retained
                "chunk_type": "image_caption"
            })

    elif doc_type == "tender":
        # Also generate a project-level summary chunk for broad recall
        full_text = " ".join([p["text"] for p in parsed_pages])
        chunks.append({
            "text":       summarise_project(full_text),
            "doc_type":   "tender",
            "chunk_type": "project_summary"
        })
        # Plus fine-grained narrative chunks
        chunks += chunk_document(parsed_pages, "condition_report")

    return chunks