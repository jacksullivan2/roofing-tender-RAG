# Azure AI Document Intelligence handles handwriting well
from azure.ai.formrecognizer import DocumentAnalysisClient

def ocr_handwritten(image_path: str) -> str:
    client = DocumentAnalysisClient(endpoint, credential)
    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-read", f)
    result = poller.result()
    return "\n".join([line.content for page in result.pages for line in page.lines])