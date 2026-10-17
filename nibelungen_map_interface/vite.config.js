import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { BootstrapVueNextResolver } from 'bootstrap-vue-next/resolvers'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [
      vue(),
      // Auto-imports the bootstrap-vue-next components (<BRow>, <BFormSelect>...) used in templates
      Components({ resolvers: [BootstrapVueNextResolver()], dts: false })
    ],
    base: env.VITE_SITE_URL || '/',
    build: {
      outDir: 'nibelungen-map-dist'
    }
  }
})
