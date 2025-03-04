<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <h1 class="text-3xl font-bold tracking-tight text-gray-900 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span>(Ис-Кис)</span>
          </h1>
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