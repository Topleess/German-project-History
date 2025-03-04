<template>
  <div class="p-4">
    <!-- Компонент настроек графа -->
    <GraphSettings 
      :initial-settings="graphSettings"
      @update:settings="updateGraphSettings"
      @apply-settings="applyGraphSettings"
    />
    
    <div class="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Фильтры</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- Поиск -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Поиск событий</label>
          <Input 
            v-model="filters.search" 
            placeholder="Введите название события" 
            @input="updateFilters({ search: filters.search })"
          />
        </div>
        
        <!-- Фильтр по категориям -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Категории событий</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="category in categories"
              :key="category.id"
              class="px-3 py-1 text-sm rounded-full transition-colors"
              :class="[
                isCategorySelected(category.id) 
                  ? 'text-white' 
                  : 'text-gray-700 bg-gray-100 hover:bg-gray-200',
                isCategorySelected(category.id) ? category.color : ''
              ]"
              @click="toggleCategory(category.id)"
            >
              {{ category.name }}
            </button>
          </div>
        </div>
        
        <!-- Временной период -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Временной период</label>
          <div class="flex space-x-2">
            <Input 
              v-model="filters.startYear" 
              type="number" 
              placeholder="Год от" 
              class="w-full"
              @input="updateFilters({ startYear: filters.startYear })"
            />
            <Input 
              v-model="filters.endYear" 
              type="number" 
              placeholder="Год до" 
              class="w-full"
              @input="updateFilters({ endYear: filters.endYear })"
            />
          </div>
        </div>
      </div>
      
      <!-- Кнопка сброса фильтров -->
      <div class="mt-4">
        <Button 
          variant="outline" 
          @click="resetFilters"
        >
          Сбросить фильтры
        </Button>
      </div>
    </div>
    
    <Card>
      <template #title>
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold">Интерактивный граф исторических событий</h1>
          <div class="flex space-x-2">
            <Button @click="resetZoom" title="Сбросить масштаб">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4zm0 2h12v12H4V4zm3 3a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1z" clip-rule="evenodd" />
              </svg>
            </Button>
            <Button @click="zoomToFit" title="Подогнать масштаб под видимые узлы">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 110-2h4a1 1 0 011 1v4a1 1 0 11-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 112 0v1.586l2.293-2.293a1 1 0 011.414 1.414L6.414 15H8a1 1 0 110 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 110-2h1.586l-2.293-2.293a1 1 0 011.414-1.414L15 13.586V12a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
            </Button>
          </div>
        </div>
      </template>
      
      <div ref="graphContainer" class="w-full h-[600px] border border-gray-200 rounded-md overflow-hidden relative">
        <!-- Индикатор загрузки -->
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
          <div class="text-center">
            <svg class="animate-spin h-10 w-10 text-blue-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-gray-700 font-medium">Загрузка данных...</p>
          </div>
        </div>
        
        <!-- Сообщение об ошибке -->
        <div v-if="error" class="absolute inset-0 flex items-center justify-center bg-white z-10">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p class="text-red-600 font-medium mb-2">{{ error }}</p>
            <Button @click="fetchData">Повторить попытку</Button>
          </div>
        </div>
        
        <!-- Кнопка добавления нового события -->
        <div class="absolute bottom-4 right-4 z-10">
          <button 
            @click="openEventForm(null)" 
            class="rounded-full bg-blue-600 hover:bg-blue-700 text-white p-3 shadow-lg focus:outline-none"
            title="Добавить новое событие"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
        
        <div v-if="filteredEvents.length === 0 && !loading && !error" class="absolute inset-0 flex items-center justify-center text-gray-500">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-lg font-medium">Нет событий, соответствующих фильтрам</p>
            <Button class="mt-3" @click="resetFilters">Сбросить фильтры</Button>
          </div>
        </div>
        <svg width="100%" height="600" style="display: block; overflow: visible;"></svg>
      </div>
    </Card>
    
    <!-- Всплывающее окно с информацией о событии -->
    <EventPopover
      :event="selectedEvent"
      :all-events="events"
      :categories="categories"
      :connections="connections"
      :is-open="isPopoverOpen"
      @close="closePopover"
      @select-event="selectEventById"
      @view-details="viewEventDetails"
    />
    
    <!-- Модальное окно для создания/редактирования события -->
    <div v-if="isEventFormOpen" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div class="max-w-3xl w-full">
        <EventForm 
          :event="eventToEdit" 
          :categories="categories"
          :all-events="events"
          :connections="connections"
          @close="closeEventForm"
          @submit-success="handleEventFormSuccess"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useNuxtApp } from '#app'
