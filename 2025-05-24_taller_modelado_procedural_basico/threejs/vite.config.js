import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  root: './',          // carpeta actual
  base: './',          // para rutas relativas al build
  build: { outDir: 'dist' }
})
