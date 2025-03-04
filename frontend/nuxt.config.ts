// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Режим сборки приложения
  ssr: false, // Отключаем SSR для решения проблем с загрузкой

  // Включаем DevTools для разработки
  devtools: { enabled: true },

  // Директории с модулями
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // Настройки для dev-сервера
  devServer: {
    port: 3000
  },

  // Глобальные переменные
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  // Директория сборки
  buildDir: '.nuxt',

  // Конфигурация сборки
  build: {
    transpile: ['d3']
  },

  vite: {
    optimizeDeps: {
      include: ['d3']
    }
  },

  app: {
    head: {
      title: 'История Германии',
      htmlAttrs: {
        lang: 'ru'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Платформа для изучения исторических событий Германии' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },

  compatibilityDate: '2025-03-03'
})