import fitz          # PyMuPDF — PDF to images
import pytesseract   # OCR for typed text
import pandas as pd  # Excel/CSV parsing
from pathlib import Path
from PIL import Image

class DocumentIngester:

    def ingest(self, file_path: str, doc_type: str) -> list[dict]:
        path = Path(file_path)
        ext  = path.suffix.lower()

        if ext == ".pdf":
            return self._ingest_pdf(path, doc_type)
        elif ext in [".jpg", ".jpeg", ".png"]:
            return self._ingest_image(path, doc_type)
        elif ext in [".xlsx", ".csv"]:
            return self._ingest_structured(path, doc_type)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _ingest_pdf(self, path, doc_type):
        doc = fitz.open(path)
        pages = []
        for i, page in enumerate(doc):
            # Render page at 200 DPI for handwriting legibility
            mat = fitz.Matrix(200/72, 200/72)
            pix = page.get_pixmap(matrix=mat)
            img_path = f"/tmp/{path.stem}_p{i+1}.jpg"
            pix.save(img_path)

            # OCR the rendered image
            text = pytesseract.image_to_string(Image.open(img_path))

            pages.append({
                "image_path": img_path,
                "text":       text,
                "page":       i + 1,
                "doc_type":   doc_type,
                "source":     str(path)
            })
        return pages

    def _ingest_image(self, path, doc_type):
        # For photographs: generate a caption using a multimodal LLM
        caption = self._generate_image_caption(path)
        return [{
            "image_path": str(path),
            "text":       caption,
            "doc_type":   doc_type,
            "source":     str(path)
        }]

    def _ingest_structured(self, path, doc_type):
        # Parse Excel/CSV rate cards into JSON rows
        df = pd.read_excel(path) if path.suffix == ".xlsx" else pd.read_csv(path)
        rows = []
        for _, row in df.iterrows():
            rows.append({
                "text":     row.to_json(),
                "doc_type": doc_type,
                "source":   str(path)
            })
        return rows

    def _generate_image_caption(self, path):
        # Call your multimodal LLM (GPT-4o, Claude, etc.)
        # to produce a roofing-aware caption from the photograph
        # e.g. "Flat roof section showing delamination of felt
        #        along north parapet, approx 3m run affected"
        pass