import { useRouter } from 'vue-router'
import EventPopover from '../components/EventPopover.vue'
import GraphSettings from '../components/GraphSettings.vue'
import EventForm from '../components/EventForm.vue'
import { useApi } from '../composables/useApi'

definePageMeta({
  title: 'Интерактивный граф - История'
})

const graphContainer = ref(null)
const svg = ref(null)
const zoom = ref(null)
const simulation = ref(null)
const graphData = reactive({
  nodes: [],
  links: []
})
const nodePositions = ref({}) // Хранилище для позиций узлов

const selectedEvent = ref(null)
const isPopoverOpen = ref(false)
const router = useRouter()

// Получаем API клиент
const { get } = useApi()

// Состояние загрузки
const loading = ref(true)
const error = ref(null)

// Данные из API
const categories = ref([])
const events = ref([])
const connections = ref([])

// Настройки графа
const graphSettings = reactive({
  chargeStrength: -100,
  linkDistance: 50,
  collisionRadius: 20,
  nodeBaseSize: 25,
  showLabels: true,
  useImportanceSize: true
})

// Обновление настроек графа
function updateGraphSettings(newSettings) {
  Object.assign(graphSettings, newSettings)
}

// Применение настроек к графу
function applyGraphSettings() {
  if (!simulation.value) return
  
  const { $d3 } = useNuxtApp()
  
  // Обновляем силы в симуляции
  simulation.value
    .force('link', $d3.forceLink().id(d => d.id).distance(graphSettings.linkDistance))
    .force('charge', $d3.forceManyBody().strength(graphSettings.chargeStrength))
    .force('collision', $d3.forceCollide().radius(graphSettings.collisionRadius))
  
  // Перезапускаем симуляцию с высоким альфа для обновления графа
  simulation.value.alpha(0.8).restart()
  
  // Перерисовываем граф с новыми настройками
  updateGraph()
  
  // Показываем уведомление пользователю
  console.log('Настройки графа обновлены:', graphSettings)
}

// Загрузка данных с сервера
async function fetchData() {
  try {
    loading.value = true
    error.value = null
    
    console.log('Начинаем загрузку данных...')
    
    // Загружаем категории
    const categoriesData = await get('/api/categories')
    categories.value = categoriesData
    console.log('Загружено категорий:', categories.value.length)
    
    // Загружаем события
    const eventsData = await get('/api/events')
    events.value = eventsData
    console.log('Загружено событий:', events.value.length)
    
    // Загружаем связи
    const connectionsData = await get('/api/connections')
    // Преобразуем связи в формат, подходящий для D3
    connections.value = connectionsData.map(conn => ({
      source: conn.cause_id,
      target: conn.effect_id,
      value: conn.strength || 1,
      description: conn.description
    }))
    console.log('Загружено связей:', connections.value.length)
    
    loading.value = false
    
    // Проверяем загруженные данные
    if (events.value.length === 0) {
      console.warn('Не загружено ни одного события, используем тестовые данные')
      useTestData()
    }
    
    return true
  } catch (err) {
    console.error('Ошибка при загрузке данных:', err)
    error.value = 'Не удалось загрузить данные. Используем тестовые данные.'
    loading.value = false
    
    // Используем тестовые данные при ошибке
    useTestData()
    return true
  }
}

