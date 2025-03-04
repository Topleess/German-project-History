<template>
  <div>
    <Card>
      <template #title>
        <h1 class="text-2xl font-bold">Обучение</h1>
      </template>
      
      <div class="flex justify-center items-center h-96">
        <div class="text-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <h2 class="mt-4 text-xl font-semibold text-gray-700">Раздел в разработке</h2>
          <p class="mt-2 text-gray-600">Образовательный раздел скоро будет доступен. Следите за обновлениями!</p>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Обучение - История'
})
</script> 