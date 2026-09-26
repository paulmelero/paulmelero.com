<script setup lang="ts">
useHead({
  title: 'Paul Melero — human | engineer',
  meta: [
    {
      name: 'description',
      content:
        'Paul Melero builds things, sometimes with code. Engineer, creative thinker. Personal landing card.',
    },
  ],
})

const { theme, toggle } = useTheme()
const menuOpen = ref(false)
const copied = ref(false)
const activeHue = ref<number | null>(null)

const links = [
  {
    name: 'graficos.net',
    href: 'https://graficos.net/',
    note: 'personal site & blog — the long version',
  },
  {
    name: 'Flipthecoin.app',
    href: 'https://flipthecoin.app/',
    note: '3D coin flip simulator with a real physics engine — where I blog about interesting math/statistics topics.',
  },
]

const spectra = [
  { name: 'magenta', hue: 330 },
  { name: 'amber', hue: 38 },
  { name: 'phosphor', hue: 140 },
  { name: 'cyan', hue: 195 },
  { name: 'violet', hue: 275 },
]

const socials = [
  {
    name: 'Bluesky',
    href: 'https://bsky.app/profile/paulmelero.com',
    d: 'M5.202 2.857C7.954 4.922 10.913 9.11 12 11.358c1.087-2.247 4.046-6.436 6.798-8.501C20.783 1.366 24 .213 24 3.883c0 .732-.42 6.156-.667 7.037-.856 3.061-3.978 3.842-6.755 3.37 4.854.826 6.089 3.562 3.422 6.299-5.065 5.196-7.28-1.304-7.847-2.97-.104-.305-.152-.448-.153-.327 0-.121-.05.022-.153.327-.568 1.666-2.782 8.166-7.847 2.97-2.667-2.737-1.432-5.473 3.422-6.3-2.777.473-5.899-.308-6.755-3.369C.42 10.04 0 4.615 0 3.883c0-3.67 3.217-2.517 5.202-1.026',
  },
  {
    name: 'GitHub',
    href: 'https://github.com/paulmelero/',
    d: 'M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12',
  },
  {
    name: 'LinkedIn',
    href: 'https://www.linkedin.com/in/paulmelero/',
    d: 'M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003',
  },
]

function setHue(hue: number | null) {
  activeHue.value = hue
}