// Функция для использования тестовых данных
function useTestData() {
  console.log('Используем тестовые данные для графа')
  
  // Тестовые категории с настоящими цветами вместо классов Tailwind
  categories.value = [
    { id: 1, name: 'Политика', color: '#3b82f6' }, // blue-500
    { id: 2, name: 'Экономика', color: '#22c55e' }, // green-500
    { id: 3, name: 'Культура', color: '#a855f7' }, // purple-500
    { id: 4, name: 'Наука', color: '#eab308' } // yellow-500
  ]
  
  // Тестовые события
  events.value = [
    { id: 1, title: 'Событие 1', date: '2000-01-01', category_id: 1, importance: 3 },
    { id: 2, title: 'Событие 2', date: '2005-02-15', category_id: 2, importance: 2 },
    { id: 3, title: 'Событие 3', date: '2010-05-20', category_id: 1, importance: 4 },
    { id: 4, title: 'Событие 4', date: '2015-08-10', category_id: 3, importance: 1 },
    { id: 5, title: 'Событие 5', date: '2018-11-30', category_id: 4, importance: 5 },
    { id: 6, title: 'Событие 6', date: '2020-03-15', category_id: 2, importance: 3 }
  ]
  
  // Тестовые связи
  connections.value = [
    { source: 1, target: 2, value: 1, description: 'Связь 1-2' },
    { source: 1, target: 3, value: 2, description: 'Связь 1-3' },
    { source: 2, target: 4, value: 1, description: 'Связь 2-4' },
    { source: 3, target: 5, value: 3, description: 'Связь 3-5' },
    { source: 4, target: 6, value: 2, description: 'Связь 4-6' },
    { source: 5, target: 6, value: 1, description: 'Связь 5-6' }
  ]
}

// Расчет минимального и максимального года для временной шкалы
const minYear = computed(() => {
  if (events.value.length === 0) return 1900
  const minDate = Math.min(...events.value.map(e => new Date(e.date).getFullYear()))
  return Math.floor(minDate / 10) * 10 // Округляем до десятилетия
})

const maxYear = computed(() => {
  if (events.value.length === 0) return 2023
  const dates = events.value.map(e => 
    e.end_date ? new Date(e.end_date).getFullYear() : new Date(e.date).getFullYear()
  )
  const maxDate = Math.max(...dates)
  return Math.ceil(maxDate / 10) * 10 // Округляем до десятилетия
})

// Инициализация фильтров с начальными значениями, которые охватывают все события
const filters = ref({
  search: '',
  categories: null,
  startYear: null,
  endYear: null
})

// Устанавливаем начальные значения фильтров при монтировании компонента
onMounted(() => {
  console.log('Компонент графа смонтирован')
  setTimeout(() => {
    fetchData().then(() => {
      console.log('Данные получены, инициализируем граф')
      initGraph()
      
      // Запускаем диагностику DOM
      diagnoseDOMElements()
    })
  }, 500) // Даём время на инициализацию DOM
})

// Функция для диагностики DOM элементов
function diagnoseDOMElements() {
  console.log('Диагностика DOM элементов:')
  
  // Проверяем контейнер графа
  if (!graphContainer.value) {
    console.error('Контейнер графа не найден в DOM')
  } else {
    console.log('Контейнер графа найден в DOM:', graphContainer.value)
  }
  
  // Проверяем SVG элемент
  const svgElement = document.querySelector('.graph-visualization svg')
  if (!svgElement) {
    console.error('SVG элемент не найден в DOM')
  } else {
    console.log('SVG элемент найден в DOM, размеры:', {
      width: svgElement.getBoundingClientRect().width,
      height: svgElement.getBoundingClientRect().height
    })
  }
  
  // Проверяем контейнер узлов
  const nodesContainer = document.querySelector('.nodes-container')
  if (!nodesContainer) {
    console.error('Контейнер узлов не найден в DOM')
  } else {
    console.log('Контейнер узлов найден, содержит элементов:', nodesContainer.childNodes.length)
  }
  
  // Проверяем наличие узлов
  const nodes = document.querySelectorAll('.node')
  console.log('Найдено узлов в DOM:', nodes.length)
  
  // Проверяем наличие связей
  const links = document.querySelectorAll('.links line')
  console.log('Найдено связей в DOM:', links.length)
}

// Фильтрация событий
const filteredEvents = computed(() => {
  // Если года не заданы, используем минимальный и максимальный годы
  const startYear = filters.value.startYear !== null ? filters.value.startYear : minYear.value
  const endYear = filters.value.endYear !== null ? filters.value.endYear : maxYear.value
  
  return events.value.filter(event => {
    const eventYear = new Date(event.date).getFullYear()
    const eventEndYear = event.end_date ? new Date(event.end_date).getFullYear() : eventYear
    
    // Проверка по временному диапазону
    if (eventYear > endYear || eventEndYear < startYear) {
      return false
    }
    
    // Проверка по категориям
    if (filters.value.categories && !filters.value.categories.includes(event.category_id)) {
      return false
    }
    
    // Проверка по поисковому запросу
    if (filters.value.search && !event.title.toLowerCase().includes(filters.value.search.toLowerCase())) {
      return false
    }
    
    return true
  })
})

