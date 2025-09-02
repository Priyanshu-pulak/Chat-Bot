from pathlib import Path 
from pdf2image import convert_from_path
import pdfplumber 
import pytesseract
from PIL import Image
import pandas as pd

PDF_DIR = Path("data")
OUTPUT_DIR = Path("extracted")
OUTPUT_FILE = OUTPUT_DIR / "extracted_info.txt"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE.write_text("", encoding="utf-8")

for pdf_path in PDF_DIR.glob("*.pdf"):
    print(f"Processing : {pdf_path.name}…")

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            tables = page.extract_tables()
            table_md_blocks = []
            for tbl in tables:
                df = pd.DataFrame(tbl).fillna("")
                table_md_blocks.append(df.to_markdown(index=False))

            if not text.strip():
                image = convert_from_path(pdf_path, dpi=300,
                                          first_page=i, last_page=i)[0]
                text = pytesseract.image_to_string(image, lang="eng")

            with OUTPUT_FILE.open("a", encoding="utf-8") as out:
                out.write(f"\n\n--- {pdf_path.name} ---\n")
                for block in table_md_blocks:
                    out.write(block + "\n\n")      # table(s), if any
                out.write(text)                     # regular text / OCR

print(f"\nAll extracted text saved to: {OUTPUT_FILE}")
