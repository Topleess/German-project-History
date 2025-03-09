// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Включаем DevTools для разработки
  devtools: { enabled: process.env.NODE_ENV === 'development' },

  // Модули
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // Глобальный метатеги
  app: {
    head: {
      title: 'Интерактивная платформа по истории',
      htmlAttrs: {
        lang: 'ru'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Интерактивная образовательная платформа для изучения ключевых исторических событий' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },

  // Конфигурация сборки
  build: {
    transpile: ['d3']
  },

  // Настройки для разработки и продакшена
  runtimeConfig: {
    public: {
      // В продакшене API будет доступен по относительному пути /api
      apiBase: process.env.NODE_ENV === 'production' 
        ? '/api' 
        : (process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000')
    }
  },

  // Конфигурация для SSR
  ssr: true,

  // Настройка прокси для разработки
  nitro: {
    devProxy: {
      '/api': {
        target: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
        pathRewrite: { '^/api': '' }
      }
    }
  },

  compatibilityDate: '2025-03-03'
})