export default {
  // Глобальная настройка страницы
  head: {
    title: 'Интерактивная платформа по истории',
    htmlAttrs: {
      lang: 'ru'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Интерактивная образовательная платформа для изучения ключевых исторических событий' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Глобальные CSS файлы
  css: [
  ],

  // Плагины для запуска перед монтированием приложения
  plugins: [
    { src: '~/plugins/d3.js', mode: 'client' }
  ],

  // Компоненты автоматически импортируются
  components: true,

  // Модули для разработки
  buildModules: [
    '@nuxtjs/eslint-module',
    '@nuxtjs/vuetify'
  ],

  // Модули
  modules: [
    '@nuxtjs/axios'
  ],

  // Конфигурация Axios
  axios: {
    baseURL: 'http://localhost:8000' // URL бэкенда
  },

  // Конфигурация Vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        light: {
          primary: '#3f51b5',
          secondary: '#b0bec5',
          accent: '#8c9eff',
          error: '#b71c1c'
        }
      }
    }
  },

  // Настройки сборки
  build: {
    babel: {
      presets: [
        ['@babel/preset-env', {
          useBuiltIns: 'usage',
          corejs: 3,
          targets: { 
            browsers: ['> 1%', 'last 2 versions', 'not dead'],
            node: 'current'
          }
        }]
      ],
      plugins: [
        '@babel/plugin-proposal-optional-chaining',
        '@babel/plugin-proposal-nullish-coalescing-operator',
        '@babel/plugin-transform-runtime'
      ]
    }
  },

  // Настройки сервера для разработки
  server: {
    host: '0.0.0.0',
    port: 3000
  }
} 