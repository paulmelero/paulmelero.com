---
name: Paul Melero — paulmelero.com
description: A personal landing card built as an engineer's plot sheet in ASCII/TUI materials.
colors:
  ground: "#0a0c0b"
  ground-raised: "#101513"
  ground-sunken: "#161c19"
  ink: "#dbe4dc"
  ink-dim: "#8b988d"
  ink-faint: "#5b675f"
  rule: "#29332c"
  rule-strong: "#3e4b41"
  phosphor: "#7dffa0"
  phosphor-soft: "#b9ffd0"
  phosphor-ink: "#04130a"
  paper: "#f2efe6"
  paper-raised: "#e9e4d6"
  paper-rule: "#cfc8b5"
  paper-rule-strong: "#ada58c"
  paper-accent: "#0b7a40"
  spectral-magenta: "#ff3d81"
  spectral-amber: "#ffb43d"
  spectral-cyan: "#46d5ff"
  spectral-violet: "#b07dff"
typography:
  display:
    fontFamily: "Aleo, ui-serif, Georgia, serif"
    fontSize: "clamp(2.25rem, 1.1rem + 4.6vw, 4.75rem)"
    fontWeight: 500
    lineHeight: 0.98
    letterSpacing: "-0.03em"
  lead:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "clamp(1.05rem, 0.95rem + 0.6vw, 1.375rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    letterSpacing: "0.08em"
  decoration:
    fontFamily: "IBM Plex Mono, ui-monospace, monospace"
    fontSize: "0.6875rem"
    fontWeight: 400
    letterSpacing: "0.04em"
rounded:
  none: "0px"
spacing:
  1: "0.25rem"
  2: "0.5rem"
  3: "0.75rem"
  4: "1rem"
  5: "1.5rem"
  6: "2rem"
  7: "3rem"
  8: "4.5rem"
components:
  command-button:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.75rem"
    typography: "{typography.label}"
  command-button-solid:
    backgroundColor: "{colors.phosphor}"
    textColor: "{colors.phosphor-ink}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.75rem"
    typography: "{typography.label}"
  swatch:
    backgroundColor: "{colors.ground-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    size: "22px x 12px"
  link-row:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "1rem 0.75rem 1rem 0.75rem"
---

# Design System: Paul Melero — paulmelero.com

## Overview

**Creative North Star: "The Engineer's Plot Sheet"**

This is a landing card argued as a technical drawing set in terminal materials. The portrait is not a photograph on a hero; it is the plotted figure. Everything around it behaves like annotation: ruled fields, tick labels, a legend, a title block. The page reads as something computed rather than composed, which is the point — "human | engineer" is demonstrated by the artifact, not claimed in copy.

The system is deliberately flat and thin. There are no shadows, no gradients used as decoration, no rounded corners, no glass. Depth comes from value relationships between three near-black grounds and from the one-per-layer rule ink. Color is rationed hard: a single phosphor accent does the work, and the portrait's own spectrum is the only saturated field on the page. Space is generous and grain is fine — the developer-facing refinement lives in the 11px annotation layer, never in the body copy.

It ships in two themes because it is used in two lights: a dark ground for a room and a projector, a warm-paper ground for daylight. Both are first-class, not inverted approximations.

**Key Characteristics:**
- Flat, shadowless, zero-radius; lines are the only depth device.
- One accent (phosphor); the portrait's spectrum is the sole saturated field.
- Monospace carries the interface; a single grotesk carries the name.
- Ruled bands and a title block organize the page, not cards.
- Decoration drops to 11px; body text never does.

## Colors

A rationed palette: near-black grounds, ink for text, phosphor for action, and the portrait's spectrum held back for the one moment that needs it.