async function copyEmail() {
  const email = 'contact@paulmelero.com'
  try {
    await navigator.clipboard.writeText(email)
  } catch {
    const area = document.createElement('textarea')
    area.value = email
    area.setAttribute('readonly', '')
    area.style.position = 'absolute'
    area.style.left = '-9999px'
    document.body.appendChild(area)
    area.select()
    document.execCommand('copy')
    document.body.removeChild(area)
  }
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') menuOpen.value = false
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div class="page">
    <a class="skip" href="#main">skip to content</a>

    <header class="site-head">
      <div class="u-container site-head__inner">
        <a class="brand" href="#top" aria-label="Paul Melero — back to top">
          <svg class="brand__mark" viewBox="0 0 4 4" aria-hidden="true">
            <rect x="0" y="0" width="1.6" height="1.6" fill="currentColor" />
            <rect
              x="2.4"
              y="0"
              width="1.6"
              height="1.6"
              fill="currentColor"
              opacity="0.35"
            />
            <rect
              x="0"
              y="2.4"
              width="1.6"
              height="1.6"
              fill="currentColor"
              opacity="0.65"
            />
            <rect
              x="2.4"
              y="2.4"
              width="1.6"
              height="1.6"
              fill="currentColor"
              opacity="0.2"
            />
          </svg>
          <span class="brand__name">paulmelero.com</span>
        </a>

        <nav class="site-nav site-nav--lean-right" aria-label="Primary">
          <a href="#work">work</a>
          <a href="#contact">contact</a>
        </nav>

        <div class="site-head__actions">
          <button
            class="icon-btn"
            type="button"
            :aria-label="
              theme === 'dark'
                ? 'Switch to light theme'
                : 'Switch to dark theme'
            "
            @click="toggle"
          >
            <svg v-if="theme === 'dark'" viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="12" cy="12" r="4" />
              <path
                d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"
              />
            </svg>
            <svg v-else viewBox="0 0 24 24" aria-hidden="true">
              <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" />
            </svg>
          </button>

          <button
            class="icon-btn menu-btn"
            type="button"
            aria-controls="mobile-menu"
            :aria-expanded="menuOpen"
            aria-label="Menu"
            @click="menuOpen = !menuOpen"
          >
            <svg v-if="!menuOpen" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M3 6h18M3 12h18M3 18h18" />
            </svg>
            <svg v-else viewBox="0 0 24 24" aria-hidden="true">
              <path d="M5 5l14 14M19 5L5 19" />
            </svg>
          </button>
        </div>
      </div>

      <nav
        v-if="menuOpen"
        id="mobile-menu"
        class="mobile-menu"
        aria-label="Primary"
      >
        <div class="u-container mobile-menu__inner">
          <a href="#work" @click="menuOpen = false">work</a>
          <a href="#contact" @click="menuOpen = false">contact</a>
        </div>
      </nav>
    </header>

    <main id="main">
      <section id="top" class="hero">
        <div class="u-container hero__inner">
          <div class="plot u-corners">
            <div class="plot__bar u-mono" aria-hidden="true">
              <span>fig. 01 — subject</span>
              <span>plot · 512 × 512</span>
            </div>

            <div class="plot__field">
              <div class="plot__dimension u-mono" aria-hidden="true">
                <span class="plot__dim-line" />
                <span class="plot__dim-label">512 px</span>
                <span class="plot__dim-line" />
              </div>

              <div class="plot__figure">
                <AsciiPortrait :theme="theme" :active-hue="activeHue" />
              </div>

              <div class="plot__legend">
                <span class="u-mono plot__legend-title">legend</span>
                <ul class="swatches">
                  <li v-for="s in spectra" :key="s.name">
                    <button
                      class="swatch"
                      type="button"
                      :style="{ '--swatch': `hsl(${s.hue} 90% 55%)` }"
                      :aria-label="`Tint the portrait ${s.name}`"
                      :aria-pressed="activeHue === s.hue"
                      @click="setHue(activeHue === s.hue ? null : s.hue)"
                    />
                  </li>
                </ul>
                <span class="plot__legend-hint u-mono" aria-hidden="true"
                  >select to tint</span
                >
              </div>
            </div>

            <div class="plot__caption">
              <h1 class="identity">Paul Melero</h1>
              <p class="identity__line u-mono">human | engineer</p>
            </div>
          </div>

          <p class="hero__lead">
            I build things, sometimes with code. Twenty years on the web.
            Engineer, creative thinker.
          </p>

          <div class="hero__cta">
            <a
              class="u-cmd u-cmd--solid"
              href="https://graficos.net/"
              target="_blank"
              rel="noopener noreferrer"
            >
              open graficos.net
              <svg class="arrow" viewBox="0 0 16 16" aria-hidden="true">
                <path d="M5 11 11 5M6 5h5v5" />
              </svg>
            </a>
            <a class="u-cmd" href="#contact">say hi</a>
          </div>
        </div>
      </section>

      <section id="work" class="section">
        <div class="u-container">
          <h2 class="section-title u-mono">related links</h2>
          <ul class="link-rows">
            <li v-for="l in links" :key="l.name">
              <a
                class="link-row"
                :href="l.href"
                target="_blank"
                rel="noopener noreferrer"
              >
                <span class="link-row__mark" aria-hidden="true">→</span>
                <span class="link-row__name">{{ l.name }}</span>
                <span class="link-row__note">{{ l.note }}</span>
                <svg
                  class="arrow link-row__arrow"
                  viewBox="0 0 16 16"
                  aria-hidden="true"
                >
                  <path d="M5 11 11 5M6 5h5v5" />
                </svg>
              </a>
            </li>
          </ul>
        </div>
      </section>

      <section id="contact" class="section">
        <div class="u-container">
          <h2 class="section-title u-mono">contact</h2>
          <p class="contact__lead">
            Feel free to reach out by email, or find me on social media.
          </p>
          <div class="contact__mail">
            <a class="contact__email" href="mailto:contact@paulmelero.com"
              >contact@paulmelero.com</a
            >
            <button class="u-cmd" type="button" @click="copyEmail">
              <svg class="arrow" viewBox="0 0 16 16" aria-hidden="true">
                <rect x="5.5" y="5.5" width="8" height="8" rx="1" />
                <path
                  d="M10.5 5.5v-2a1 1 0 0 0-1-1h-7a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h2"
                />
              </svg>
              copy
            </button>
          </div>
          <p class="contact__status u-mono" aria-live="polite">
            {{ copied ? 'copied to clipboard' : '' }}
          </p>
        </div>
      </section>
    </main>

    <footer class="site-foot">
      <div class="u-container">
        <div class="titleblock u-corners">
          <div class="titleblock__cell">
            <span class="titleblock__key u-mono">project</span>
            <span class="titleblock__val">paulmelero.com</span>
          </div>
          <div class="titleblock__cell">
            <span class="titleblock__key u-mono">subject</span>
            <span class="titleblock__val">Paul Melero</span>
          </div>
          <div class="titleblock__cell">
            <span class="titleblock__key u-mono">role</span>
            <span class="titleblock__val">human | engineer</span>
          </div>
          <div class="titleblock__cell">
            <span class="titleblock__key u-mono">unit</span>
            <span class="titleblock__val">PX</span>
          </div>
          <div class="titleblock__cell titleblock__cell--socials">
            <span class="titleblock__key u-mono">elsewhere</span>
            <ul class="socials">
              <li v-for="s in socials" :key="s.name">
                <a
                  :href="s.href"
                  target="_blank"
                  rel="noopener noreferrer"
                  :aria-label="`${s.name} (opens in a new tab)`"
                >
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path :d="s.d" />
                  </svg>
                </a>
              </li>
            </ul>
          </div>
          <div class="titleblock__cell">
            <span class="titleblock__key u-mono">note</span>
            <span class="titleblock__val">© 2026 Paul Melero</span>
          </div>
          <div class="titleblock__cell">
            <span class="titleblock__key u-mono">size</span>
            <span class="footer-size">A1</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  min-height: 100svh;
}

