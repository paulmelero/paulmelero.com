<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    src?: string
    densitySrc?: string
    label?: string
    theme?: 'dark' | 'light'
    activeHue?: number | null
  }>(),
  {
    src: '/me-trim.png',
    densitySrc: '/me-density.png',
    label: "ASCII and dithered rendering of Paul Melero's portrait",
    theme: 'dark',
    activeHue: null,
  },
)

const wrapEl = ref<HTMLElement | null>(null)
const canvasEl = ref<HTMLCanvasElement | null>(null)

const RAMP = ' .:-=+*#%@'
const BAYER = [
  [0, 8, 2, 10],
  [12, 4, 14, 6],
  [3, 11, 1, 9],
  [15, 7, 13, 5],
]

type Cell = {
  glyph: string
  h: number
  s: number
  density: number
  cov: number
}

const cells: Cell[] = []
let cols = 0
let rows = 0
let cellW = 0
let cellH = 0
let ctx: CanvasRenderingContext2D | null = null
let source: HTMLImageElement | null = null
let densitySource: HTMLImageElement | null = null
let sampler: HTMLCanvasElement | null = null
let rafId = 0
let running = false

const reducedMotion = ref(false)
let tiltX = 0
let tiltY = 0
let targetX = 0
let targetY = 0
let phase = 0
let pointerInside = false
let lastShimmer = 0

function clamp(v: number, min: number, max: number) {
  return v < min ? min : v > max ? max : v
}

function rgbToHsl(r: number, g: number, b: number) {
  r /= 255
  g /= 255
  b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const l = (max + min) / 2
  let h = 0
  let s = 0
  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    if (max === r) h = (g - b) / d + (g < b ? 6 : 0)
    else if (max === g) h = (b - r) / d + 2
    else h = (r - g) / d + 4
    h /= 6
  }
  return { h: h * 360, s, l }
}

function mixHue(a: number, b: number, t: number) {
  const d = ((b - a) % 360 + 540) % 360 - 180
  return (a + d * t + 360) % 360
}

function buildSampler() {
  if (!source || !wrapEl.value) return
  const side = wrapEl.value.clientWidth
  if (!side) return

  cellH = clamp(side / 38, 8, 16)
  cellW = cellH * 0.62
  rows = Math.max(24, Math.floor(side / cellH))
  cols = Math.max(38, Math.round(rows * 1.61))

  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  const canvas = canvasEl.value
  if (!canvas) return
  canvas.width = Math.round(side * dpr)
  canvas.height = Math.round(side * dpr)
  canvas.style.width = `${side}px`
  canvas.style.height = `${side}px`
  ctx = canvas.getContext('2d')
  if (!ctx) return
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  sampler ??= document.createElement('canvas')
  sampler.width = cols
  sampler.height = rows
  const sctx = sampler.getContext('2d', { willReadFrequently: true })
  if (!sctx) return

  // Contain the image inside the grid so its aspect is preserved once the
  // non-square character cells compress it back on screen.
  const imageAspect = source.naturalWidth / source.naturalHeight
  let dw = rows * (imageAspect / (cellW / cellH))
  let dh = rows
  let dx = (cols - dw) / 2
  let dy = 0
  if (dw > cols) {
    dw = cols
    dh = cols * ((cellW / cellH) / imageAspect)
    dx = 0
    dy = (rows - dh) / 2
  }

  function sample(image: HTMLImageElement) {
    sctx.clearRect(0, 0, cols, rows)
    sctx.imageSmoothingEnabled = false
    sctx.drawImage(image, dx, dy, dw, dh)
    return sctx.getImageData(0, 0, cols, rows).data
  }

  const colour = sample(source)
  const densityMap = densitySource ? sample(densitySource) : colour

  // First pass: find the density range across the figure so the ramp is used fully.
  let min = 1
  let max = 0
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const i = (y * cols + x) * 4
      if (colour[i + 3] / 255 < 0.28) continue
      const lum = (0.2126 * densityMap[i] + 0.7152 * densityMap[i + 1] + 0.0722 * densityMap[i + 2]) / 255
      if (lum < min) min = lum
      if (lum > max) max = lum
    }
  }
  const range = Math.max(max - min, 0.05)

  cells.length = 0
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const i = (y * cols + x) * 4
      const a = colour[i + 3] / 255
      const dlum =
        (0.2126 * densityMap[i] + 0.7152 * densityMap[i + 1] + 0.0722 * densityMap[i + 2]) / 255
      const density = a < 0.28 ? 0 : Math.pow(clamp((dlum - min) / range, 0, 1), 1.2)
      const bayer = (BAYER[y % 4][x % 4] / 16 - 0.47) * 0.75
      const level = Math.round(clamp(density * 1.25 + bayer, 0, 1) * (RAMP.length - 1))
      const glyph = a < 0.28 ? ' ' : RAMP[level]
      const { h, s } = rgbToHsl(colour[i], colour[i + 1], colour[i + 2])
      cells.push({ glyph, h, s, density, cov: a })
    }
  }
}

