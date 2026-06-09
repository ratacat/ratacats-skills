# ANSI Art Research Notes

Use this reference when the user asks for source-grounded decisions about CP437/ANSI art, storage formats, or terminal display fidelity.

## Core Findings

Classic ANSI art combines three things:

- A fixed character-cell grid.
- IBM PC code page 437 glyphs, especially block, shade, and box drawing characters.
- ANSI control sequences for color, cursor movement, and attributes.

Modern terminal output should usually keep the fixed grid and CP437 visual vocabulary, then render with Unicode code points plus ANSI SGR color. Literal CP437 bytes are best reserved for `.ANS` files and artpack-compatible artifacts.

## Source-Backed Constraints

SAUCE exists because viewers need metadata such as width, height, file type, font, letter spacing, aspect ratio, and iCE color hints. For agent-generated art, capture these fields in the design notes even when no SAUCE record is written. Source: https://www.acid.org/info/sauce/sauce.htm

16colo.rs documents why 8px/9px letter spacing and legacy aspect ratio matter. VGA line graphics duplicated the eighth pixel column for the C0-DFh range so lines and blocks joined cleanly. Modern terminals cannot guarantee that exact hardware behavior, so terminal art should be tested as character cells, not pixels. Source: https://16colo.rs/ansiflags.php

Roy/SAC's block ASCII tutorial frames "High ASCII" or "Block ASCII" as art built from DOS extended characters, with the block set `░ ▒ ▓ █ ▀ ▄ ▌ ▐ ■` as the primary visual material. Source: https://www.roysac.com/tutorial/roy-blockasciitutorial.html

Halaster and Zerovision tutorials emphasize artistic process: distort simple shapes, choose a light source, work at a scale large enough for transitions, add highlights and shadows, use grit sparingly, and blend by pushing colors and block densities together. Sources: http://www.roysac.com/tutorial/ansitut-hal-shade.html and https://www.roysac.com/tutorial/ansitut-zv.html

Lord Soth/iCE emphasizes proportion before polish: lay out the whole ANSI in block colors before shading, make the unshaded image read first, keep shading short and smooth as a transition between colors, continue half-blocks in the same light/dark trend, and omit details that distract from the focal point. Source: http://www.roysac.com/tutorial/LordSothAnsiTips.html

The Unicode CP437 mapping provides the practical bridge from DOS glyph bytes to modern text rendering. Use the mapping for glyph validation and for generating UTF-8 terminal output. Sources: http://unicode.org/Public/MAPPINGS/VENDORS/MICSFT/PC/CP437.TXT and https://susam.net/code/cp437/cp437.html

ANSI art converters show the common terminal failure modes: CP437 bytes need transcoding, cursor-forward sequences need expansion, line wrapping must be width-aware, and terminal fonts need CP437-compatible glyphs. Source: https://github.com/BourgeoisBear/ansiart2utf8

XBIN and BIN are cell-grid storage formats rather than stream text formats. BIN stores character/attribute pairs; XBIN adds explicit dimensions and optional palette/font/compression. Borrow the data model for app storage, and write these formats only when compatibility requires them. Sources: https://github.com/radman1/xbin/blob/master/XBIN.TXT and http://fileformats.archiveteam.org/wiki/BIN_(Binary_Text)

AnsiLove-style tooling supports `.ANS`, `.BIN`, `.XB`, iCE colors, SAUCE, IBM VGA fonts, and related art-scene formats. Use it as an ecosystem clue: high-fidelity display depends on both file bytes and render metadata. Source: https://github.com/ansilove/ansilove.js

16colo.rs examples show that high-quality art carries explicit metadata such as width, height, IBM VGA font, iCE colors, and letter spacing. Study metadata and technique; create original art. Example source: https://16colo.rs/pack/blocktronics_acid_trip/asx-ACiD.ANS

## Design Synthesis For Agents

Treat terminal art like constrained pixel art. The first pass should solve silhouette, scale, negative space, and light direction with a tiny glyph set. The second pass should add density ramps and color. The final pass should polish individual cells only after the whole form reads at normal terminal zoom.

Prefer original compositions. When a reference piece is supplied, extract the transferable mechanics: composition, density ramps, palette economy, lettering treatment, framing, and metadata. Produce new art that follows those mechanics without duplicating the source.

For CLI software, optimize for reliability over archival authenticity. A small UTF-8 CP437-compatible cell grid with style spans is easier to test, respects user color settings, and removes the implicit wrapping/cursor movement assumptions that make old `.ANS` files fragile in modern terminals.