// Фильтрация связей
const filteredConnections = computed(() => {
  const filteredEventIds = filteredEvents.value.map(e => e.id)
  return connections.value.filter(conn => 
    filteredEventIds.includes(conn.source) && filteredEventIds.includes(conn.target)
  )
})

watch(filteredEvents, () => {
  updateGraph()
}, { deep: true })

function initGraph() {
  const { $d3 } = useNuxtApp()
  
  if (!$d3) {
    console.error('D3.js не инициализирован корректно')
    return
  }
  
  console.log('Инициализация графа началась')
  
  // Проверяем, существует ли контейнер для графа
  if (!graphContainer.value) {
    console.error('Контейнер для графа не найден')
    return
  }
  
  // Сохраняем ссылку на svg
  svg.value = $d3.select(graphContainer.value).select('svg')
  
  if (!svg.value.node()) {
    console.error('SVG элемент не найден в DOM')
    return
  }
  
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  
  console.log(`Размеры SVG: ${width}x${height}`)
  
  // Очищаем существующий SVG перед инициализацией
  svg.value.selectAll('*').remove()
  
  // Инициализация масштабирования
  zoom.value = $d3.zoom()
    .scaleExtent([0.1, 10])
    .on('zoom', (event) => {
      svg.value.select('g.graph-container').attr('transform', event.transform)
    })
  
  svg.value.call(zoom.value)
  
  // Создаем контейнер для графа
  const graphG = svg.value.append('g')
    .attr('class', 'graph-container')
  
  // Добавляем фоновый прямоугольник для обработки событий клика на пустом месте
  graphG.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'transparent')
  
  // Создаем симуляцию для графа с параметрами из настроек
  simulation.value = $d3.forceSimulation()
    .force('link', $d3.forceLink().id(d => d.id).distance(graphSettings.linkDistance))
    .force('charge', $d3.forceManyBody().strength(graphSettings.chargeStrength))
    .force('center', $d3.forceCenter(width / 2, height / 2))
    .force('collision', $d3.forceCollide().radius(graphSettings.collisionRadius))
    .alpha(0.9) // Увеличиваем значение alpha для более активного начального движения
    .alphaDecay(0.01) // Замедляем затухание для лучшей стабилизации
  
  console.log('Симуляция создана:', simulation.value)
  console.log('Настройки графа:', JSON.stringify(graphSettings)) // Логируем настройки
  
  // Обновляем/рисуем граф
  updateGraph()
  
  // Инициализируем с начальным масштабом
  svg.value.call(
    zoom.value.transform,
    $d3.zoomIdentity.translate(width / 2, height / 2).scale(1) // Изменено с 0.8 на 1 для лучшего начального масштаба
  )
  
  console.log('Инициализация графа завершена')
}

