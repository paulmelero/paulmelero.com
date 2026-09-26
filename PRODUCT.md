# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: people Paul Melero meets while presenting — conference audiences, collaborators, recruiters, and peers who scan the URL from a slide, talk, or chat. Situation: on a laptop or phone, with seconds of attention, often wanting to place a name and reach a link or an email. No account, no settings, no return visits required.

## Product Purpose

A durable personal landing card for Paul Melero at paulmelero.com. It is a minimal, presentation-ready front door that (a) states who he is in one line, (b) routes visitors to his real work at graficos.net and flipthecoin.app plus his social profiles, and (c) offers a direct email contact. Success: within a few seconds a first-time visitor knows who this is, can reach a link or send mail, and the page looks crafted enough to sit behind or beside a live presentation.

## Positioning

Unlike graficos.net — the long-running personal blog and archive — paulmelero.com is deliberately a single-screen identity card. It carries none of the blog's content weight; it exists to be the clean, memorable pointer that a presentation URL can live on permanently. The ascii/dither render of Paul's own portrait is the one thing a generic link-in-bio page could not truthfully copy.

## Operating Context

Used live during presentations (projected, and visited from slides), shared in chat and on social profiles, and found via search for the name. A recurring task: copying the email or clicking through to graficos.net / flipthecoin.app. Content is expected to change rarely; it is a placeholder intended to stay valid while the main site evolves.

## Capabilities and Constraints

- Single-page landing. In-page anchor navigation only: a "work/links" section and a contact section. No blog, no CMS, no auth, no forms.
- External destinations: graficos.net, flipthecoin.app, plus social profiles extracted from graficos.net (Bluesky, GitHub, LinkedIn). May include an Atom/RSS link if useful.
- Contact email: `paul@paulmelero.com`.
- Dark and light themes; user-switchable.
- Nuxt 4 with `@nuxt/fonts`, `@nuxt/icon`, `@nuxt/eslint` already scaffolded. Fonts fixed by the user: Space Grotesk (300 700) and IBM Plex Mono (100–700, normal + italic).
- The portrait (`public/me.png`) is rendered as an interactive ascii/dither treatment in the hero; implementation may be WebGL/Three.js or a lighter equivalent, at the user's stated openness. Slightly interactive (card-tilt on hover) with a holographic/reflection character tied to the ascii colours.
- Explicitly excluded from this session: any changes to graficos.net.

## Brand Commitments

Paul's own identity, voiced as "human | engineer". Binding aesthetic constraints volunteered by the user and to be preserved, not expanded here (visual world is decided in the design flow): ascii / terminal (TUI) inspired; minimalistic; dark and light themes; prefer ascii-oriented decorative elements over pixelated chunks; small fonts allowed only for decoration (≥11px); avoid excessive rules/lines; enjoy corner ornaments; no scroll hijacking; a11y considered for decorative ascii.

## Evidence on Hand

- `public/me.png` — the source portrait (colourful paint explosion around a smiling man in glasses), the basis for the ascii render.
- graficos.net content and structure (home + contact) as reference for bio voice, link set, and social profiles.
- No testimonials, benchmarks, or commercial claims exist or should be invented.

## Product Principles

1. One screen, one idea: identity first, everything else one click away.
2. The portrait is the product demonstration; the interface around it recedes.
3. Craft over content volume — the page earns attention by looking deliberate, not by saying more.
4. Honest and current: no fabricated claims, no dead links, no decorative noise that implies depth that is not there.
5. Degrade gracefully: readable and useful with the ascii render absent or reduced-motion preferred.

## Accessibility & Inclusion

- Decorative ascii must not be exposed to assistive tech as meaningful text; the portrait carries an accessible name/description, not raw glyph soup.
- Honour `prefers-reduced-motion`: no tilt, no holographic motion, portrait renders static.
- Reasoning: dark/light themes and legible body type; small sizes reserved strictly for decoration.