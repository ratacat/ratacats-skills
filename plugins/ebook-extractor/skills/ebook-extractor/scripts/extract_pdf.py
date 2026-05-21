#!/usr/bin/env python3
"""Extract text from PDF files using PyMuPDF."""

import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Missing dependency: PyMuPDF", file=sys.stderr)
    print("Install with: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text content from a PDF file."""
    doc = fitz.open(pdf_path)

    text_parts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        if text.strip():
            text_parts.append(text)

    doc.close()

    return '\n\n'.join(text_parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_pdf.py <pdf_file> [-o output_file]", file=sys.stderr)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = None

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    if not Path(pdf_path).exists():
        print(f"File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    text = extract_text_from_pdf(pdf_path)

    if output_path:
        Path(output_path).write_text(text, encoding='utf-8')
        print(f"Extracted to: {output_path}", file=sys.stderr)
    else:
        print(text)


if __name__ == '__main__':
    main()