/* ---------- Header ---------- */
.site-head {
  position: sticky;
  top: 0;
  z-index: 20;
  background: var(--bg);
  border-bottom: var(--line-w) solid var(--line);
}
.site-head__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  min-height: 52px;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  text-decoration: none;
  font-size: var(--fs-small);
  letter-spacing: 0.02em;
}
.brand__mark {
  width: 11px;
  height: 11px;
  color: var(--accent);
  flex: none;
}
.brand__name {
  font-weight: 500;
}

.site-nav {
  display: flex;
  gap: var(--sp-5);
  font-size: var(--fs-small);
}
.site-nav a,
.mobile-menu a {
  text-decoration: none;
  color: var(--ink-dim);
  padding: var(--sp-1) 0;
}
.site-nav a:hover,
.mobile-menu a:hover {
  color: var(--accent);
}

.site-nav--lean-right {
  margin: 0 0 0 auto;
}

.site-head__actions {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
}
.icon-btn {
  display: inline-grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border: var(--line-w) solid transparent;
  background: transparent;
  color: var(--ink-dim);
  cursor: pointer;
  transition:
    color 0.18s ease,
    border-color 0.18s ease;
}
.icon-btn:hover {
  color: var(--accent);
  border-color: var(--line);
}
.icon-btn svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: square;
  stroke-linejoin: miter;
}
.menu-btn {
  display: none;
}

.mobile-menu {
  border-top: var(--line-w) solid var(--line);
  background: var(--bg-2);
}
.mobile-menu__inner {
  display: flex;
  flex-direction: column;
  padding-block: var(--sp-2);
}
.mobile-menu a {
  padding-block: var(--sp-3);
  font-size: var(--fs-body);
}

