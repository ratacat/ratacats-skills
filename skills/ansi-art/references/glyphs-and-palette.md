# CP437 Glyphs And Palette

Use this reference while choosing glyphs, validating source art, or designing a shade ramp.

## Core Glyph Sets

Primary blocks:

```text
░  light shade        CP437 B0  U+2591
▒  medium shade       CP437 B1  U+2592
▓  dark shade         CP437 B2  U+2593
█  full block         CP437 DB  U+2588
▀  upper half block   CP437 DF  U+2580
▄  lower half block   CP437 DC  U+2584
▌  left half block    CP437 DD  U+258C
▐  right half block   CP437 DE  U+2590
■  black square       CP437 FE  U+25A0
∙  bullet operator    CP437 F9  U+2219
```

Single-line box drawing:

```text
┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼
```

Double-line box drawing:

```text
╔ ╗ ╚ ╝ ═ ║ ╠ ╣ ╦ ╩ ╬
```

Mixed-line box drawing:

```text
╓ ╖ ╙ ╜ ╒ ╕ ╘ ╛ ╞ ╡ ╟ ╢ ╤ ╧ ╥ ╨ ╪ ╫
```

Useful symbols and texture accents:

```text
• ° · ∙ √ ≈ ≡ ≤ ≥ ÷ ±
```

Validate these accents in the target font. Blocks and box drawing are more reliable than math symbols in many terminal stacks.

## Density Ramps

Monochrome block ramp:

```text
space -> ░ -> ▒ -> ▓ -> █
```

Half-block edge ramp:

```text
space -> ▄ or ▀ -> █
space -> ▌ or ▐ -> █
```

Combined ramp:

```text
space -> ░ -> ▄ -> ▒ -> ▓ -> █
```

Use ramps directionally. A row of random density characters looks noisy; a ramp that follows the surface, light source, or curvature reads as form.

## DOS Color Vocabulary

Base 8 foreground/background colors:

```text
0 black       30 / 40
1 red         31 / 41
2 green       32 / 42
3 brown       33 / 43
4 blue        34 / 44
5 magenta     35 / 45
6 cyan        36 / 46
7 light gray  37 / 47
```

Bright foreground colors are usually SGR bold or 90-97 in modern terminals:

```text
8 dark gray
9 bright red
10 bright green
11 yellow
12 bright blue
13 bright magenta
14 bright cyan
15 white
```

Classic ANSI backgrounds are 0-7. iCE-style non-blink mode uses the high bit for bright backgrounds instead of blink, making 0-15 backgrounds possible. For modern CLI output, use ordinary SGR bright background codes only when the terminal and color policy support them.

## Palette Rules

Pick one dominant hue family, one shadow family, and one highlight family. Use gray and black for depth, separation, and crisp small details.

Use high contrast at focal edges and low contrast in large interior masses. Dense terminal art becomes muddy when every cell receives maximum contrast.

Use background color deliberately. A foreground shade character over a colored background doubles the available perceived tones, but it also makes no-color fallback harder. For CLI banners, prefer foreground-only art unless the banner is explicitly decorative.

## Glyph Discipline

Create the large form with no more than six glyphs. Add accents after the silhouette works.

Use box drawing for frames, panels, circuitry, architecture, UI chrome, and lettering scaffolds.

Use block and shade glyphs for volume, portraits, creatures, logos, terrain, smoke, fire, and gradients.

Use punctuation texture only when CP437 blocks cannot express the surface. In oldschool ASCII styles, punctuation can carry slopes and fine texture; in CP437 block ANSI, punctuation should be intentional detail rather than filler.
