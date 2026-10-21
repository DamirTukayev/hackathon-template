import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': '/src' } },
  server: {
    port: 5173,
    // /api/* -> FastAPI. Без CORS-головной боли и с работающим SSE.
    proxy: { '/api': 'http://localhost:8000' },
  },
})
