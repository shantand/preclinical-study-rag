import json
from pathlib import Path

import fitz  # PyMuPDF

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

CHUNK_SIZE = 1000
OVERLAP = 200


def extract_text(pdf_path: Path) -> str:
    """Extract all text from a PDF."""

    document = fitz.open(pdf_path)

    pages = []

    for page in document:
        text = page.get_text("text")

        # Basic cleanup
        text = text.replace("\u00A0", " ")
        text = text.replace("\r", "")
        text = "\n".join(
            line.strip()
            for line in text.splitlines()
            if line.strip()
        )

        pages.append(text)

    document.close()

    return "\n".join(pages)


def chunk_text(text: str):
    """Split text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):

        end = min(start + CHUNK_SIZE, len(text))

        chunks.append({
            "char_start": start,
            "char_end": end,
            "text": text[start:end]
        })

        if end == len(text):
            break

        start = end - OVERLAP

    return chunks


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    pdfs = sorted(DATA_DIR.glob("*.pdf"))

    if not pdfs:
        print("No PDFs found inside data/")
        return

    all_chunks = []

    global_chunk_id = 1

    for pdf in pdfs:

        print(f"Processing {pdf.name}")

        text = extract_text(pdf)

        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):

            all_chunks.append({
                "id": global_chunk_id,
                "source": pdf.name,
                "chunk_index": idx,
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
                "text": chunk["text"]
            })

            global_chunk_id += 1

        print(f"  {len(chunks)} chunks created")

    output_file = OUTPUT_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 60)
    print(f"Processed {len(pdfs)} PDFs")
    print(f"Created {len(all_chunks)} chunks")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
