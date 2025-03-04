<template>
  <div class="space-y-8">
    <!-- Верхняя секция с описанием и интерактивной картой -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card title="Интерактивная образовательная платформа по истории">
        <p class="text-gray-700 mb-4">Добро пожаловать в образовательную платформу, где вы можете изучать исторические события и их взаимосвязи.</p>
        <div class="flex flex-col mb-4">
          <div class="flex items-center mb-2">
            <div class="w-16 font-medium text-gray-700">События:</div>
            <div class="text-lg font-bold text-primary-600">{{ totalEvents }}</div>
          </div>
          <div class="flex items-center mb-2">
            <div class="w-16 font-medium text-gray-700">Период:</div>
            <div class="text-lg font-bold text-primary-600">{{ earliestYear }} - {{ latestYear }}</div>
          </div>
          <div class="flex items-center">
            <div class="w-16 font-medium text-gray-700">Страны:</div>
            <div class="text-lg font-bold text-primary-600">{{ totalCountries }}</div>
          </div>
        </div>
        
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
      
      <Card title="Интерактивная карта событий" class="h-full">
        <div class="h-64 md:h-72 lg:h-80">
          <WorldMap 
            :country-data="countryEventData" 
            @country-selected="handleCountrySelected" 
          />
        </div>
        <div v-if="selectedCountry" class="mt-4 p-3 bg-gray-50 rounded-md">
          <h3 class="font-medium text-gray-900">{{ selectedCountry.name }}</h3>
          <div class="mt-1 text-sm text-gray-600">Событий: {{ selectedCountry.eventsCount }}</div>
          <div class="mt-2 flex flex-wrap gap-2">
            <span v-for="(category, idx) in selectedCountry.categories" :key="idx" 
                  class="px-2 py-1 text-xs rounded-full" 
                  :style="{ backgroundColor: getCategoryColor(category.id), color: 'white' }">
              {{ category.name }}: {{ category.count }}
            </span>
          </div>
        </div>
      </Card>
    </div>

    <!-- Карусель с историческими событиями -->
    <Card title="Значимые события в истории">
      <EventCarousel :events="featuredEvents" :autoplay="true" :interval="5000" />
    </Card>

    <!-- Графики данных -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card title="Рост исторических событий по годам">
        <div class="h-64">
          <YearlyGrowthChart :data="yearlyGrowthData" />
        </div>
      </Card>
      
      <Card title="Распределение событий по категориям">
        <div class="h-64">
          <CategoryBubbleChart 
            :data="categoryData" 
            @category-selected="handleCategorySelected" 
          />
        </div>
      </Card>
    </div>
    
    <!-- Навигационные карточки -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
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
      
      <Card 
        title="Обучение" 
        subtitle="Образовательные материалы"
        hoverable
        @click="navigateTo('/learning')"
      >
        <p class="text-gray-700">
          Изучайте историю через структурированные образовательные модули и интерактивные презентации.
        </p>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import WorldMap from '~/components/WorldMap.vue';
import EventCarousel from '~/components/EventCarousel.vue';
import YearlyGrowthChart from '~/components/YearlyGrowthChart.vue';
import CategoryBubbleChart from '~/components/CategoryBubbleChart.vue';

definePageMeta({
  title: 'Главная - Интерактивная образовательная платформа по истории'
})

// Composables и API
const { getAllEvents, getCountries, getCategoryCounts, getYearlyGrowth } = useApi();

// Состояния данных
const events = ref([]);
const selectedCountry = ref(null);

// Статистика
const totalEvents = ref(0);
const earliestYear = ref('');
const latestYear = ref('');
const totalCountries = ref(0);

// Данные для карты
const countryEventData = ref({
  "RUS": { eventsCount: 120, categories: [{id: 1, name: "Политические", count: 50}, {id: 2, name: "Военные", count: 30}] },
  "USA": { eventsCount: 85, categories: [{id: 1, name: "Политические", count: 40}, {id: 3, name: "Экономические", count: 25}] },
  "FRA": { eventsCount: 65, categories: [{id: 4, name: "Культурные", count: 30}, {id: 1, name: "Политические", count: 20}] },
  "DEU": { eventsCount: 75, categories: [{id: 3, name: "Экономические", count: 35}, {id: 2, name: "Военные", count: 20}] }
});

// Для карусели
const featuredEvents = ref([]);

// Данные для графиков
const yearlyGrowthData = ref([]);
const categoryData = ref([]);

// Цвета для категорий
const categoryColors = {
  1: '#4285F4', // Политические события - синий
  2: '#EA4335', // Военные события - красный
  3: '#FBBC05', // Экономические события - желтый
  4: '#34A853', // Культурные события - зеленый
  5: '#9C27B0', // Научные открытия - фиолетовый
  6: '#FF9800', // Социальные изменения - оранжевый
  7: '#795548', // Религиозные события - коричневый
  8: '#607D8B'  // Другие события - серый
};

const getCategoryColor = (categoryId) => {
  return categoryColors[categoryId] || '#607D8B';
};

// Обработчики событий
const handleCountrySelected = (country) => {
  selectedCountry.value = country;
  
  if (country.clicked) {
    // Переход к странице событий для выбранной страны
    // navigateTo(`/events?country=${country.name}`);
    console.log(`Переход к событиям страны: ${country.name}`);
  }
};

const handleCategorySelected = (category) => {
  // Переход к странице событий с фильтром по категории
  // navigateTo(`/events?category=${category.id}`);
  console.log(`Переход к событиям категории: ${category.name}`);
};

// Загрузка данных
onMounted(async () => {
  try {
    // Получаем события
    const eventsData = await getAllEvents();
    events.value = eventsData;
    totalEvents.value = eventsData.length;
    
    // Находим диапазон лет
    const years = eventsData.map(e => e.year).sort();
    if (years.length > 0) {
      earliestYear.value = years[0];
      latestYear.value = years[years.length - 1];
    }
    
    // Получаем статистику по странам
    const countriesData = await getCountries();
    totalCountries.value = countriesData.length;
    
    // Выбираем события для карусели (например, самые последние или важные)
    featuredEvents.value = eventsData
      .sort((a, b) => b.importance - a.importance) // Сортировка по важности события
      .slice(0, 9); // Берем топ-9 важных событий
    
    // Получаем данные для графиков
    yearlyGrowthData.value = await getYearlyGrowth();
    
    // Формируем данные для пузырькового графика категорий
    const categoriesData = await getCategoryCounts();
    categoryData.value = categoriesData.map(category => ({
      ...category,
      color: getCategoryColor(category.id)
    }));
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 