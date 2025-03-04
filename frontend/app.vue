<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <h1 class="text-3xl font-bold tracking-tight text-gray-900">Интерактивная платформа по истории</h1>
          <nav>
            <ul class="flex space-x-6">
              <li>
                <NuxtLink to="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path === '/' }">
                  Главная
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/graph" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path === '/graph' }">
                  Граф событий
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/events" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path.startsWith('/events') }">
                  Библиотека событий
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/learning" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path === '/learning' }">
                  Обучение
                </NuxtLink>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
    <main>
      <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <NuxtPage />
      </div>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html {
  font-family: 'Inter', sans-serif;
}

body {
  @apply antialiased text-gray-900;
}
</style> 