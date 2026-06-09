---
name: ansi-art
description: "Use when creating, reviewing, converting, or embedding terminal text art: ASCII art, ANSI art, CP437/code page 437 glyph art, block ASCII, BBS-style logos, CLI banners, NFOs, fixed-width art, or SAUCE/XBIN/BIN/ANS output."
---

# ANSI Art

Goal: Create original CP437/ANSI/textmode art that renders cleanly in modern fixed-width terminals while carrying the visual richness of oldschool BBS art.

Success means:
- The target terminal, width, height, color policy, and output format are explicit.
- Every row has a fixed cell width and preserves intentional leading/trailing spaces.
- The glyph vocabulary comes from CP437-safe single-cell characters.
- The final output includes validation notes for width, colors, wrapping, and fallback behavior.

Stop when the art is display-ready for the requested environment or when the remaining uncertainty is a named terminal/font limitation.

## Workflow

1. Frame the target.
   - Identify the surface: CLI banner, splash screen, NFO, `.ANS` file, README preview, game UI, or code-embedded asset.
   - Set hard dimensions in character cells. For CLI banners, prefer 40-64 columns and 6-14 rows unless the user asks for larger art.
   - Select color mode: monochrome, 8-color ANSI, 16-color ANSI/iCE-style, 256-color, truecolor, or no-color fallback.
   - Ask one blocking question only when width, subject, or output format is genuinely unknown.

2. Choose the representation.
   - Use a cell grid for app and CLI assets: each cell has a glyph, foreground, background, and optional attributes.
   - Use UTF-8 Unicode glyphs that correspond to CP437 for modern terminal output.
   - Use CP437 bytes plus ANSI SGR only when producing a real `.ANS` artifact.
   - Use BIN/XBIN only when the user needs authentic textmode files, custom fonts/palettes, or archival compatibility.
   - Read `references/formats-and-rendering.md` before designing storage or renderer code.

3. Compose like pixel art.
   - Block in the silhouette at thumbnail scale.
   - Pick a light source before adding texture.
   - Build large masses with `█`, `▀`, `▄`, `▌`, and `▐`.
   - Add shade transitions with `░`, `▒`, and `▓`.
   - Use line drawing for UI frames and architectural structure. For organic outlines, use line drawing only when the style calls for a hard-edged look.
   - Read `references/creation-playbook.md` when the task is artistic rather than mechanical.

4. Use a constrained glyph vocabulary.
   - Start with the core block set and box drawing set in `references/glyphs-and-palette.md`.
   - Treat letters, punctuation, bullets, and math symbols as texture accents after the big forms work.
   - Keep ambiguous-width Unicode outside the art unless the target renderer has explicit width tests.

5. Render for terminals.
   - Emit explicit line breaks at the chosen width.
   - Preserve leading and trailing spaces in source storage and output tests.
   - Batch adjacent cells with the same style into one ANSI SGR span.
   - Reset SGR before each newline and after the last row.
   - Provide a no-color version when the art is used in a CLI that honors `NO_COLOR`, `TERM=dumb`, or `--color never`.

6. Validate.
   - Count cell width for every row.
   - Check that each non-ASCII glyph is in the allowed CP437 map.
   - Preview in at least one monospaced terminal font with box/block glyph support.
   - Test narrow-terminal behavior: center, skip, or use a smaller mark instead of letting the terminal wrap.
   - For code assets, add a focused test that rejects tabs, wide glyphs, inconsistent row widths, and unterminated ANSI styling.

## Output Patterns

For design work, return:

```text
Target:
Dimensions:
Palette:
Glyph set:
Art:
Validation:
Implementation notes:
```

For implementation work, include the renderer/storage choice and the tests that guard spacing.

## Research References

- Read `references/research-notes.md` for the source-backed synthesis behind this skill.
- Read `references/glyphs-and-palette.md` for CP437 glyph families, color ramps, and style vocabulary.
- Read `references/formats-and-rendering.md` for `.ANS`, SAUCE, BIN/XBIN, UTF-8 terminal rendering, and code storage choices.
- Read `references/creation-playbook.md` for composition, shading, lettering, and polish steps.
