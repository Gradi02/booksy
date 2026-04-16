/**
 * Vitest Configuration for Booksy Frontend
 * 
 * IMPORTANT: Requires Node.js 16.11.0 or higher
 * Current version: v14.21.3 (TOO OLD)
 * 
 * To upgrade Node.js:
 * 1. Visit https://nodejs.org/ and download LTS version
 * 2. Or use nvm: nvm install 18
 * 3. Then re-run: npm install && npm run test
 */

import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