.skip {
  position: absolute;
  left: var(--sp-4);
  top: -100px;
  z-index: 50;
  padding: var(--sp-2) var(--sp-3);
  background: var(--accent);
  color: var(--accent-ink);
  font-size: var(--fs-label);
  text-decoration: none;
}
.skip:focus {
  top: var(--sp-2);
}

/* ---------- Hero / plot sheet ---------- */
.hero {
  flex: 1;
  display: flex;
  align-items: center;
  padding-block: clamp(2rem, 6vh, 5rem);
  scroll-margin-top: 60px;
}
.hero__inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-6);
}

.plot {
  width: 100%;
  border: var(--line-w) solid var(--line-strong);
  background: var(--bg-2);
}
.plot__bar {
  display: flex;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-2) var(--sp-3);
  border-bottom: var(--line-w) solid var(--line);
  color: var(--ink-faint);
  font-size: var(--fs-deco);
}
.plot__field {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  gap: var(--sp-4);
  padding: clamp(1rem, 3vw, 2.5rem);
}
.plot__figure {
  width: clamp(220px, 46vh, 560px);
  max-width: 100%;
  min-width: 0;
}

.plot__dimension {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  align-self: stretch;
  color: var(--ink-faint);
  font-size: var(--fs-deco);
}
.plot__dim-line {
  flex: 1;
  width: var(--line-w);
  background: var(--line);
}
.plot__dim-label {
  writing-mode: vertical-rl;
  letter-spacing: 0.14em;
  white-space: nowrap;
}

.plot__legend {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--sp-3);
}
.plot__legend-title {
  color: var(--ink-faint);
  font-size: var(--fs-deco);
}
.swatches {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}
.swatch {
  width: 22px;
  height: 12px;
  padding: 0;
  border: var(--line-w) solid var(--line-strong);
  background: var(--swatch);
  cursor: pointer;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease;
}
.swatch:hover,
.swatch:focus-visible,
.swatch[aria-pressed='true'] {
  border-color: var(--ink);
  transform: translateX(-4px);
}
.plot__legend-hint {
  color: var(--ink-faint);
  font-size: var(--fs-deco);
  text-align: right;
}

.plot__caption {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-5) var(--sp-4) var(--sp-6);
  border-top: var(--line-w) solid var(--line);
  text-align: center;
}
.identity {
  font-family: var(--brand-font);
  font-size: var(--fs-display);
  font-weight: 500;
  line-height: 0.98;
  letter-spacing: -0.03em;
}
.identity__line {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  color: var(--accent);
  font-size: var(--fs-label);
}

.hero__lead {
  max-width: var(--measure);
  text-align: center;
  color: var(--ink-dim);
  font-size: var(--fs-lead);
  line-height: 1.5;
}
.hero__cta {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--sp-3);
}
.u-cmd .arrow,
.arrow {
  width: 14px;
  height: 14px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: square;
}

/* ---------- Sections ---------- */
.section {
  padding-block: clamp(2.5rem, 7vh, 4.5rem);
  scroll-margin-top: 60px;
}
.section + .section {
  border-top: var(--line-w) solid var(--line);
}
.section-title {
  position: relative;
  margin-bottom: var(--sp-6);
  padding-bottom: var(--sp-3);
  color: var(--ink);
  font-size: var(--fs-label);
  font-weight: 500;
}
.section-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: var(--line-w);
  background: var(--line);
}

.link-rows {
  display: flex;
  flex-direction: column;
}
.link-row {
  display: grid;
  grid-template-columns: auto minmax(8rem, 14rem) 1fr auto;
  align-items: baseline;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-3);
  border-top: var(--line-w) solid var(--line);
  text-decoration: none;
  transition:
    background-color 0.18s ease,
    color 0.18s ease;
}
.link-rows li:last-child .link-row {
  border-bottom: var(--line-w) solid var(--line);
}
.link-row:hover {
  background: var(--bg-2);
}
.link-row__mark {
  color: var(--ink-faint);
  font-family: var(--mono);
  font-size: var(--fs-lead);
}
.link-row__name {
  color: var(--ink);
  font-size: var(--fs-lead);
  font-family: var(--brand-font);
  font-weight: 500;
  letter-spacing: -0.01em;
}
.link-row:hover .link-row__name {
  color: var(--accent);
}
.link-row__note {
  color: var(--ink-dim);
  font-size: var(--fs-small);
}
.link-row__arrow {
  color: var(--ink-faint);
  align-self: center;
}
.link-row:hover .link-row__arrow {
  color: var(--accent);
}

