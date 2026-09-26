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

const glOk = ref(false)

if (import.meta.client) {
  try {
    const probe = document.createElement('canvas')
    glOk.value = !!probe.getContext('webgl2')
  } catch {
    glOk.value = false
  }
}
</script>

<template>
  <ClientOnly>
    <AsciiPortraitGL
      v-if="glOk"
      :src="props.src"
      :density-src="props.densitySrc"
      :label="props.label"
      :theme="props.theme"
      :active-hue="props.activeHue"
      @fail="glOk = false"
    />
    <AsciiPortraitCanvas
      v-else
      :src="props.src"
      :density-src="props.densitySrc"
      :label="props.label"
      :theme="props.theme"
      :active-hue="props.activeHue"
    />
    <template #fallback>
      <div class="ascii-portrait-fallback" aria-hidden="true" />
    </template>
  </ClientOnly>
</template>

<style scoped>
.ascii-portrait-fallback {
  width: 100%;
  aspect-ratio: 1;
}
</style>