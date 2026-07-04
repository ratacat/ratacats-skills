# Ebook Extractor

This skill turns EPUB, MOBI, and PDF files into plain text an agent can search, quote, summarize, index, or analyze.

Different ebook formats hide text in different ways. Ebook Extractor gives the agent a local, repeatable path from "I have a book file" to "I can inspect the content" without using an LLM for the extraction pass.

Good fits:

- Extracting a chapter for study
- Preparing a book for search or indexing
- Pulling text into a research workflow
- Converting an ebook before asking questions about it

Extraction quality depends on the source file. EPUB and text PDFs work well; image-based PDFs need OCR, which this skill does not provide.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill ebook-extractor

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install ebook-extractor@ratacats-skills
```

## Requirements

Requires Python 3. From the skill directory, run:

```sh
bash setup.sh
```

`setup.sh` installs the Python packages from [requirements.txt](requirements.txt). It also checks for Calibre's `ebook-convert`; install Calibre separately if you need MOBI support.
