import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { loadEnv } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  // const env = loadEnv(mode, process.cwd())
  plugins: [
    vue(),
    // url({
    //   include: ['**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.gif'],
    //   limit: 8192, // 根据需要调整大小限制
    // }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0'
  },

})
