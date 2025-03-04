<template>
  <div class="p-4">
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
        
        <div v-if="filteredEvents.length === 0 && !loading && !error" class="absolute inset-0 flex items-center justify-center text-gray-500">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-lg font-medium">Нет событий, соответствующих фильтрам</p>
            <Button class="mt-3" @click="resetFilters">Сбросить фильтры</Button>
          </div>
        </div>
        <svg width="100%" height="600"></svg>
      </div>
    </Card>
    
    <EventPopover
      :event="selectedEvent"
      :all-events="events"
      :categories="categories"
      :is-open="isPopoverOpen"
      @close="closePopover"
      @select-event="selectEventById"
      @view-details="viewEventDetails"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useNuxtApp } from '#app'
import { useRouter } from 'vue-router'
import EventPopover from '../components/EventPopover.vue'
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

// Загрузка данных с сервера
async function fetchData() {
  try {
    loading.value = true
    error.value = null
    
    // Загружаем категории
    const categoriesData = await get('/api/categories')
    categories.value = categoriesData
    
    // Загружаем события
    const eventsData = await get('/api/events')
    events.value = eventsData
    
    // Загружаем связи
    const connectionsData = await get('/api/connections')
    // Преобразуем связи в формат, подходящий для D3
    connections.value = connectionsData.map(conn => ({
      source: conn.cause_id,
      target: conn.effect_id,
      value: conn.strength || 1,
      description: conn.description
    }))
    
    loading.value = false
  } catch (err) {
    console.error('Ошибка при загрузке данных:', err)
    error.value = 'Не удалось загрузить данные. Пожалуйста, попробуйте позже.'
    loading.value = false
  }
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
  // Загружаем данные с сервера
  fetchData().then(() => {
    // Устанавливаем годы по умолчанию, охватывающие все события
    filters.value.startYear = minYear.value
    filters.value.endYear = maxYear.value
    
    initGraph()
  })
})

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
  
  // Сохраняем ссылку на svg
  svg.value = $d3.select(graphContainer.value).select('svg')
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  
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
  
  // Создаем симуляцию для графа
  simulation.value = $d3.forceSimulation()
    .force('link', $d3.forceLink().id(d => d.id).distance(20))
    .force('charge', $d3.forceManyBody().strength(-100))
    .force('center', $d3.forceCenter(width / 2, height / 2))
    .force('collision', $d3.forceCollide().radius(20))
    
  updateGraph()
}

