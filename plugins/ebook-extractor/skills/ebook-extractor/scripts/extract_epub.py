#!/usr/bin/env python3
"""Extract text from EPUB files."""

import sys
from pathlib import Path

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing dependency: {e}", file=sys.stderr)
    print("Install with: pip install ebooklib beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def extract_text_from_epub(epub_path: str) -> str:
    """Extract all text content from an EPUB file."""
    book = epub.read_epub(epub_path)

    text_parts = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')

            # Remove script and style elements
            for element in soup(['script', 'style', 'nav']):
                element.decompose()

            # Get text with reasonable whitespace handling
            text = soup.get_text(separator='\n', strip=True)

            if text.strip():
                text_parts.append(text)

    return '\n\n'.join(text_parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_epub.py <epub_file> [-o output_file]", file=sys.stderr)
        sys.exit(1)

    epub_path = sys.argv[1]
    output_path = None

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    if not Path(epub_path).exists():
        print(f"File not found: {epub_path}", file=sys.stderr)
        sys.exit(1)

    text = extract_text_from_epub(epub_path)

    if output_path:
        Path(output_path).write_text(text, encoding='utf-8')
        print(f"Extracted to: {output_path}", file=sys.stderr)
    else:
        print(text)


if __name__ == '__main__':
    main()