/* ---------- Contact ---------- */
.contact__lead {
  max-width: var(--measure);
  color: var(--ink-dim);
  font-size: var(--fs-lead);
  margin-bottom: var(--sp-5);
}
.contact__mail {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--sp-4);
}
.contact__email {
  font-family: var(--brand-font);
  font-size: clamp(1.25rem, 0.9rem + 1.6vw, 2rem);
  font-weight: 500;
  letter-spacing: -0.02em;
}
.contact__email:hover {
  color: var(--accent);
}
.contact__status {
  min-height: 1.6em;
  margin-top: var(--sp-3);
  color: var(--accent);
  font-size: var(--fs-deco);
}

/* ---------- Footer / title block ---------- */
.site-foot {
  padding-block: var(--sp-7) var(--sp-6);
  border-top: var(--line-w) solid var(--line);
}
.titleblock {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: var(--line-w) solid var(--line-strong);
}
.titleblock__cell {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--sp-1);
  padding: var(--sp-3) var(--sp-4);
  border-right: var(--line-w) solid var(--line);
  border-bottom: var(--line-w) solid var(--line);
  min-width: 0;
}
.titleblock__cell:nth-child(4n) {
  border-right: 0;
}
.titleblock__cell--socials {
  grid-column: span 2;
}
.titleblock__key {
  color: var(--ink-faint);
  font-size: var(--fs-deco);
}
.titleblock__val {
  font-size: var(--fs-small);
}
.socials {
  display: flex;
  gap: var(--sp-3);
  margin-top: var(--sp-1);
}
.socials a {
  display: inline-grid;
  place-items: center;
  width: 28px;
  height: 28px;
  color: var(--ink-dim);
  border: var(--line-w) solid var(--line);
  transition:
    color 0.18s ease,
    border-color 0.18s ease;
}
.socials a:hover {
  color: var(--accent);
  border-color: var(--accent);
}
.socials svg {
  width: 15px;
  height: 15px;
  fill: currentColor;
}

.footer-size {
  font-family: var(--brand-font);
  font-size: clamp(1.25rem, 0.9rem + 1.6vw, 2rem);
  font-weight: 500;
  text-box-trim: trim-both;
}

/* ---------- Responsive ---------- */
@media (max-width: 860px) {
  .plot__field {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--sp-5);
    justify-items: center;
  }
  .plot__dimension {
    display: none;
  }
  .plot__legend {
    align-items: center;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--sp-4);
  }
  .swatches {
    flex-direction: row;
    gap: var(--sp-2);
  }
  .plot__legend-hint {
    display: none;
  }
  .swatch:hover,
  .swatch:focus-visible,
  .swatch[aria-pressed='true'] {
    transform: translateY(-4px);
  }
}

@media (max-width: 720px) {
  .site-nav {
    display: none;
  }
  .menu-btn {
    display: inline-grid;
  }
  .titleblock {
    grid-template-columns: 1fr 1fr;
  }
  .titleblock__cell:nth-child(4n) {
    border-right: var(--line-w) solid var(--line);
  }
  .titleblock__cell:nth-child(2n):not(:nth-last-child(2)) {
    border-right: 0;
  }
  .titleblock__cell--socials {
    grid-column: span 2;
  }
}

@media (max-width: 520px) {
  .link-row {
    grid-template-columns: auto 1fr auto;
    row-gap: var(--sp-1);
  }
  .link-row__note {
    grid-column: 2 / 3;
  }
}

@media (prefers-reduced-motion: reduce) {
  .link-row,
  .icon-btn,
  .swatch {
    transition: none;
  }
}
</style>
