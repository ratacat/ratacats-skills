#!/usr/bin/env python3
"""
Unified ebook text extractor.
Auto-detects format and extracts text from EPUB, MOBI, and PDF files.
"""

import sys
from pathlib import Path

# Add script directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def detect_format(file_path: str) -> str:
    """Detect ebook format from file extension."""
    ext = Path(file_path).suffix.lower()

    format_map = {
        '.epub': 'epub',
        '.mobi': 'mobi',
        '.azw': 'mobi',
        '.azw3': 'mobi',
        '.pdf': 'pdf',
    }

    return format_map.get(ext, 'unknown')


def extract_text(file_path: str) -> str:
    """Extract text from any supported ebook format."""
    fmt = detect_format(file_path)

    if fmt == 'epub':
        from extract_epub import extract_text_from_epub
        return extract_text_from_epub(file_path)

    elif fmt == 'mobi':
        from extract_mobi import extract_text_from_mobi
        return extract_text_from_mobi(file_path)

    elif fmt == 'pdf':
        from extract_pdf import extract_text_from_pdf
        return extract_text_from_pdf(file_path)

    else:
        print(f"Unsupported format: {Path(file_path).suffix}", file=sys.stderr)
        print("Supported formats: .epub, .mobi, .azw, .azw3, .pdf", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract.py <ebook_file> [-o output_file]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Supported formats: EPUB, MOBI, AZW, AZW3, PDF", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    output_path = None

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    if not Path(file_path).exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    fmt = detect_format(file_path)
    print(f"Detected format: {fmt.upper()}", file=sys.stderr)

    text = extract_text(file_path)

    if output_path:
        Path(output_path).write_text(text, encoding='utf-8')
        print(f"Extracted to: {output_path}", file=sys.stderr)
    else:
        print(text)


if __name__ == '__main__':
    main()
