// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/eslint', '@nuxt/fonts', '@nuxt/icon'],

  css: ['~/assets/css/main.css'],

  fonts: {
    families: [
      {
        name: 'Aleo',
        provider: 'google',
        weights: ['100 900'],
        styles: ['normal', 'italic'],
        subsets: ['menu', 'latin', 'latin-ext', 'vietnamese'],
      },
      {
        name: 'IBM Plex Mono',
        provider: 'google',
        weights: ['100', '200', '300', '400', '500', '600', '700'],
        styles: ['normal', 'italic'],
        subsets: ['menu', 'cyrillic', 'cyrillic-ext', 'latin', 'latin-ext', 'vietnamese'],
      },
    ],
  },

  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      title: 'Paul Melero — human | engineer',
      meta: [
        {
          name: 'description',
          content:
            'Paul Melero builds things, sometimes with code. Personal landing card, twenty years on the web.',
        },
        { name: 'theme-color', content: '#0a0c0b', media: '(prefers-color-scheme: dark)' },
        { name: 'theme-color', content: '#f2efe6', media: '(prefers-color-scheme: light)' },
        { property: 'og:title', content: 'Paul Melero — human | engineer' },
        {
          property: 'og:description',
          content: 'Personal landing card. human | engineer. Twenty years on the web.',
        },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: 'https://paulmelero.com/' },
        { name: 'twitter:card', content: 'summary_large_image' },
      ],
      link: [{ rel: 'canonical', href: 'https://paulmelero.com/' }],
      script: [
        {
          // Set the theme before first paint to avoid a flash. Mirrors useTheme().
          innerHTML:
            "(function(){try{var t=localStorage.getItem('pm-theme');if(t!=='light'&&t!=='dark'){t=window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'}document.documentElement.dataset.theme=t}catch(e){document.documentElement.dataset.theme='dark'}})()",
          tagPosition: 'head',
        },
      ],
    },
  },
})