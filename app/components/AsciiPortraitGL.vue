<script setup lang="ts">
import type * as ThreeNS from 'three'

type ThreeModule = typeof import('three')

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

const emit = defineEmits<{ fail: [] }>()

const wrapEl = ref<HTMLElement | null>(null)
const canvasEl = ref<HTMLCanvasElement | null>(null)

const RAMP = ' .:-=+*#%@'
const AGE_THRESHOLD = 0.28

let three: ThreeModule | null = null
let renderer: ThreeNS.WebGLRenderer | null = null
let scene: ThreeNS.Scene | null = null
let camera: ThreeNS.Camera | null = null
let geometry: ThreeNS.PlaneGeometry | null = null
let material: ThreeNS.ShaderMaterial | null = null

let colorTex: ThreeNS.Texture | null = null
let densityTex: ThreeNS.Texture | null = null
let atlasTex: ThreeNS.CanvasTexture | null = null
let bayerTex: ThreeNS.DataTexture | null = null
let colorImg: ImageBitmap | null = null
let densityImg: ImageBitmap | null = null

let analysis: HTMLCanvasElement | null = null
let analysisCtx: CanvasRenderingContext2D | null = null

let layout = {
  cols: 0,
  rows: 0,
  cellW: 0,
  cellH: 0,
  rect: [0, 0, 0, 0] as number[],
}

let rafId = 0
let running = false
let disposed = false

const reducedMotion = ref(false)
let tiltX = 0
let tiltY = 0
let targetX = 0
let targetY = 0
let pointerInside = false
let clock = 0
let pulse = 0.5
let lastFrame = 0
let lastDraw = 0

function clamp(v: number, min: number, max: number) {
  return v < min ? min : v > max ? max : v
}

function easeReflect(x: number) {
  const t = 1 - Math.abs(1 - (x % 2))
  return t * t * (3 - 2 * t)
}

function makeBayer(size: number) {
  if (!three) return null
  let m: number[][] = [[0]]
  while (m.length < size) {
    const s = m.length
    const next = Array.from({ length: s * 2 }, () =>
      Array<number>(s * 2).fill(0),
    )
    for (let y = 0; y < s; y++) {
      for (let x = 0; x < s; x++) {
        const v = m[y][x] * 4
        next[y][x] = v
        next[y][x + s] = v + 2
        next[y + s][x] = v + 3
        next[y + s][x + s] = v + 1
      }
    }
    m = next
  }
  const data = new Uint8Array(size * size)
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      data[y * size + x] = Math.round((m[y][x] / (size * size)) * 255)
    }
  }
  const tex = new three.DataTexture(
    data,
    size,
    size,
    three.RedFormat,
    three.UnsignedByteType,
  )
  tex.minFilter = three.NearestFilter
  tex.magFilter = three.NearestFilter
  tex.wrapS = three.ClampToEdgeWrapping
  tex.wrapT = three.ClampToEdgeWrapping
  tex.needsUpdate = true
  return tex
}

function buildAtlas(cellW: number, cellH: number) {
  if (!three) return null
  const aw = Math.max(2, Math.round(cellW))
  const ah = Math.max(4, Math.round(cellH))
  const canvas = document.createElement('canvas')
  canvas.width = aw * RAMP.length
  canvas.height = ah
  const c = canvas.getContext('2d')
  if (!c) return null
  c.clearRect(0, 0, canvas.width, canvas.height)
  c.font = `500 ${ah}px "IBM Plex Mono", ui-monospace, monospace`
  c.textBaseline = 'top'
  c.textAlign = 'left'
  c.fillStyle = '#fff'
  for (let i = 0; i < RAMP.length; i++) {
    c.fillText(RAMP[i], i * aw, 0)
  }
  const tex = new three.CanvasTexture(canvas)
  tex.minFilter = three.NearestFilter
  tex.magFilter = three.NearestFilter
  tex.wrapS = three.ClampToEdgeWrapping
  tex.wrapT = three.ClampToEdgeWrapping
  tex.needsUpdate = true
  return tex
}

function computeRect() {
  if (!colorImg) return [0, 0, 0, 0]
  const { cols, rows, cellW, cellH } = layout
  const imageAspect = colorImg.width / colorImg.height
  let dw = rows * (imageAspect / (cellW / cellH))
  let dh = rows
  let dx = (cols - dw) / 2
  let dy = 0
  if (dw > cols) {
    dw = cols
    dh = cols * (cellW / cellH / imageAspect)
    dx = 0
    dy = (rows - dh) / 2
  }
  return [dx, dy, dw, dh]
}

