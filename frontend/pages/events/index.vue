<template>
  <div class="p-4">
    <Card>
      <template #title>
        <div class="flex flex-col md:flex-row md:items-center justify-between w-full">
          <h1 class="text-2xl font-bold mb-4 md:mb-0">Библиотека исторических событий</h1>
          <div class="w-full md:w-1/3">
            <Input 
              v-model="search" 
              placeholder="Поиск" 
              @input="applyFilter"
            >
              <template #append>
                <button class="absolute inset-y-0 right-0 flex items-center pr-3" @click="applyFilter">
                  <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                  </svg>
                </button>
              </template>
            </Input>
          </div>
        </div>
      </template>
      
      <div class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Фильтр по категории -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
            <select 
              v-model="selectedCategory"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              @change="applyFilter"
            >
              <option :value="null">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          
          <!-- Фильтр по дате начала -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">От</label>
            <Input 
              v-model="startDate" 
              type="date"
              @input="applyFilter"
            />
          </div>
          
          <!-- Фильтр по дате окончания -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">До</label>
            <Input 
              v-model="endDate" 
              type="date"
              @input="applyFilter"
            />
          </div>
          
          <!-- Кнопка сброса фильтров -->
          <div class="flex items-end">
            <Button 
              variant="outline" 
              class="w-full"
              @click="clearFilters"
            >
              Сбросить фильтры
            </Button>
          </div>
        </div>
      </div>
      
      <!-- Список событий -->
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
      
      <div v-else-if="filteredEvents.length === 0" class="text-center py-8 text-gray-500">
        Нет событий, соответствующих заданным критериям
      </div>
      
      <div v-else>
        <!-- Отображение событий по годам -->
        <div v-for="(yearEvents, year) in eventsByYear" :key="year" class="mb-10">
          <div class="relative mb-6">
            <h2 class="text-2xl font-bold text-gray-800 inline-block bg-white pr-4 relative z-10">{{ year }}</h2>
            <div class="absolute left-0 right-0 top-1/2 h-px bg-gray-300"></div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card 
              v-for="event in yearEvents" 
              :key="event.id"
              :title="event.title"
              hoverable
              @click="navigateTo(`/events/${event.id}`)"
            >
              <div class="relative">
                <div class="flex items-center mb-2">
                  <span :class="[getCategoryColor(event.category_id), 'px-2 py-1 text-xs text-white rounded-full']">
                    {{ getCategoryName(event.category_id) }}
                  </span>
                  <span class="ml-2 text-sm text-gray-500">
                    {{ formatDate(event.date) }}
                    <span v-if="event.end_date"> - {{ formatDate(event.end_date) }}</span>
                  </span>
                </div>
                
                <p class="text-sm text-gray-700 line-clamp-3">{{ event.description }}</p>
                
                <div v-if="event.location" class="mt-2 text-xs text-gray-500 flex items-center">
                  <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {{ event.location }}
                </div>
                
                <!-- Кнопка редактирования -->
                <button 
                  @click.stop="editEvent(event)"
                  class="absolute top-0 right-0 p-1 bg-white rounded-full shadow hover:bg-gray-100"
                  title="Редактировать событие"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </Card>

    <!-- Кнопка добавления нового события -->
    <div class="fixed bottom-6 right-6">
      <button 
        @click="openEventForm()" 
        class="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg flex items-center justify-center focus:outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </div>

    <!-- Модальное окно для формы события -->
    <Modal v-if="isEventFormOpen" @close="closeEventForm">
      <EventForm 
        :event="selectedEvent" 
        @close="closeEventForm" 
        @success="handleEventSuccess"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'
import Modal from '~/components/Modal.vue'
import EventForm from '~/components/EventForm.vue'

definePageMeta({
  title: 'Библиотека исторических событий'
})

const api = useApi()
const search = ref('')
const selectedCategory = ref(null)
const startDate = ref(null)
const endDate = ref(null)
const startDateMenu = ref(false)
const endDateMenu = ref(false)
const loading = ref(false)
const events = ref([])
const filteredEvents = ref([])
const categories = ref([])
const isEventFormOpen = ref(false)
const selectedEvent = ref(null)

// Категории событий
const categoriesData = [
  { id: 1, name: 'Политические', color: 'bg-blue-500' },
  { id: 2, name: 'Военные', color: 'bg-red-500' },
  { id: 3, name: 'Экономические', color: 'bg-green-500' },
  { id: 4, name: 'Культурные', color: 'bg-purple-500' },
  { id: 5, name: 'Социальные', color: 'bg-yellow-500' }
]