function draw() {
  if (!ctx) return
  const light = props.theme === 'light'
  const canvas = canvasEl.value
  if (!canvas) return
  const side = rows * cellH
  ctx.clearRect(0, 0, side, side)
  ctx.font = `500 ${cellH}px "IBM Plex Mono", ui-monospace, monospace`
  ctx.textBaseline = 'top'
  ctx.textAlign = 'left'

  const tilt = pointerInside || targetX !== 0 || targetY !== 0 ? 1 : 0
  const sweep = 0.5 + tiltX * 0.5 + Math.sin(phase * 0.6) * 0.12
  const hueBoost = props.activeHue != null ? 1 : 0

  for (let y = 0; y < rows; y++) {
    const ny = y / (rows - 1)
    for (let x = 0; x < cols; x++) {
      const cell = cells[y * cols + x]
      if (!cell || cell.glyph === ' ') continue
      const nx = x / (cols - 1)

      const t = cell.density
      const baseSat = clamp(cell.s * (light ? 1.75 : 1.5), 0.03, 1)
      const baseLum = light ? 0.19 + t * 0.34 : 0.37 + t * 0.38

      const targetHue =
        props.activeHue != null
          ? props.activeHue
          : (phase * 34 + nx * 120 + ny * 66) % 360
      const k =
        (hueBoost ? 0.5 : 0.16 + 0.28 * tilt) *
        (0.25 + 0.75 * baseSat) *
        (0.5 + 0.5 * Math.abs(nx - 0.5) * 2)

      const hue = mixHue(cell.h, targetHue, k)
      const band = Math.max(0, 1 - Math.abs(nx * 0.6 + ny * 0.4 - sweep) * 4)
      const lum = clamp(baseLum + band * 0.16 + k * 0.07, 0.12, 0.9)
      const sat = clamp(baseSat * (0.95 + 0.3 * k), 0.08, 1)

      ctx.fillStyle = `hsl(${hue | 0} ${(sat * 100) | 0}% ${(lum * 100) | 0}%)`
      ctx.fillText(cell.glyph, x * cellW, y * cellH)
    }
  }
}

function frame(now: number) {
  if (!running) return
  const dt = now - (lastShimmer || now)
  if (lastShimmer === 0) lastShimmer = now

  tiltX += (targetX - tiltX) * 0.12
  tiltY += (targetY - tiltY) * 0.12
  const el = wrapEl.value
  if (el && !reducedMotion.value) {
    el.style.transform =
      `perspective(920px) rotateX(${(-tiltY * 11).toFixed(2)}deg) ` +
      `rotateY(${(tiltX * 13).toFixed(2)}deg) translateZ(0)`
  }

  const idle = !pointerInside
  if (!idle || dt > 240) {
    if (!idle) {
      phase += 0.012
      draw()
    } else {
      phase += 0.004
      draw()
    }
    lastShimmer = now
  }
  rafId = requestAnimationFrame(frame)
}

function start() {
  if (running) return
  running = true
  lastShimmer = 0
  rafId = requestAnimationFrame(frame)
}

function stop() {
  running = false
  cancelAnimationFrame(rafId)
}

function onPointerMove(e: PointerEvent) {
  if (reducedMotion.value) return
  const el = wrapEl.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  targetX = (e.clientX - rect.left) / rect.width - 0.5
  targetY = (e.clientY - rect.top) / rect.height - 0.5
  pointerInside = true
  start()
}

function onPointerLeave() {
  pointerInside = false
  targetX = 0
  targetY = 0
}

let io: IntersectionObserver | null = null
let ro: ResizeObserver | null = null
let resizeTimer: ReturnType<typeof setTimeout> | null = null

onMounted(async () => {
  reducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  function load(src: string) {
    return new Promise<HTMLImageElement>((resolve, reject) => {
      const image = new Image()
      image.decoding = 'async'
      image.onload = () => resolve(image)
      image.onerror = reject
      image.src = src
    })
  }

  try {
    ;[source, densitySource] = await Promise.all([load(props.src), load(props.densitySrc)])
  } catch {
    try {
      source = await load(props.src)
    } catch {
      return
    }
  }
  if (document.fonts?.ready) await document.fonts.ready

  buildSampler()
  if (reducedMotion.value) {
    draw()
    return
  }
  start()

  io = new IntersectionObserver(
    (entries) => {
      if (entries[0]?.isIntersecting) start()
      else stop()
    },
    { threshold: 0 },
  )
  if (wrapEl.value) io.observe(wrapEl.value)

  ro = new ResizeObserver(() => {
    if (resizeTimer) clearTimeout(resizeTimer)
    resizeTimer = setTimeout(() => {
      buildSampler()
      if (reducedMotion.value) draw()
    }, 140)
  })
  if (wrapEl.value) ro.observe(wrapEl.value)
})

onBeforeUnmount(() => {
  stop()
  io?.disconnect()
  ro?.disconnect()
  if (resizeTimer) clearTimeout(resizeTimer)
})

watch(
  () => props.activeHue,
  () => {
    if (reducedMotion.value) draw()
  },
)

watch(
  () => props.theme,
  () => {
    if (reducedMotion.value) draw()
  },
)
</script>

<template>
  <div
    ref="wrapEl"
    class="ascii-portrait"
    @pointermove="onPointerMove"
    @pointerleave="onPointerLeave"
    @pointercancel="onPointerLeave"
  >
    <canvas ref="canvasEl" class="ascii-portrait__canvas" role="img" :aria-label="label" />
  </div>
</template>

<style scoped>
.ascii-portrait {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  transform-style: preserve-3d;
  will-change: transform;
}

.ascii-portrait__canvas {
  display: block;
  image-rendering: auto;
}
</style>