function updateGraph() {
  if (!svg.value || !simulation.value) {
    console.error('SVG или симуляция не инициализированы')
    return
  }
  
  const { $d3 } = useNuxtApp()
  console.log('Обновление графа. Узлов:', filteredEvents.value.length, 'Связей:', filteredConnections.value.length)
  
  // Сохраняем текущие позиции узлов перед обновлением
  const prevNodes = graphData.nodes || []
  prevNodes.forEach(node => {
    if (node.x !== undefined && node.y !== undefined) {
      nodePositions.value[node.id] = { x: node.x, y: node.y }
    }
  })
  
  // Подготовка данных для графа
  graphData.nodes = filteredEvents.value.map(event => {
    const node = {
      id: event.id,
      name: event.title,
      group: event.category_id,
      data: event
    }
    
    // Применяем сохраненные позиции, если они существуют
    if (nodePositions.value[node.id]) {
      node.x = nodePositions.value[node.id].x
      node.y = nodePositions.value[node.id].y
    }
    
    return node
  })
  
  graphData.links = filteredConnections.value.map(conn => ({
    source: conn.source,
    target: conn.target,
    value: conn.value || 1
  }))
  
  console.log('Данные подготовлены:', { 
    nodes: graphData.nodes.length, 
    links: graphData.links.length 
  })
  
  if (graphData.nodes.length === 0) {
    console.warn('Нет узлов для отображения')
    return
  }
  
  // Очищаем существующий граф
  const graphG = svg.value.select('g.graph-container')
  graphG.selectAll('*').remove()
  
  // Восстанавливаем прозрачный прямоугольник для обработки событий
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  graphG.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'transparent')
  
  // Добавляем отладочный круг в центре для проверки отображения
  graphG.append('circle')
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', 10)
    .attr('fill', 'red')
    .attr('class', 'debug-circle')
  
  // Функция для получения цвета категории
  function getCategoryColor(categoryId) {
    const category = categories.value.find(c => c.id === categoryId)
    if (!category) return '#cccccc'
    
    // Если цвет начинается с 'bg-', конвертируем в настоящий цвет
    if (category.color && category.color.startsWith('bg-')) {
      const colorMap = {
        'bg-blue-500': '#3b82f6',
        'bg-green-500': '#22c55e',
        'bg-purple-500': '#a855f7',
        'bg-yellow-500': '#eab308',
        'bg-red-500': '#ef4444',
        'bg-orange-500': '#f97316',
        'bg-teal-500': '#14b8a6',
        'bg-indigo-500': '#6366f1',
        'bg-pink-500': '#ec4899',
        'bg-gray-500': '#6b7280'
      }
      return colorMap[category.color] || '#cccccc'
    }
    
    return category.color || '#cccccc'
  }
  
  // Добавляем связи
  const link = graphG.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(graphData.links)
    .enter()
    .append('line')
    .attr('stroke', '#999')
    .attr('stroke-opacity', 0.6)
    .attr('stroke-width', d => Math.sqrt(d.value))
  
  // Добавляем узлы в отдельный контейнер для лучшей производительности
  const nodesContainer = graphG.append('g').attr('class', 'nodes-container')
  
  // Добавляем узлы
  const node = nodesContainer.selectAll('.node')
    .data(graphData.nodes)
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('data-id', d => d.id)
    .call(drag(simulation.value, $d3))
    .on('click', (event, d) => {
      event.stopPropagation()
      selectEvent(d.data)
      zoomToNode(d)
    })
  
  // Добавляем круги для узлов с явными параметрами
  node.append('circle')
    .attr('r', d => {
      // Используем большой размер узлов независимо от значимости
      const baseSize = graphSettings.nodeBaseSize
      if (graphSettings.useImportanceSize && d.data.importance) {
        return Math.max(baseSize, baseSize + d.data.importance * 2)
      }
      return baseSize
    })
    .attr('fill', d => getCategoryColor(d.group))
    .attr('stroke', '#000') // Изменено с #fff на #000 для лучшей видимости
    .attr('stroke-width', 2) // Увеличено для лучшей видимости
    .attr('opacity', 1)
  
  // Добавляем текст с учетом настройки видимости подписей
  if (graphSettings.showLabels) {
    node.append('text')
      .text(d => d.name)
      .attr('x', d => {
        const baseSize = graphSettings.nodeBaseSize
        return graphSettings.useImportanceSize && d.data.importance 
          ? Math.max(baseSize, baseSize + d.data.importance * 2) + 2
        : baseSize + 2
      })
      .attr('y', 5)
      .attr('font-family', 'Inter, sans-serif')
      .attr('font-size', '14px') // Увеличено с 12px для лучшей читаемости
      .attr('font-weight', 'bold') // Добавлено для лучшей читаемости
      .attr('pointer-events', 'none')
      .attr('fill', '#000')
      .attr('stroke', '#fff') // Добавлено для лучшей читаемости на темном фоне
      .attr('stroke-width', '0.5') // Тонкая обводка для текста
  }
  
  // Логируем число созданных узлов и связей для отладки
  console.log(`Создано ${node.size()} узлов и ${link.size()} связей на графе`)
  
  // Устанавливаем начальные позиции для узлов, если они не определены
  graphData.nodes.forEach((node, i) => {
    if (node.x === undefined || node.y === undefined) {
      // Распределяем узлы по кругу
      const angle = (i / graphData.nodes.length) * 2 * Math.PI;
      const radius = Math.min(width, height) / 3;
      node.x = width / 2 + radius * Math.cos(angle);
      node.y = height / 2 + radius * Math.sin(angle);
    }
  });
  
  // Обновляем симуляцию с новыми данными
  simulation.value
    .nodes(graphData.nodes)
    .force('link', $d3.forceLink(graphData.links).id(d => d.id).distance(graphSettings.linkDistance))
    .force('charge', $d3.forceManyBody().strength(graphSettings.chargeStrength))
    .force('collision', $d3.forceCollide().radius(graphSettings.collisionRadius))
    .on('tick', () => {
      // Логируем координаты узлов в первом тике для отладки
      if (!window._loggedPositions) {
        console.log('Первые координаты узлов:', 
          graphData.nodes.slice(0, 3).map(n => ({ id: n.id, x: n.x, y: n.y }))
        )
        console.log('Текущие настройки графа:', JSON.stringify(graphSettings))
        window._loggedPositions = true
      }
      
      // Показываем процесс добавления узлов и связей
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
      
      node
        .attr('transform', d => `translate(${d.x},${d.y})`)
        
      // Сохраняем позиции при каждом тике для будущего использования
      graphData.nodes.forEach(d => {
        if (d.x !== undefined && d.y !== undefined) {
          nodePositions.value[d.id] = { x: d.x, y: d.y }
        }
      })
    })
  
  // Устанавливаем высокую начальную силу симуляции для распределения узлов
  simulation.value
    .alpha(1)
    .alphaDecay(0.005)
    .restart()
  
  console.log('Граф обновлен и симуляция запущена с настройками:', JSON.stringify({
    chargeStrength: graphSettings.chargeStrength,
    linkDistance: graphSettings.linkDistance,
    collisionRadius: graphSettings.collisionRadius,
    nodeBaseSize: graphSettings.nodeBaseSize
  }))
    
  // Добавляем обработчик клика по фону для сброса выбора
  svg.value.on('click', (event) => {
    if (event.target.tagName === 'svg') {
      closePopover()
    }
  })
}

