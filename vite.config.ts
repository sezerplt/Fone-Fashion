import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const cssFileName="index.min.css"
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(),],
  publicDir:"./public",
  build: {
    chunkSizeWarningLimit: 500000,
    rollupOptions:{
      output:{
        assetFileNames:(file)=>{
          return `assets/css/${cssFileName}`
        },
        entryFileNames:(file)=>{
          return `assets/js/[name].min.js`
        }
      }
    }
},
})
