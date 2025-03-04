<template>
  <div class="space-y-6">
    <Card title="Интерактивная образовательная платформа по истории">
      <p class="text-gray-700 mb-4">Добро пожаловать в образовательную платформу, где вы можете изучать исторические события и их взаимосвязи.</p>
      <p class="text-gray-700 font-medium mb-2">Платформа предлагает следующие возможности:</p>
      <ul class="list-disc list-inside text-gray-700 space-y-1 ml-4 mb-6">
        <li>Интерактивные графы событий с причинно-следственными связями</li>
        <li>Категоризация событий по типам с цветовой кодировкой</li>
        <li>Детальная информация о каждом историческом событии</li>
        <li>Режимы "Лекция" и "Презентация" для обучения</li>
        <li>Библиотечный (списковый) режим для удобного просмотра</li>
      </ul>
      
      <template #footer>
        <div class="flex justify-end space-x-4">
          <Button variant="primary" @click="navigateTo('/graph')">
            Интерактивный граф
          </Button>
          <Button variant="secondary" @click="navigateTo('/events')">
            Библиотека событий
          </Button>
        </div>
      </template>
    </Card>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card 
        title="Интерактивный граф" 
        subtitle="Визуализация исторических событий"
        hoverable
        @click="navigateTo('/graph')"
      >
        <p class="text-gray-700">
          Исследуйте исторические события в интерактивном графе, который показывает причинно-следственные связи между ними.
        </p>
      </Card>
      
      <Card 
        title="Библиотека событий" 
        subtitle="Систематизированный каталог"
        hoverable
        @click="navigateTo('/events')"
      >
        <p class="text-gray-700">
          Просматривайте события в удобном списковом режиме с возможностью сортировки и фильтрации.
        </p>
      </Card>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Главная - Интерактивная образовательная платформа по истории'
})
</script>

<style scoped>
.headline {
  text-align: center;
}
</style> 