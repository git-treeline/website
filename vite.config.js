import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: '.',
  build: {
    outDir: 'dist',
    emptyDirOnBuild: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        docs: resolve(__dirname, 'docs/index.html'),
        networkingRedirect: resolve(__dirname, 'networking/index.html'),
        featIsolation: resolve(__dirname, 'features/isolation/index.html'),
        featNetworking: resolve(__dirname, 'features/networking/index.html'),
        featWorkflows: resolve(__dirname, 'features/workflows/index.html'),
        featAgents: resolve(__dirname, 'features/agents/index.html'),
      },
    },
  },
})
