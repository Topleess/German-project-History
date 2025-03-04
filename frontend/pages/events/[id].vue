<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '../../composables/useApi'
import EventMiniMap from '~/components/EventMiniMap.vue'

definePageMeta({
  title: 'Детальная информация о событии'
})

const route = useRoute()
const router = useRouter()
const api = useApi()
const event = ref(null)
const loading = ref(true)
const relatedEvents = ref([])

// Данные для мини-карты
const allEvents = ref([])
const connections = ref([])

// Категории событий
const categories = ref([])

// Тестовые данные для события
const testEvent = {
  id: 1,
  title: 'Первая мировая война',
  date: '1914-07-28',
  end_date: '1918-11-11',
  category_id: 2,
  description: 'Один из самых широкомасштабных вооружённых конфликтов в истории человечества. Первая мировая война началась 28 июля 1914 года и завершилась 11 ноября 1918 года. В результате войны прекратили своё существование четыре империи: Российская, Австро-Венгерская, Османская и Германская. Страны-участницы потеряли более 10 млн человек убитыми солдат, около 12 млн убитыми мирных жителей, около 55 млн были ранены.',
  location: 'Европа, Ближний Восток, Африка',
  importance: 5,
  image_url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Bundesarchiv_Bild_183-R05148%2C_Westfront%2C_deutsche_Soldaten_in_Sch%C3%BCtzengraben.jpg/1200px-Bundesarchiv_Bild_183-R05148%2C_Westfront%2C_deutsche_Soldaten_in_Sch%C3%BCtzengraben.jpg',
  sources: [
    { title: 'Википедия', url: 'https://ru.wikipedia.org/wiki/Первая_мировая_война' },
    { title: 'Британская энциклопедия', url: 'https://www.britannica.com/event/World-War-I' }
  ],
  related_events: [2, 3]
}

// Тестовые данные для связанных событий
const testRelatedEvents = [
  {
    id: 2,
    title: 'Революция 1917 года',
    date: '1917-02-23',
    end_date: '1917-11-07',
    category_id: 1,
    description: 'Революционные события в России, приведшие к свержению монархии и установлению советской власти',
    location: 'Российская империя'
  },
  {
    id: 3,
    title: 'Версальский договор',
    date: '1919-06-28',
    category_id: 1,
    description: 'Мирный договор, завершивший Первую мировую войну',
    location: 'Версаль, Франция'
  }
]

// Тестовые данные всех событий (для мини-карты)
const testAllEvents = [
  { 
    id: 1, 
    title: "Первая мировая война", 
    date: "1914-07-28", 
    end_date: "1918-11-11",
    category_id: 2, 
    description: "Один из самых широкомасштабных военных конфликтов в истории человечества.",
    location: "Европа",
    importance: 5,
  },
  { 
    id: 2, 
    title: "Революция 1917 года", 
    date: "1917-02-23", 
    end_date: "1917-11-07",
    category_id: 1, 
    description: "Цепь революционных событий в России в 1917 году, которые привели к свержению монархии и установлению советской власти.",
    location: "Россия",
    importance: 5,
  },
  { 
    id: 3, 
    title: "Версальский договор", 
    date: "1919-06-28",
    category_id: 1, 
    description: "Мирный договор, официально завершивший Первую мировую войну.",
    location: "Версаль, Франция",
    importance: 4,
  },
  { 
    id: 4, 
    title: "Теория относительности Эйнштейна", 
    date: "1915-11-25",
    category_id: 4, 
    description: "Публикация общей теории относительности Альбертом Эйнштейном.",
    location: "Германия",
    importance: 5,
  }
]

// Тестовые данные связей для мини-карты
const testConnections = [
  { source: 1, target: 2, value: 1, description: "Война привела к революции" },
  { source: 1, target: 3, value: 2, description: "Результат войны" },
  { source: 2, target: 3, value: 1, description: "Влияние на договор" }
]

// Форматирование даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ru-RU').format(date)
}

// Получение названия категории по ID
const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : ''
}

// Получение цвета категории по ID
const getCategoryColor = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.color : 'bg-gray-500'
}

// Переход к событию при клике на мини-карте
const navigateToEvent = (eventId) => {
  router.push(`/events/${eventId}`)
}

// Загрузка данных о событии
const fetchEvent = async () => {
  loading.value = true
  try {
    const { get } = useApi()
    const eventId = route.params.id
    
    // Загружаем данные с API
    event.value = await get(`/api/events/${eventId}`)
    
    // Загружаем категории
    categories.value = await get('/api/categories')
    
    // Загружаем связанные события
    const connectionsData = await get('/api/connections')
    connections.value = connectionsData.filter(
      c => c.cause_id === parseInt(eventId) || c.effect_id === parseInt(eventId)
    )
    
    // Загружаем все события для отображения связанных событий
    const allEventsData = await get('/api/events')
    allEvents.value = allEventsData
    
    // Формируем список связанных событий
    const relatedIds = new Set(
      connections.value.map(c => 
        c.cause_id === parseInt(eventId) ? c.effect_id : c.cause_id
      )
    )
    
    relatedEvents.value = allEventsData.filter(e => relatedIds.has(e.id))
  } catch (error) {
    console.error('Ошибка при загрузке события:', error)
  } finally {
    loading.value = false
  }
}

