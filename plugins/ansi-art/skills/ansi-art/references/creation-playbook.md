# Creation Playbook

Use this reference when the task is to make beautiful original terminal art, not just choose a file format.

## Design Passes

### 1. Thumbnail

Draw the subject in the fewest cells possible. Use spaces and full blocks first.

Check:

- The silhouette reads without color.
- The focal point is obvious.
- The composition has breathing room.
- The art fits the target width at normal terminal zoom.
- The full subject is blocked in before local shading begins.

### 2. Massing

Replace crude blocks with half blocks where they improve contour:

```text
▀ for top edges
▄ for bottom edges
▌ and ▐ for side edges
█ for solid mass
```

Keep large areas calm. Small terminal art fails when every cell tries to be detail.

### 3. Light

Choose one light source. Mark the bright side, midtone, shadow, and deepest shadow before adding texture.

Use this common ramp:

```text
highlight:       light color on space or ░
midtone:         ▒
shadow:          ▓
core shadow:     █ or dark foreground/background
edge highlight:  ▀ ▄ ▌ ▐ in bright color
```

Use black or dark gray for small cut lines, occlusion shadows, eye sockets, folds, underside edges, and separation between overlapping shapes.

### 4. Blend

Blend along the form direction. For a curved form, change density along the curve rather than in straight horizontal bands.

Use vertical or diagonal smears when the style needs grit. Use every second or third row/cell so the original form remains readable.

Use foreground/background inversion as a tone tool when color output is allowed. A light shade glyph with dark foreground over bright background can approximate a different density than the same glyph over black.

### 5. Lettering

For logos, build letters as shapes first.

Start with 5-7 cell tall block letters. Use half blocks to round terminals and shade characters to bevel faces. Keep counters and holes larger than they seem to need; terminal glyphs fill visually at normal size.

For small CLI marks, use a symbol plus ordinary text instead of forcing unreadable block letters.

### 6. Frame And UI

Use box drawing for panels and grids:

```text
┌────┐  ╔════╗
│    │  ║    ║
└────┘  ╚════╝
```

Use single-line boxes for quiet utility UI. Use double-line boxes for title cards, splash screens, and oldschool BBS energy.

### 7. Polish

Zoom out. The whole image should read before individual cells feel clever.

Remove texture that fights the silhouette. Increase contrast at the focal point. Reduce contrast near quiet edges. Check the no-color fallback. Check one narrow terminal case.

## Recipes

### CLI Banner

Use 40-64 columns and 6-12 rows. Prefer foreground-only color. Keep a 1-3 row compact mark for narrow terminals. Include the product name as normal terminal text near the art when block lettering would be cramped.

### BBS Logo

Use 80 columns or wider. Build chunky custom letters. Add bevels with `▀`, `▄`, and shade glyphs. Use a small signature or metadata line only after the main wordmark reads clearly.

### Portrait Or Character

Use at least 40 columns wide for a face. Place eyes first. Reserve high contrast for eyes, nose bridge, mouth corners, and silhouette breaks. Use shade fields for cheeks, hair masses, and clothing folds.

### Object Or Icon

Use a strong silhouette and one material language. Metal wants bright edge highlights and hard black cuts. Glass wants sparse highlights and low-density interior texture. Smoke and flame want broken shade ramps and asymmetry.

## Agent Output Checklist

Return the art in a fenced block when it is plain text. Explain any required terminal color settings after the block.

For ANSI-colored output, include both:

- A literal preview using Unicode CP437 glyphs.
- Implementation notes showing how colors/styles should be encoded.

For code changes, include tests that verify fixed row widths and allowed glyphs.

For reference-driven requests, name the sources studied and describe the borrowed technique in general terms: palette, density ramp, framing, lettering, or light treatment.