function analyze() {
  if (!colorImg || !densityImg || !analysisCtx || !analysis)
    return { min: 0, range: 1 }
  const { cols, rows } = layout
  const rect = layout.rect
  analysis.width = cols
  analysis.height = rows
  analysisCtx.clearRect(0, 0, cols, rows)
  analysisCtx.imageSmoothingEnabled = false
  analysisCtx.drawImage(densityImg, rect[0], rect[1], rect[2], rect[3])
  const densityMap = analysisCtx.getImageData(0, 0, cols, rows).data
  analysisCtx.clearRect(0, 0, cols, rows)
  analysisCtx.drawImage(colorImg, rect[0], rect[1], rect[2], rect[3])
  const colour = analysisCtx.getImageData(0, 0, cols, rows).data

  let min = 1
  let max = 0
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const i = (y * cols + x) * 4
      if (colour[i + 3] / 255 < AGE_THRESHOLD) continue
      const lum =
        (0.2126 * densityMap[i] +
          0.7152 * densityMap[i + 1] +
          0.0722 * densityMap[i + 2]) /
        255
      if (lum < min) min = lum
      if (lum > max) max = lum
    }
  }
  return { min, range: Math.max(max - min, 0.05) }
}

function applyUniforms() {
  if (!material || !three) return
  const u = material.uniforms
  u.uGrid.value.set(layout.cols, layout.rows)
  u.uRect.value.set(
    layout.rect[0],
    layout.rect[1],
    layout.rect[2],
    layout.rect[3],
  )
  const stats = analyze()
  u.uMin.value = stats.min
  u.uRange.value = stats.range
  u.uLight.value = props.theme === 'light' ? 1 : 0
  u.uTintHue.value = props.activeHue == null ? -1 : props.activeHue
}

function buildLayout() {
  if (
    !three ||
    !renderer ||
    !canvasEl.value ||
    !wrapEl.value ||
    !colorImg ||
    !densityImg
  )
    return
  const side = wrapEl.value.clientWidth
  if (!side) return

  const cellH = clamp(side / 38, 8, 16)
  const cellW = cellH * 0.62
  const rows = Math.max(24, Math.floor(side / cellH))
  const cols = Math.max(38, Math.round(rows * 1.61))
  layout = { cols, rows, cellW, cellH, rect: [0, 0, 0, 0] }
  layout.rect = computeRect()

  const dpr = Math.min(window.devicePixelRatio || 1, 2)
  renderer.setPixelRatio(dpr)
  renderer.setSize(side, side, false)

  if (atlasTex) atlasTex.dispose()
  const nextAtlas = buildAtlas(cellW, cellH)
  if (nextAtlas) {
    atlasTex = nextAtlas
    if (material) material.uniforms.uAtlasTex.value = atlasTex
  }

  applyUniforms()
  renderer.render(scene!, camera!)
}

function draw() {
  if (!renderer || !scene || !camera || !material) return
  material.uniforms.uTilt.value.set(tiltX, tiltY)
  material.uniforms.uPhase.value = clock
  material.uniforms.uPulse.value = pulse
  renderer.render(scene, camera)
}

function frame(now: number) {
  if (!running) return
  const dt = lastFrame ? now - lastFrame : 16
  lastFrame = now

  tiltX += (targetX - tiltX) * 0.12
  tiltY += (targetY - tiltY) * 0.12

  const el = wrapEl.value
  if (el && !reducedMotion.value) {
    el.style.transform =
      `perspective(920px) rotateX(${(-tiltY * 11).toFixed(2)}deg) ` +
      `rotateY(${(tiltX * 13).toFixed(2)}deg) translateZ(0)`
  }

  clock += dt * 0.0012
  pulse = easeReflect(clock)

  // Idle: keep the pulse alive but redraw at a low cadence to spare the GPU.
  const idle = !pointerInside
  if (!idle || now - lastDraw > 240) {
    lastDraw = now
    draw()
  }
  rafId = requestAnimationFrame(frame)
}