// Установка заголовка страницы с названием события
const setPageTitle = computed(() => {
  return event.value ? event.value.title : 'Загрузка события...'
})

// Динамическое обновление заголовка страницы
watch(event, () => {
  if (event.value) {
    document.title = `${event.value.title} | История`
  }
})

onMounted(() => {
  fetchEvent()
})
</script>

<template>
  <div class="p-4">
    <div v-if="loading">
      <div class="mb-2">
        <button @click="router.back()" class="inline-flex items-center text-gray-600 hover:text-gray-900">
          <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span class="text-sm">Назад</span>
        </button>
      </div>
      
      <h1 class="text-3xl font-bold mb-6">Загрузка события...</h1>
      
      <div class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    </div>
    
    <template v-else-if="event">
      <div class="mb-2">
        <button @click="router.back()" class="inline-flex items-center text-gray-600 hover:text-gray-900">
          <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span class="text-sm">Назад</span>
        </button>
      </div>
      
      <h1 class="text-3xl font-bold mb-6">{{ event.title }}</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Основная информация -->
        <div class="lg:col-span-2">
          <Card>
            <template #title>
              <div class="flex flex-wrap items-center">
                <span :class="[getCategoryColor(event.category_id), 'px-2 py-1 text-xs text-white rounded-full mr-2']">
                  {{ getCategoryName(event.category_id) }}
                </span>
              </div>
            </template>
            
            <div class="text-sm text-gray-500 mb-4">
              {{ formatDate(event.date) }}
              <span v-if="event.end_date"> - {{ formatDate(event.end_date) }}</span>
              <span v-if="event.location" class="ml-2 flex items-center inline-block">
                <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ event.location }}
              </span>
            </div>
            
            <div v-if="event.image_url" class="mb-6">
              <img :src="event.image_url" alt="Изображение события" class="w-full h-auto rounded-lg shadow-md">
            </div>
            
            <div class="prose prose-sm sm:prose lg:prose-lg max-w-none">
              <p>{{ event.description }}</p>
            </div>
            
            <div v-if="event.sources && event.sources.length > 0" class="mt-6">
              <h3 class="text-lg font-semibold mb-2">Источники:</h3>
              <ul class="list-disc list-inside space-y-1 ml-4">
                <li v-for="source in event.sources" :key="source.url">
                  <a :href="source.url" target="_blank" rel="noopener noreferrer" class="text-primary-600 hover:underline">
                    {{ source.title }}
                  </a>
                </li>
              </ul>
            </div>
          </Card>
        </div>
        
        <!-- Боковая панель -->
        <div class="space-y-6">
          <!-- Мини-карта событий -->
          <div class="mini-map-wrapper">
            <EventMiniMap 
              :event-id="Number(route.params.id)" 
              :events="allEvents" 
              :connections="connections" 
              :categories="categories"
              @navigate="navigateToEvent"
            />
          </div>
          
          <!-- Важность события -->
          <Card title="Важность события">
            <div class="flex items-center">
              <div class="flex-1 bg-gray-200 rounded-full h-2.5">
                <div 
                  class="bg-primary-600 h-2.5 rounded-full" 
                  :style="{ width: `${(event.importance / 5) * 100}%` }"
                ></div>
              </div>
              <span class="ml-2 text-sm font-medium text-gray-700">{{ event.importance }}/5</span>
            </div>
          </Card>
          
          <!-- Связанные события -->
          <Card v-if="relatedEvents.length > 0" title="Связанные события">
            <div class="space-y-4">
              <div 
                v-for="relatedEvent in relatedEvents" 
                :key="relatedEvent.id"
                class="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition cursor-pointer"
                @click="router.push(`/events/${relatedEvent.id}`)"
              >
                <div class="flex items-center mb-1">
                  <span :class="[getCategoryColor(relatedEvent.category_id), 'w-2 h-2 rounded-full mr-2']"></span>
                  <h4 class="font-medium text-gray-900">{{ relatedEvent.title }}</h4>
                </div>
                <div class="text-xs text-gray-500">
                  {{ formatDate(relatedEvent.date) }}
                  <span v-if="relatedEvent.end_date"> - {{ formatDate(relatedEvent.end_date) }}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </template>
    
    <div v-else class="text-center py-12">
      <p class="text-xl text-gray-500">Событие не найдено</p>
      <Button class="mt-4" @click="router.push('/events')">
        Вернуться к списку событий
      </Button>
    </div>
  </div>
</template>

<style scoped>
.mini-map-wrapper {
  position: relative;
  height: auto;
  width: 100%;
}
</style> 