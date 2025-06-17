from pathlib import Path # Handling path like data, extracted
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import fitz  # PyMuPDF

PDF_DIR = Path("data")
OUTPUT_DIR = Path("extracted")
OUTPUT_FILE = OUTPUT_DIR / "pdf_text.txt"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE.write_text("", encoding="utf-8")

for pdf_path in PDF_DIR.glob("*.pdf"):
    print(f"Processing : {pdf_path.name}…")
    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()

        if not text:
            image = convert_from_path(pdf_path, dpi=300, first_page=i, last_page=i)[0]
            text = pytesseract.image_to_string(image, lang="eng")

        with OUTPUT_FILE.open("a", encoding="utf-8") as out:
            out.write(f"\n\n--- {pdf_path.name} | Page {i} ---\n{text}")

print(f"\nAll extracted text saved to: {OUTPUT_FILE}")