function drag(simulation, d3) {
  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    
    // Запоминаем начальную позицию
    d.fx = d.x
    d.fy = d.y
    
    console.log('Начало перетаскивания узла:', d.id)
    
    // Сохраняем позицию при начале перетаскивания
    nodePositions.value[d.id] = { 
      x: d.x, 
      y: d.y 
    }
  }

  function dragged(event, d) {
    // Перемещаем узел за курсором
    d.fx = event.x
    d.fy = event.y
    
    // Обновляем сохраненную позицию при перетаскивании
    nodePositions.value[d.id] = { 
      x: event.x, 
      y: event.y 
    }
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0)
    
    // Оставляем узел на фиксированной позиции после перетаскивания
    d.fx = event.x
    d.fy = event.y
    
    console.log('Завершение перетаскивания узла:', d.id, {x: event.x, y: event.y})
    
    // Сохраняем конечную позицию
    nodePositions.value[d.id] = { 
      x: event.x, 
      y: event.y 
    }
  }

  // Создаем поведение перетаскивания
  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended)
}

function selectEvent(event) {
  console.log('Событие выбрано:', event)
  selectedEvent.value = event
  isPopoverOpen.value = true
  console.log('Статус всплывающего окна:', isPopoverOpen.value)
}

function selectEventById(id) {
  const event = events.value.find(e => e.id === id)
  if (event) {
    selectEvent(event)
    
    // Найти соответствующий узел графа и масштабировать к нему
    const node = graphData.nodes.find(n => n.id === id)
    if (node) {
      zoomToNode(node)
    }
  }
}

function closePopover() {
  isPopoverOpen.value = false
}

function viewEventDetails(id) {
  // Перенаправляем на страницу детального просмотра события
  router.push(`/events/${id}`)
}

function zoomToNode(d) {
  if (!svg.value || !zoom.value) return
  
  const { $d3 } = useNuxtApp()
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  
  // Если узел не имеет координат, ничего не делаем
  if (d.x === undefined || d.y === undefined) return
  
  // Масштаб для центрирования на узле
  const scale = 2
  
  // Применяем трансформацию с анимацией
  svg.value
    .transition()
    .duration(750)
    .call(
      zoom.value.transform,
      $d3.zoomIdentity
        .translate(width / 2 - d.x * scale, height / 2 - d.y * scale)
        .scale(scale)
    )
}

