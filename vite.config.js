import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: '.',
  server: {
    allowedHosts: ['.prt.dev', '.localhost'],
  },
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
        useCases: resolve(__dirname, 'use-cases/index.html'),
        useCasesMultiRepo: resolve(__dirname, 'use-cases/multi-repo/index.html'),
        useCasesIntegrations: resolve(__dirname, 'use-cases/integrations-urls/index.html'),
        useCasesPlatform: resolve(__dirname, 'use-cases/platform-pr/index.html'),
        useCasesAgents: resolve(__dirname, 'use-cases/agents-automation/index.html'),
        useCasesLocalServices: resolve(__dirname, 'use-cases/local-services/index.html'),
        useCasesDatabase: resolve(__dirname, 'use-cases/database-per-branch/index.html'),
        useCasesOnboarding: resolve(__dirname, 'use-cases/onboarding/index.html'),
        useCasesFirstTimeSetup: resolve(__dirname, 'use-cases/first-time-setup/index.html'),
        useCasesOauthAlias: resolve(__dirname, 'use-cases/oauth-alias/index.html'),
      },
    },
  },
})
