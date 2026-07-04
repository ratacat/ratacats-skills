# ANSI Art

This skill helps an agent create original terminal text art with the oldschool CP437/ANSI vocabulary: block glyphs, shade ramps, fixed cell grids, and BBS-style color discipline.

Use it when the output needs to live in a terminal, CLI banner, NFO, `.ANS` file, TUI, README preview, or code-embedded art asset. It focuses on beauty and display reliability together: silhouette first, controlled glyphs, explicit dimensions, terminal-safe rendering, and validation for wrapping and color fallback.

Good fits:

- Designing CP437-style CLI banners
- Creating ANSI or block ASCII logos
- Choosing `.ANS`, BIN/XBIN, or app-native storage
- Converting art for UTF-8 terminal output
- Reviewing fixed-width art for spacing and glyph issues

For deeper work, use the bundled references: [research notes](references/research-notes.md), [glyphs and palette](references/glyphs-and-palette.md), [formats and rendering](references/formats-and-rendering.md), and the [creation playbook](references/creation-playbook.md).

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill ansi-art

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install ansi-art@ratacats-skills
```