### Primary
- **Phosphor Green** (#7dffa0 dark / #0b7a40 light): the single action color. Command buttons, hover states, the identity prompt, the copy confirmation, focus rings. It marks interaction and nothing else.

### Secondary
- **Portrait Spectrum** (#ff3d81, #ffb43d, #7dffa0, #46d5ff, #b07dff dark; deepened equivalents on paper): a five-hue legend bound to the portrait's dithered colours. Each swatch tints the render toward its hue. This is the only place saturated colour runs free.

### Neutral
- **Ground** (#0a0c0b dark / #f2efe6 light): the page field. Near-black with a green cast; warm paper in light.
- **Ground Raised** (#101513 / #e9e4d6): the plot panel and hover row fill, one step off the field.
- **Ink** (#dbe4dc / #14170f): primary text.
- **Ink Dim** (#8b988d / #5d6454): secondary text and lead copy.
- **Ink Faint** (#5b675f / #8c9280): annotation, labels, and 11px decoration only.
- **Rule** (#29332c / #cfc8b5) and **Rule Strong** (#3e4b41 / #ada58c): the hairline system — dividers, panel borders, corner brackets, tick rulers, scrollbar thumbs.

**The One Accent Rule.** Phosphor is used on interaction and the identity prompt. Ornament, headings, and body never take it. Its rarity is the point.

**The Paper Ground Rule.** The light theme is a distinct palette, not an inversion. Its ink is warm black and its accent is a deep green; never reuse phosphor on paper.

## Typography

**Display Font:** Aleo (with ui-serif, Georgia fallback)
**Body / Interface Font:** IBM Plex Mono (with ui-monospace, monospace fallback)

**Character:** A single slab serif against a broad monospace field. The monospace is functional, not costume — this page is full of measurement, coordinates, and annotation. The slab serif appears only for the proper nouns a visitor should remember: the name, the two project links, the email address.

### Hierarchy
- **Display** (500, clamp(2.25rem, 1.1rem + 4.6vw, 4.75rem), 0.98): the name and nothing else.
- **Lead** (400 mono, clamp(1.05–1.375rem), 1.5): the one-line bio and the contact sentence, held to a 62ch measure.
- **Title** (500 Aleo, clamp to 2rem): the contact email and the project-link names.
- **Body** (400 mono, 0.9375rem, 1.6): link descriptions and footer values.
- **Label** (400 mono, 0.75rem, 0.08em, uppercase): section titles, nav, button text, annotation.
- **Decoration** (400 mono, 0.6875rem / 11px): plot-bar captions, dimension labels, legend hints — decoration only, never information a visitor needs.

**The 11px Floor Rule.** Nothing below 11px ships, and 11px is reserved for aria-hidden decoration. Any text a visitor must read is ≥12px.

## Layout

A single centered column on a 76rem container with fluid gutters (clamp(1rem, 4vw, 3rem)). The hero is a bordered plot panel: a caption bar on top, then a three-track field (`minmax(0,1fr) auto minmax(0,1fr)`) holding a vertical dimension rule, the portrait, and the legend. Below it, the identity caption is separated by a rule. Content sections are full-width bands divided by hairlines rather than cards. The footer is a four-column title block on desktop, two columns under 720px.

The spacing rhythm runs 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72px, always more space above a heading than below. The portrait scales from `clamp(220px, 46vh, 560px)` and the whole field collapses to one centered column at 860px, where the dimension rule and the phone hint are hidden.

## Elevation & Depth

There are no shadows anywhere. Depth is carried entirely by value and line: three grounds one step apart, a single hairline weight for structure and a stronger one for the outer frame, and the portrait's own density. Hover is expressed as a ground shift or a border/ink change, never as lift.

**The Flat-By-Default Rule.** No `box-shadow` on any surface. If an element needs to separate from the page, change its border, its ground, or its spacing.

## Shapes

Strictly rectilinear: 0px radius everywhere, 1px hairlines, square line caps and joins on every drawn icon. The recurring silhouette is the corner bracket — a doubled short rule at the panel's top-left and bottom-right — and the tick ruler along the portrait's edge. Progress bars and rounded chips do not exist in this system.

## Components

### Buttons
- **Shape:** square (0 radius), 1px rule border.
- **Primary (command-solid):** phosphor ground, phosphor-ink text, 0.5rem × 0.75rem padding, 12px label type.
- **Ghost (command):** transparent ground, rule-strong border, ink text; hover shifts border and text to phosphor.
- **Hover / Focus:** color transitions only (~0.18s); global 2px phosphor focus ring at 2px offset.

### Navigation
- **Style:** 12px mono labels, ink-dim at rest, phosphor on hover; anchors to `#work` and `#contact`. Sticky header on the ground with a bottom hairline.
- **Mobile:** links collapse behind a hamburger that reveals a stacked menu; the theme toggle stays in the bar.

### Swatches (legend)
- **Style:** 22×12px rectangles, 1px rule-strong border, filled with one spectrum hue; `aria-pressed` shows the active tint with an ink border and a 4px shift.
- **State:** click toggles a tint on the portrait; click again clears it.

### Link rows
- **Style:** a four-column grid (mark / name / description / arrow) divided by hairlines, no card container. Hover raises the row to ground-raised and turns the name phosphor.
- **Mark:** a literal `->` in the annotation layer, not an icon.

### Title block (signature component)
- **Style:** a bordered grid of labelled cells (`project` / `subject` / `role` / `rev` / `elsewhere` / `note`), key in 11px ink-faint uppercase, value in 13px mono. Socials are drawn brand SVGs at 15px inside 28px square ruled targets.

### ASCII portrait (signature component)
- **Behavior:** a Three.js fullscreen-quad shader samples a colour plate (`me-trim.png`) and a high-contrast luminance map (`me-density.png`) into a grid of character cells. An 8×8 ordered Bayer threshold drives a ten-step glyph ramp drawn from an IBM Plex Mono atlas texture, coloured by the source hue. A pointer tilts the sheet in perspective and drives a holographic iridescent reflection across the glyphs; the legend swatches tint the whole field. Idle motion is a reflected-eased ping-pong.
- **Fallbacks:** when WebGL2 or Three.js is unavailable, the pre-shader 2D-canvas renderer takes over; the canvas carries `role="img"` with a text label; under `prefers-reduced-motion` it renders a single static frame and ignores the pointer.

## Do's and Don'ts

### Do:
- **Do** keep the portrait's spectrum the only saturated field; everything else is ink, ground, and phosphor.
- **Do** express depth with the three grounds and the two hairline weights.
- **Do** hold body text at ≥15px and keep 11px strictly to aria-hidden decoration.
- **Do** make `prefers-reduced-motion` render a static portrait and disable tilt and shimmer.
- **Do** keep the monospace functional: it is the medium for coordinates, rules, and annotation.

### Don't:
- **Don't** add `box-shadow`, rounded corners, or glass to any surface.
- **Don't** use phosphor for headings, ornament, or large fills outside the portrait legend.
- **Don't** invert the light theme from the dark one; use its own warm-black ink and deep-green accent.
- **Don't** expose decorative ascii, tick rulers, dimension labels, or the `->` mark to assistive tech.
- **Don't** let the portrait's pointer tilt or shimmer run under `prefers-reduced-motion`.