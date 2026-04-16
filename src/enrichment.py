def enrich_chunk(chunk: dict, manifest: dict) -> dict:
    return {
        **chunk,
        "metadata": {
            # Project-level
            "project_id":        manifest["project_id"],
            "date":              manifest["date"],
            "roof_type":         manifest["roof_type"],    # flat, pitched, mansard
            "system":            manifest["system"],        # Proteus TF, Bauder, IKO
            "region":            manifest["region"],        # North West, London, etc.
            "contract_value":    manifest["contract_value_gbp"],

            # Document-level
            "doc_type":          chunk["doc_type"],
            # condition_report | tender | pricing_sheet |
            # labour_rates | scope_of_works | photograph |
            # product_spec | self_gen_prices

            # Content-level (populated by LLM extraction)
            "materials":         extract_materials(chunk["text"]),
            "products":          extract_product_codes(chunk["text"]),
            "has_quantities":    has_numeric_quantities(chunk["text"]),
            "has_pricing":       has_gbp_values(chunk["text"])
        }
    }

EXTRACT_PROMPT = """
Extract from the following roofing document text. Return JSON only.
{
  "materials": [],        // e.g. ["torch-on felt", "lead flashing"]
  "product_codes": [],    // e.g. ["PRO-TF-180", "PRO-ANC-FL"]
  "quantities": [],       // e.g. ["142.5m2", "8 rolls"]
  "prices_gbp": []        // e.g. [42.00, 336.00]
}
Text: {text}
"""