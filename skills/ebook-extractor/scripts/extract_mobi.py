#!/usr/bin/env python3
"""Extract text from MOBI files using Calibre conversion."""

import subprocess
import sys
import tempfile
from pathlib import Path

# Import the EPUB extractor
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from extract_epub import extract_text_from_epub


def check_calibre():
    """Check if Calibre's ebook-convert is available."""
    try:
        subprocess.run(
            ['ebook-convert', '--version'],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def extract_text_from_mobi(mobi_path: str) -> str:
    """Extract text from MOBI by converting to EPUB first."""
    if not check_calibre():
        print("Error: Calibre not found. Install with: brew install calibre", file=sys.stderr)
        sys.exit(1)

    # Convert MOBI to temporary EPUB
    with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as tmp:
        tmp_epub = tmp.name

    try:
        result = subprocess.run(
            ['ebook-convert', mobi_path, tmp_epub],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Conversion failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        # Extract text from the converted EPUB
        return extract_text_from_epub(tmp_epub)

    finally:
        # Clean up temp file
        Path(tmp_epub).unlink(missing_ok=True)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_mobi.py <mobi_file> [-o output_file]", file=sys.stderr)
        sys.exit(1)

    mobi_path = sys.argv[1]
    output_path = None

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    if not Path(mobi_path).exists():
        print(f"File not found: {mobi_path}", file=sys.stderr)
        sys.exit(1)

    text = extract_text_from_mobi(mobi_path)

    if output_path:
        Path(output_path).write_text(text, encoding='utf-8')
        print(f"Extracted to: {output_path}", file=sys.stderr)
    else:
        print(text)


if __name__ == '__main__':
    main()