function updateGraph() {
  if (!svg.value || !simulation.value) return
  
  const { $d3 } = useNuxtApp()
  
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
    value: conn.value
  }))
  
  // Очищаем существующий граф
  svg.value.select('g.graph-container').selectAll('*').remove()
  
  const graphG = svg.value.select('g.graph-container')
  
  // Добавляем связи
  const link = graphG.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(graphData.links)
    .join('line')
    .style('stroke', '#999')
    .style('stroke-opacity', 0.6)
    .style('stroke-width', d => Math.sqrt(d.value))
  
  // Добавляем узлы
  const node = graphG.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(graphData.nodes)
    .join('g')
    .attr('class', 'node')
    .attr('data-id', d => d.id)
    .call(drag(simulation.value, $d3))
    .on('click', (event, d) => {
      console.log('Клик на узле графа:', d)
      event.stopPropagation()
      selectEvent(d.data)
      zoomToNode(d)
    })
  
  // Добавляем круги для узлов
  node.append('circle')
    .attr('r', d => d.data.importance ? 6 + d.data.importance : 10)
    .style('fill', d => {
      const category = categories.value.find(c => c.id === d.group)
      return category ? category.color : '#ccc'
    })
    .style('stroke', '#fff')
    .style('stroke-width', 1.5)
  
  // Добавляем текст
  node.append('text')
    .text(d => d.name)
    .attr('x', d => (d.data.importance ? 8 + d.data.importance : 12))
    .attr('y', 5)
    .style('font-family', 'Inter, sans-serif')
    .style('font-size', '12px')
    .style('pointer-events', 'none')
  
  // Обновляем симуляцию
  simulation.value
    .nodes(graphData.nodes)
    .force('link', $d3.forceLink(graphData.links).id(d => d.id).distance(60))
    .on('tick', () => {
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
    
  // Установка alpha для начального разбегания
  if (Object.keys(nodePositions.value).length > 0) {
    simulation.value.alpha(0.3) // Даем графу немного "разбежаться"
  } else {
    simulation.value.alpha(1) // Полная сила для первоначального размещения
  }

  // Настройка значения alphaDecay для более плавного движения
  simulation.value.alphaDecay(0.015); // Уменьшено с 0.02, чтобы симуляция дольше продолжалась
  simulation.value.restart()
  
  // Добавляем обработчик клика по фону для сброса выбора
  svg.value.on('click', (event) => {
    if (event.target.tagName === 'svg') {
      closePopover()
    }
  })
  
  // Если узлов нет, сбрасываем масштаб
  if (graphData.nodes.length === 0) {
    resetZoom()
  } else if (graphData.nodes.length > 0 && filteredEvents.value.length !== events.value.length) {
    // Если фильтрация активна и есть узлы, подгоняем масштаб
    zoomToFit()
  }
}

function drag(simulation, d3) {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
    
    // Сохраняем позицию при начале перетаскивания
    nodePositions.value[event.subject.id] = { 
      x: event.subject.x, 
      y: event.subject.y 
    }
  }

  function dragged(event) {
    event.subject.fx = event.x
    event.subject.fy = event.y
    
    // Обновляем сохраненную позицию при перетаскивании
    nodePositions.value[event.subject.id] = { 
      x: event.x, 
      y: event.y 
    }
  }

  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0)
    
    // Убираем фиксацию, чтобы узел мог двигаться после перетаскивания
    event.subject.fx = null
    event.subject.fy = null
    
    // Сохраняем конечную позицию
    nodePositions.value[event.subject.id] = { 
      x: event.subject.x, 
      y: event.subject.y 
    }
  }

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

function zoomToNode(node) {
  const { $d3 } = useNuxtApp()
  
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  
  // Создаем трансформацию для масштабирования к узлу
  const scale = 2 // Уровень масштабирования
  const x = width / 2 - node.x * scale
  const y = height / 2 - node.y * scale
  
  svg.value.transition()
    .duration(750)
    .call(
      zoom.value.transform,
      $d3.zoomIdentity.translate(x, y).scale(scale)
    )
}

function zoomToFit() {
  if (graphData.nodes.length === 0) return
  
  const { $d3 } = useNuxtApp()
  const width = svg.value.node().getBoundingClientRect().width
  const height = 600
  
  // Находим границы графа
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity
  
  graphData.nodes.forEach(node => {
    minX = Math.min(minX, node.x)
    minY = Math.min(minY, node.y)
    maxX = Math.max(maxX, node.x)
    maxY = Math.max(maxY, node.y)
  })
  
  // Добавляем отступы
  const padding = 50
  minX -= padding
  minY -= padding
  maxX += padding
  maxY += padding
  
  // Рассчитываем коэффициент масштабирования
  const dx = maxX - minX
  const dy = maxY - minY
  const scale = Math.min(width / dx, height / dy)
  
  // Рассчитываем смещение для центрирования
  const translateX = width / 2 - scale * (minX + maxX) / 2
  const translateY = height / 2 - scale * (minY + maxY) / 2
  
  // Применяем трансформацию
  svg.value.transition()
    .duration(750)
    .call(
      zoom.value.transform,
      $d3.zoomIdentity.translate(translateX, translateY).scale(scale)
    )
}

function resetZoom() {
  const { $d3 } = useNuxtApp()
  
  svg.value.transition()
    .duration(750)
    .call(
      zoom.value.transform,
      $d3.zoomIdentity
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
}
</style> 