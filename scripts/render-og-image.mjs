#!/usr/bin/env node
// Renders the OG card as an engineer's plot sheet (TUI/technical drawing style)
// using satori + @resvg/resvg-js.
//
// Usage: node scripts/render-og-image.mjs
// Wired into `pnpm build` / `pnpm generate` so the image is always fresh.

import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const root = resolve(__dirname, '..')

const WIDTH = 1200
const HEIGHT = 630
const OUT = resolve(root, 'public/og-image.png')

// Tokens mirrored from app/assets/css/main.css (dark ground).
const C = {
  ground: '#0a0c0b',
  raised: '#101513',
  sunken: '#161c19',
  ink: '#dbe4dc',
  dim: '#8b988d',
  faint: '#5b675f',
  rule: '#29332c',
  ruleStrong: '#3e4b41',
  phosphor: '#7dffa0',
}
const SPECTRA = ['#ff3d81', '#ffb43d', '#7dffa0', '#46d5ff', '#b07dff']

const el = (style, children, type = 'div') => ({ type, props: { style, children } })

const load = (p) => readFile(resolve(root, 'node_modules', p))
const [aleo, mono400, mono500] = await Promise.all([
  load('@fontsource/aleo/files/aleo-latin-500-normal.woff'),
  load('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff'),
  load('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff'),
])

const portrait = await readFile(resolve(root, 'public/me-trim.png'))
const portraitUri = `data:image/png;base64,${portrait.toString('base64')}`

const bracket = (corner) => {
  const style = {
    position: 'absolute',
    width: '18px',
    height: '18px',
    borderColor: C.ruleStrong,
    borderStyle: 'solid',
    borderTopWidth: corner === 'tl' || corner === 'tr' ? '2px' : '0',
    borderBottomWidth: corner === 'bl' || corner === 'br' ? '2px' : '0',
    borderLeftWidth: corner === 'tl' || corner === 'bl' ? '2px' : '0',
    borderRightWidth: corner === 'tr' || corner === 'br' ? '2px' : '0',
  }
  style[corner === 'tl' || corner === 'tr' ? 'top' : 'bottom'] = '-1px'
  style[corner === 'tl' || corner === 'bl' ? 'left' : 'right'] = '-1px'
  return el(style, '')
}

const cell = (key, value, last = false) => {
  const style = {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    flex: 1,
    padding: '14px 20px',
  }
  if (!last) style.borderRight = `1px solid ${C.rule}`
  return el(style, [
    el({ fontSize: '12px', letterSpacing: '0.12em', color: C.faint }, key.toUpperCase()),
    el({ fontSize: '16px', color: C.ink }, value),
  ])
}

const card = el(
  {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',
    border: `1px solid ${C.ruleStrong}`,
    background: C.raised,
    position: 'relative',
  },
  [
    bracket('tl'),
    bracket('br'),
    // caption bar
    el(
      {
        display: 'flex',
        justifyContent: 'space-between',
        padding: '12px 22px',
        borderBottom: `1px solid ${C.rule}`,
        color: C.faint,
        fontSize: '15px',
        letterSpacing: '0.06em',
        flex: 'none',
      },
      [el({}, 'fig. 01 — subject'), el({}, `plot · ${WIDTH} × ${HEIGHT}`)],
    ),
    // field
    el({ display: 'flex', flex: 1, minHeight: 0 }, [
      el(
        {
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          gap: '22px',
          flex: 1,
          padding: '44px 48px',
          minWidth: 0,
        },
        [
          el({ fontSize: '15px', letterSpacing: '0.2em', color: C.faint }, '// PAULMELERO.COM'),
          el(
            {
              fontFamily: 'Aleo',
              fontSize: '84px',
              fontWeight: 500,
              lineHeight: 1.02,
              letterSpacing: '-0.03em',
              color: C.ink,
            },
            'Paul Melero',
          ),
          el({ display: 'flex', alignItems: 'center', gap: '14px', color: C.phosphor, fontSize: '21px', letterSpacing: '0.1em' }, [
            el({ width: '48px', height: '2px', background: C.phosphor }, ''),
            el({}, 'human | engineer'),
          ]),
          el(
            { fontSize: '19px', lineHeight: 1.5, color: C.dim, maxWidth: '520px' },
            'I build things, sometimes with code. Twenty years on the web.',
          ),
          el({ display: 'flex', alignItems: 'center', gap: '14px', marginTop: '6px' }, [
            el({ fontSize: '13px', letterSpacing: '0.1em', color: C.faint }, 'legend'),
            ...SPECTRA.map((c) =>
              el({ width: '34px', height: '14px', border: `1px solid ${C.ruleStrong}`, background: c }, ''),
            ),
          ]),
        ],
      ),
      // portrait figure
      el(
        {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '14px',
          width: '400px',
          flex: 'none',
          borderLeft: `1px solid ${C.rule}`,
          padding: '36px',
        },
        [
          el(
            {
              display: 'flex',
              border: `1px solid ${C.rule}`,
              background: C.sunken,
              padding: '10px',
            },
            [{ type: 'img', props: { src: portraitUri, width: 250, height: 318, style: { display: 'block' } } }],
          ),
          el({ fontSize: '13px', letterSpacing: '0.1em', color: C.faint }, 'fig. 01 · 364 × 463'),
        ],
      ),
    ]),
    // title block
    el(
      { display: 'flex', borderTop: `1px solid ${C.ruleStrong}`, flex: 'none' },
      [
        cell('project', 'paulmelero.com'),
        cell('subject', 'Paul Melero'),
        cell('role', 'human | engineer'),
        cell('rev', '2026', true),
      ],
    ),
  ],
)

const svg = await satori(
  el(
    {
      display: 'flex',
      width: `${WIDTH}px`,
      height: `${HEIGHT}px`,
      padding: '36px',
      background: C.ground,
      color: C.ink,
      fontFamily: 'IBM Plex Mono',
    },
    [card],
  ),
  {
    width: WIDTH,
    height: HEIGHT,
    fonts: [
      { name: 'Aleo', data: aleo, weight: 500, style: 'normal' },
      { name: 'IBM Plex Mono', data: mono400, weight: 400, style: 'normal' },
      { name: 'IBM Plex Mono', data: mono500, weight: 500, style: 'normal' },
    ],
  },
)

const png = new Resvg(svg).render().asPng()
await mkdir(dirname(OUT), { recursive: true })
await writeFile(OUT, png)
console.log(`✔ ${OUT}`)