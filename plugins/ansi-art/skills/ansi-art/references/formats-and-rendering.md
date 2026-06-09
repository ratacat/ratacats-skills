# Formats And Rendering

Use this reference when choosing storage, writing renderer code, converting art, or explaining terminal fidelity constraints.

## Choose The Format

### App-native cell grid

Best for CLI banners, TUIs, generated source assets, and tests.

Store:

```text
width
height
cells: glyph + foreground + background + attributes
metadata: title, target font, palette, fallback behavior
```

Render as UTF-8 plus ANSI SGR. This keeps the art deterministic and testable while preserving the CP437 visual vocabulary.

### Plain UTF-8 text

Best for monochrome README previews or no-color terminal fallback.

Store rows in a raw string or text file. Preserve trailing spaces by using a fenced code block, a raw string literal, or an escaped representation that keeps row length visible.

### `.ANS`

Best for authentic BBS/art-scene output.

Store CP437 bytes interspersed with ANSI escape sequences. Add SAUCE metadata when width, height, font, iCE colors, letter spacing, or aspect ratio matter to downstream viewers.

Use this format when the user asks for `.ans`, artpack compatibility, PabloDraw/ACiDDraw workflows, or historical viewers.

### BIN / BinaryText

Best for raw textmode screenshots.

Store character/attribute byte pairs in row-major order. Width usually comes from SAUCE metadata. Use when raw cell attributes are more important than text stream compatibility.

### XBIN

Best for explicit dimensions, custom palette/font, or compressed textmode images.

XBIN starts with `XBIN` plus EOF byte `0x1A`, stores width/height/font size/flags, and can include palette, font, and compressed image data. Use only when the user needs this specific compatibility surface.

## Renderer Rules

Count character cells, not bytes.

Treat these as one-cell glyphs in the intended terminal context:

```text
░ ▒ ▓ █ ▀ ▄ ▌ ▐ ■ ┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼ ╔ ╗ ╚ ╝ ═ ║
```

Use a Unicode width library when available. In Rust, prefer `unicode-width` if dependencies are acceptable. In dependency-light code, validate against an explicit whitelist and reject anything outside it.

Batch runs by style:

```text
set style -> write glyphs -> reset before newline
```

Reset before each newline and after the last row. This prevents color bleed into subsequent CLI output.

Preserve a no-color path. In color-disabled mode, render glyphs and spaces only.

## Terminal Failure Modes

Implicit wrapping breaks art. Render explicit line breaks and skip/scale/swap the banner when the terminal is narrower than the art.

Tabs break fixed art. Store spaces only.

Cursor movement makes output terminal-width dependent. For app-native art, expand cursor movement into spaces before storing. For `.ANS` conversion, parse cursor movement in a virtual grid, then render rows.

Raw CP437 bytes display incorrectly in UTF-8 terminals. Convert CP437 bytes to Unicode for modern terminal output.

SGR color codes consume zero cells. Row-width tests should strip ANSI escape sequences before counting glyph cells.

Ambiguous Unicode symbols may render as wide in some environments. Keep the glyph whitelist CP437-centered and test the target terminal.

Line drawing may show gaps in some fonts because original VGA hardware duplicated the eighth pixel column for selected CP437 glyphs. Prefer block art over intricate single-line boxes when pixel-perfect joins are critical.

## Storage Pattern For Source Code

For small CLI banners:

```text
const WIDTH: usize = 48;
const ROWS: &[&str] = &[
    "                                                ",
    " ... fixed width rows ...                       ",
];
```

Add tests:

```text
each row has WIDTH cells
no row contains tabs
every non-ASCII char is in the allowed CP437 glyph table
no rendered line exceeds terminal width in default mode
color output ends with reset
```

For colored art, store spans separately from glyph rows. This makes no-color rendering, width tests, and future palette changes straightforward.

## Conversion Pattern

When converting existing `.ANS` art for terminal display:

1. Read SAUCE metadata for width, font, aspect, and iCE hints.
2. Parse ANSI escape sequences into a virtual cell grid.
3. Decode CP437 bytes into Unicode glyphs.
4. Expand cursor movement and implicit wraps in the virtual grid.
5. Render explicit rows with modern SGR.
6. Validate the output width against the target terminal.

When creating new art for a CLI, skip `.ANS` stream parsing and build the grid directly.
