import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://git-treeline.dev',
  server: {
    host: true,
    allowedHosts: ['.prt.dev', '.localhost'],
  },
  build: {
    format: 'directory',
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
