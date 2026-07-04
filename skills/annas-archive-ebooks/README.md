# Anna's Archive Ebooks

This skill helps an agent find a published book, compare editions and formats, and use the local `annas.py` script to search or download a file when the user has lawful access. Search works without an Anna's Archive key; automated fast downloads need a membership key, and free slow downloads still require the user to solve a captcha in a browser.

It is useful when a request starts as a vague title, author, or format preference and needs to become a concrete PDF, EPUB, MOBI, AZW3, or DJVU file. Downloads stay on your machine at the output path you choose; the skill does not publish files, and this skill directory has its own `.gitignore` for local `.env` and Python cache files.

Good fits:

- Finding the right edition of a technical or reference book
- Searching by title, author, expected title, or preferred format
- Downloading with a configured Anna's Archive membership key
- Renaming downloaded files into clean `title-author.ext` names
- Handing PDF, EPUB, or MOBI files to `ebook-extractor` for text conversion

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill annas-archive-ebooks

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install annas-archive-ebooks@ratacats-skills
```

## Setup / Requirements

The skill uses Python 3 and the bundled `annas.py` script:

```sh
python3 annas.py search "Clean Code Robert Martin" --format pdf --limit 5
python3 annas.py details <md5>
python3 annas.py download <md5> --output ./books/
```

Set `ANNAS_ARCHIVE_KEY` only if you have an Anna's Archive membership key and want automated fast downloads:

```sh
export ANNAS_ARCHIVE_KEY="your-membership-key"
```

Without a key, the skill shows the book page for manual download and explains that free slow downloads require a captcha. After every download, rename the file immediately with a clean lowercase `title-author.ext` filename; the original Anna's Archive filenames can contain Unicode punctuation that breaks shell commands.

On macOS, Python installs that cannot find system certificates may need `certifi` and `SSL_CERT_FILE` as described in the skill. Downloaded ebooks remain in their original format until another tool, such as `ebook-extractor`, converts them to text.
