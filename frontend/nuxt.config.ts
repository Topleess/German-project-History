// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Включаем DevTools для разработки
  devtools: { enabled: true },

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

  // Настройки для разработки
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  compatibilityDate: '2025-03-03'
})