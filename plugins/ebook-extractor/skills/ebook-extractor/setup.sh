#!/bin/bash
# Setup script for ebook-extractor skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Ebook Extractor Setup ==="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3 first."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Install Python packages
echo
echo "Installing Python packages..."
pip3 install -q -r "$SCRIPT_DIR/requirements.txt"
echo "✓ Python packages installed"

# Check for Calibre (optional, for MOBI support)
echo
if command -v ebook-convert &> /dev/null; then
    echo "✓ Calibre found (MOBI support enabled)"
else
    echo "⚠ Calibre not found (MOBI support disabled)"
    echo "  To enable MOBI support, install Calibre:"
    echo "    macOS:  brew install calibre"
    echo "    Linux:  sudo apt install calibre"
fi

echo
echo "=== Setup complete ==="
echo
echo "Usage:"
echo "  python3 $SCRIPT_DIR/scripts/extract.py <ebook_file>"
