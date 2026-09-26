type Theme = 'dark' | 'light'

const STORAGE_KEY = 'pm-theme'

export function useTheme() {
  const theme = useState<Theme>('theme', () => 'dark')

  function apply(next: Theme) {
    theme.value = next
    if (import.meta.client) {
      document.documentElement.dataset.theme = next
    }
  }

  function toggle() {
    apply(theme.value === 'dark' ? 'light' : 'dark')
    try {
      localStorage.setItem(STORAGE_KEY, theme.value)
    } catch {
      /* storage unavailable — session-only theme */
    }
  }

  onMounted(() => {
    const current = document.documentElement.dataset.theme
    if (current === 'light' || current === 'dark') theme.value = current
  })

  return { theme, toggle, apply }
}