function start() {
  if (running || reducedMotion.value) return
  running = true
  lastFrame = 0
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

function onContextLost(e: Event) {
  e.preventDefault()
  stop()
  fail()
}

function fail() {
  if (disposed) return
  disposed = true
  stop()
  emit('fail')
}

const vertexShader = /* glsl */ `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position.xy, 0.0, 1.0);
}
`

const fragmentShader = /* glsl */ `
precision highp float;

varying vec2 vUv;

uniform vec2 uGrid;
uniform vec4 uRect;
uniform float uMin;
uniform float uRange;
uniform vec2 uTilt;
uniform float uPhase;
uniform float uPulse;
uniform float uTintHue;
uniform float uLight;

uniform sampler2D uColorTex;
uniform sampler2D uDensityTex;
uniform sampler2D uAtlasTex;
uniform sampler2D uBayerTex;

const float RAMP_LEN = 10.0;

vec3 rgb2hsv(vec3 c) {
  vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
  vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
  vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
  float d = q.x - min(q.w, q.y);
  float e = 1.0e-10;
  return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
  vec2 g = vUv * uGrid;
  vec2 n = g / uGrid;
  vec2 cell = floor(g);
  vec2 cellLocal = fract(g);
  vec2 center = cell + 0.5;
  vec2 imgUv = (center - uRect.xy) / uRect.zw;

  if (imgUv.x < 0.0 || imgUv.x > 1.0 || imgUv.y < 0.0 || imgUv.y > 1.0) {
    gl_FragColor = vec4(0.0);
    return;
  }

  vec4 src = texture2D(uColorTex, imgUv);
  float a = src.a;
  if (a < 0.28) {
    gl_FragColor = vec4(0.0);
    return;
  }

  float dlum = dot(texture2D(uDensityTex, imgUv).rgb, vec3(0.2126, 0.7152, 0.0722));
  float density = clamp((dlum - uMin) / uRange, 0.0, 1.0);
  density = pow(density, 1.2);

  float bayer = (texture2D(uBayerTex, (mod(cell, 8.0) + 0.5) / 8.0).r - 0.47) * 0.75;
  float level = clamp(density * 1.25 + bayer, 0.0, 1.0) * (RAMP_LEN - 1.0);
  float glyphIndex = floor(level + 0.5);
  // On paper the ink marks the shadows, so coverage mirrors the density.
  if (uLight > 0.5) glyphIndex = (RAMP_LEN - 1.0) - glyphIndex;

  vec2 atlasUv = vec2((glyphIndex + cellLocal.x) / RAMP_LEN, cellLocal.y);
  float mask = texture2D(uAtlasTex, atlasUv).a;

  vec3 hsv = rgb2hsv(src.rgb);
  float hue = hsv.x * 360.0;
  float baseSat = clamp(hsv.y * (uLight > 0.5 ? 1.75 : 1.5), 0.03, 1.0);
  float baseLum = uLight > 0.5 ? 0.19 + density * 0.34 : 0.37 + density * 0.38;

  float tilt = clamp(length(uTilt) * 2.0, 0.0, 1.0);
  float targetHue = uTintHue >= 0.0
    ? uTintHue
    : mod(uPhase * 34.0 + n.x * 120.0 + n.y * 66.0, 360.0);
  float k = (uTintHue >= 0.0 ? 0.5 : 0.16 + 0.28 * tilt)
          * (0.25 + 0.75 * baseSat)
          * (0.5 + 0.5 * abs(n.x - 0.5) * 2.0);
  float dh = mod(targetHue - hue + 540.0, 360.0) - 180.0;
  hue = mod(hue + dh * k + 360.0, 360.0);

  float sweep = 0.5 + uTilt.x * 0.5 + (uPulse - 0.5) * 0.24;
  float band = max(0.0, 1.0 - abs(n.x * 0.6 + n.y * 0.4 - sweep) * 4.0);
  float lum = clamp(baseLum + band * 0.16 + k * 0.07, 0.12, 0.9);
  float sat = clamp(baseSat * (0.95 + 0.3 * k), 0.08, 1.0);

  vec3 glyph = hsv2rgb(vec3(hue / 360.0, sat, lum));

  float holo = clamp(tilt * 1.4, 0.0, 1.0) * 0.34;
  vec3 spectrum = 0.5 + 0.5 * cos(6.28318 * (vec3(0.0, 0.33, 0.67) + n.x * 0.6 + n.y * 0.4 + uPulse * 0.25));
  glyph += spectrum * holo * mask;

  // Premultiplied alpha so the transparent canvas composites cleanly over the page ground.
  float cov = mask * a;
  gl_FragColor = vec4(clamp(glyph, 0.0, 1.0) * cov, cov);
}
`

let io: IntersectionObserver | null = null
let ro: ResizeObserver | null = null
let resizeTimer: ReturnType<typeof setTimeout> | null = null

async function loadBitmap(src: string) {
  const res = await fetch(src)
  if (!res.ok) throw new Error(`portrait asset ${src} -> ${res.status}`)
  const blob = await res.blob()
  return createImageBitmap(blob, { imageOrientation: 'flipY' })
}

onMounted(async () => {
  reducedMotion.value = window.matchMedia(
    '(prefers-reduced-motion: reduce)',
  ).matches
  if (!canvasEl.value) return

  try {
    three = await import('three')
  } catch {
    fail()
    return
  }

  three.ColorManagement.enabled = false

  try {
    renderer = new three.WebGLRenderer({
      canvas: canvasEl.value,
      antialias: false,
      alpha: true,
      powerPreference: 'low-power',
    })
  } catch {
    fail()
    return
  }
  renderer.outputColorSpace = three.LinearSRGBColorSpace

  try {
    ;[colorImg, densityImg] = await Promise.all([
      loadBitmap(props.src),
      loadBitmap(props.densitySrc),
    ])
  } catch {
    fail()
    return
  }

  if (document.fonts?.ready) await document.fonts.ready

  colorTex = new three.Texture(colorImg)
  colorTex.needsUpdate = true
  colorTex.minFilter = three.LinearFilter
  colorTex.magFilter = three.LinearFilter
  colorTex.wrapS = three.ClampToEdgeWrapping
  colorTex.wrapT = three.ClampToEdgeWrapping

  densityTex = new three.Texture(densityImg)
  densityTex.needsUpdate = true
  densityTex.minFilter = three.LinearFilter
  densityTex.magFilter = three.LinearFilter
  densityTex.wrapS = three.ClampToEdgeWrapping
  densityTex.wrapT = three.ClampToEdgeWrapping

  bayerTex = makeBayer(8)
  atlasTex = buildAtlas(8, 8)

  scene = new three.Scene()
  camera = new three.Camera()
  geometry = new three.PlaneGeometry(2, 2)

  const uniforms: Record<string, ThreeNS.IUniform> = {
    uGrid: { value: new three.Vector2(1, 1) },
    uRect: { value: new three.Vector4(0, 0, 1, 1) },
    uMin: { value: 0 },
    uRange: { value: 1 },
    uTilt: { value: new three.Vector2(0, 0) },
    uPhase: { value: 0 },
    uPulse: { value: 0.5 },
    uTintHue: { value: -1 },
    uLight: { value: 0 },
    uColorTex: { value: colorTex },
    uDensityTex: { value: densityTex },
    uAtlasTex: { value: atlasTex },
    uBayerTex: { value: bayerTex },
  }

  material = new three.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms,
    depthTest: false,
    depthWrite: false,
  })

  const mesh = new three.Mesh(geometry, material)
  mesh.frustumCulled = false
  scene.add(mesh)

  analysis = document.createElement('canvas')
  analysisCtx = analysis.getContext('2d', { willReadFrequently: true })

  canvasEl.value.addEventListener('webglcontextlost', onContextLost)

  buildLayout()

  if (reducedMotion.value) {
    applyUniforms()
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
      buildLayout()
      if (reducedMotion.value) {
        draw()
      }
    }, 140)
  })
  if (wrapEl.value) ro.observe(wrapEl.value)
})

onBeforeUnmount(() => {
  disposed = true
  stop()
  canvasEl.value?.removeEventListener('webglcontextlost', onContextLost)
  io?.disconnect()
  ro?.disconnect()
  if (resizeTimer) clearTimeout(resizeTimer)
  atlasTex?.dispose()
  bayerTex?.dispose()
  colorTex?.dispose()
  densityTex?.dispose()
  geometry?.dispose()
  material?.dispose()
  renderer?.dispose()
})

watch(
  () => [props.activeHue, props.theme],
  () => {
    if (!material || !three) return
    applyUniforms()
    if (reducedMotion.value || running) draw()
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
    <canvas
      ref="canvasEl"
      class="ascii-portrait__canvas"
      role="img"
      :aria-label="label"
    />
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
  width: 100%;
  height: 100%;
}
</style>
