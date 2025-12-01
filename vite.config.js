import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // use '/too-doo-list/' only when building for GitHub Pages
  base: mode === 'github' ? '/too-doo-list/' : '/',
}))