// Расширенные тестовые данные для событий из разных лет
const testEvents = [
  {
    id: 1,
    title: 'Первая мировая война',
    date: '1914-07-28',
    end_date: '1918-11-11',
    category_id: 2,
    description: 'Один из самых широкомасштабных вооружённых конфликтов в истории человечества',
    location: 'Европа, Ближний Восток, Африка'
  },
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
  },
  {
    id: 4,
    title: 'Теория относительности Эйнштейна',
    date: '1915-11-25',
    category_id: 4,
    description: 'Публикация общей теории относительности Альбертом Эйнштейном',
    location: 'Германия'
  },
  {
    id: 5,
    title: 'Великая депрессия',
    date: '1929-10-29',
    end_date: '1939-09-01',
    category_id: 5,
    description: 'Мировой экономический кризис, начавшийся после краха на Нью-Йоркской фондовой бирже',
    location: 'США, Европа'
  },
  {
    id: 6,
    title: 'Вторая мировая война',
    date: '1939-09-01',
    end_date: '1945-09-02',
    category_id: 2,
    description: 'Крупнейший вооружённый конфликт в истории человечества',
    location: 'Европа, Азия, Африка'
  },
  {
    id: 7,
    title: 'Холодная война',
    date: '1947-03-12',
    end_date: '1991-12-26',
    category_id: 1,
    description: 'Геополитическое противостояние между СССР и США и их союзниками',
    location: 'Весь мир'
  }
]

// Группировка событий по годам
const eventsByYear = computed(() => {
  const grouped = {}
  
  // Сортируем события по дате
  const sortedEvents = [...filteredEvents.value].sort((a, b) => {
    return new Date(a.date) - new Date(b.date)
  })
  
  // Группируем по годам
  sortedEvents.forEach(event => {
    const year = new Date(event.date).getFullYear()
    if (!grouped[year]) {
      grouped[year] = []
    }
    grouped[year].push(event)
  })
  
  // Сортируем ключи (годы) в обратном порядке, чтобы показать сначала новые
  return Object.keys(grouped)
    .sort((a, b) => b - a)
    .reduce((obj, key) => {
      obj[key] = grouped[key]
      return obj
    }, {})
})

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

// Применение фильтров
const applyFilter = () => {
  filteredEvents.value = events.value.filter(event => {
    // Фильтр по поиску
    const searchMatch = !search.value || 
      event.title.toLowerCase().includes(search.value.toLowerCase()) ||
      event.description.toLowerCase().includes(search.value.toLowerCase())
    
    // Фильтр по категории
    const categoryMatch = !selectedCategory.value || event.category_id === selectedCategory.value
    
    // Фильтр по дате начала
    const startDateMatch = !startDate.value || new Date(event.date) >= new Date(startDate.value)
    
    // Фильтр по дате окончания
    const endDateMatch = !endDate.value || new Date(event.date) <= new Date(endDate.value)
    
    return searchMatch && categoryMatch && startDateMatch && endDateMatch
  })
}

// Загрузка данных
const fetchEvents = async () => {
  loading.value = true
  try {
    // Загружаем данные с API
    const { get } = useApi()
    const eventsData = await get('/api/events')
    const categoriesData = await get('/api/categories')
    
    events.value = eventsData
    filteredEvents.value = eventsData
    categories.value = categoriesData
  } catch (error) {
    console.error('Ошибка при загрузке событий:', error)
  } finally {
    loading.value = false
  }
}

// Очистка всех фильтров
const clearFilters = () => {
  search.value = ''
  selectedCategory.value = null
  startDate.value = null
  endDate.value = null
  applyFilter()
}

// Открытие формы для создания нового события
const openEventForm = (event = null) => {
  selectedEvent.value = event
  isEventFormOpen.value = true
}

// Закрытие формы события
const closeEventForm = () => {
  isEventFormOpen.value = false
  selectedEvent.value = null
}

// Обработка успешного создания/редактирования события
const handleEventSuccess = () => {
  closeEventForm()
  fetchEvents()
}

// Функция для редактирования события
const editEvent = (event) => {
  openEventForm(event)
}

onMounted(() => {
  fetchEvents()
})
</script>

<style>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 