function zoomToFit() {
  if (!svg.value || !zoom.value || graphData.nodes.length === 0) {
    console.error('Невозможно масштабировать: отсутствует SVG, zoom или нет узлов')
    return resetZoom()
  }
  
  const { $d3 } = useNuxtApp()
  const svgNode = svg.value.node()
  const width = svgNode.getBoundingClientRect().width
  const height = 600
  
  // Получаем текущие координаты всех узлов
  const xs = graphData.nodes.map(d => d.x).filter(x => x !== undefined)
  const ys = graphData.nodes.map(d => d.y).filter(y => y !== undefined)
  
  if (xs.length === 0 || ys.length === 0) {
    console.warn('Координаты узлов не определены, невозможно масштабировать')
    return resetZoom()
  }
  
  // Вычисляем границы
  const xExtent = $d3.extent(xs)
  const yExtent = $d3.extent(ys)
  
  // Если нет корректных координат, сбрасываем масштаб
  if (xExtent[0] === undefined || yExtent[0] === undefined) {
    console.warn('Границы не определены, сбрасываем масштаб')
    return resetZoom()
  }
  
  console.log('Масштабирование к размеру графа', {
    xExtent,
    yExtent,
    nodesWithCoords: xs.length
  })
  
  // Добавляем отступы
  const padding = 50
  const xWidth = xExtent[1] - xExtent[0] + padding * 2
  const yHeight = yExtent[1] - yExtent[0] + padding * 2
  
  // Вычисляем масштаб и смещение
  const scale = Math.min(width / xWidth, height / yHeight, 3) // Ограничиваем масштаб
  const translateX = width / 2 - scale * (xExtent[0] + xExtent[1]) / 2
  const translateY = height / 2 - scale * (yExtent[0] + yExtent[1]) / 2
  
  // Применяем трансформацию с анимацией
  svg.value
    .transition()
    .duration(750)
    .call(
      zoom.value.transform,
      $d3.zoomIdentity.translate(translateX, translateY).scale(scale)
    )
}

function resetZoom() {
  if (!svg.value || !zoom.value) {
    console.error('SVG или zoom не инициализированы')
    return
  }
  
  const { $d3 } = useNuxtApp()
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  
  console.log('Сброс масштаба')
  
  svg.value
    .transition()
    .duration(750)
    .call(
      zoom.value.transform,
      $d3.zoomIdentity.translate(width / 2, height / 2).scale(0.8)
    )
}

function resetFilters() {
  filters.value = {
    search: '',
    categories: null,
    startYear: minYear.value,
    endYear: maxYear.value
  }
}

function updateFilters(newFilters) {
  filters.value = { ...filters.value, ...newFilters }
}

// Проверка выбрана ли категория
function isCategorySelected(categoryId) {
  return filters.value.categories && filters.value.categories.includes(categoryId)
}

// Переключение категории
function toggleCategory(categoryId) {
  if (!filters.value.categories) {
    filters.value.categories = [categoryId]
  } else if (filters.value.categories.includes(categoryId)) {
    filters.value.categories = filters.value.categories.filter(id => id !== categoryId)
    if (filters.value.categories.length === 0) {
      filters.value.categories = null
    }
  } else {
    filters.value.categories.push(categoryId)
  }
  
  updateFilters({ categories: filters.value.categories })
}

// Модальное окно для создания/редактирования события
const isEventFormOpen = ref(false)
const eventToEdit = ref(null)

function openEventForm(event) {
  eventToEdit.value = event ? { ...event } : null
  isEventFormOpen.value = true
}

function closeEventForm() {
  isEventFormOpen.value = false
}

function handleEventFormSuccess(event) {
  // Обработка успешной отправки формы
  closeEventForm()
  // Обновление данных графа
  fetchData().then(() => {
    initGraph()
  })
}
</script>

<style scoped>
.graph-container {
  padding: 1rem;
}
.graph-card {
  min-height: 400px;
}
.graph-visualization {
  width: 100%;
  height: 600px;
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: visible !important;
}

/* Убеждаемся, что элементы графа видны */
:deep(.node) {
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 100 !important;
}

:deep(.node circle) {
  visibility: visible !important;
  opacity: 1 !important;
  stroke-width: 2px !important;
}

:deep(.links line) {
  stroke-width: 2px !important;
  stroke-opacity: 0.8 !important;
}

:deep(.debug-circle) {
  visibility: visible !important;
  opacity: 1 !important;
}
</style> 