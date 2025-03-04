<template>
  <div class="event-mini-map">
    <div 
      class="mini-map-header"
      @click="navigateToFullGraph"
      title="Нажмите для перехода к полному графу"
    >
      <h3 class="mini-map-title">
        Визуализация связей
        <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
          <polyline points="15 3 21 3 21 9"></polyline>
          <line x1="10" y1="14" x2="21" y2="3"></line>
        </svg>
      </h3>
    </div>
    <div 
      ref="miniMapContainer" 
      class="mini-map-container"
      :class="{ 'mini-map-expanded': isExpanded }"
      @mouseenter="handleMouseEnter" 
      @mouseleave="handleMouseLeave"
    >
      <svg 
        width="100%" 
        height="100%"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
      ></svg>
      <button 
        v-if="isExpanded" 
        class="close-button"
        @click="isExpanded = false"
        title="Закрыть"
      >
        ✕
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { useNuxtApp } from '#app'
import { useRouter } from 'vue-router'

const props = defineProps({
  // ID текущего события
  eventId: {
    type: Number,
    required: true
  },
  // Все события системы
  events: {
    type: Array,
    required: true
  },
  // Связи между событиями
  connections: {
    type: Array,
    default: () => []
  },
  // Категории событий
  categories: {
    type: Array,
    required: true
  },
  // Максимальное количество отображаемых событий (для производительности)
  maxEvents: {
    type: Number,
    default: 15
  }
})

const emit = defineEmits(['navigate'])

const miniMapContainer = ref(null)
const isExpanded = ref(false)
const svg = ref(null)
const simulation = ref(null)
const graphData = ref({
  nodes: [],
  links: []
})
const isMouseInside = ref(false)
const mouseCheckInterval = ref(null)
const centralNodePosition = ref({ x: 0, y: 0 })

const router = useRouter()

// Состояние для отслеживания перетаскивания
const isDragging = ref(false)
const isPanning = ref(false)
const startPos = ref({ x: 0, y: 0 })
const viewTransform = ref({ x: 0, y: 0 })

// Обработчик входа мыши в область мини-карты
function handleMouseEnter() {
  isMouseInside.value = true;
  isExpanded.value = true;
  
  // Останавливаем предыдущую проверку, если она была
  if (mouseCheckInterval.value) {
    clearInterval(mouseCheckInterval.value);
    mouseCheckInterval.value = null;
  }
}

// Обработчик нажатия кнопки мыши
function handleMouseDown(event) {
  // Определяем, по какому элементу кликнули
  const target = event.target;
  
  // Если клик по кругу или тексту (части узла), игнорируем, чтобы работало перетаскивание узлов
  if (target.tagName === 'circle' || target.tagName === 'text') {
    return;
  }
  
  // Если клик по SVG или его фону, активируем режим перемещения
  isPanning.value = true;
  startPos.value = { x: event.clientX, y: event.clientY };
  
  // Устанавливаем курсор "grabbing" на время перемещения
  document.body.style.cursor = 'grabbing';
  
  // Предотвращаем выделение текста при движении
  event.preventDefault();
}

// Обработчик движения мыши
function handleMouseMove(event) {
  if (!isPanning.value) return;
  
  // Вычисляем смещение с момента начала перемещения
  const dx = event.clientX - startPos.value.x;
  const dy = event.clientY - startPos.value.y;
  
  // Обновляем позицию графа
  viewTransform.value.x += dx;
  viewTransform.value.y += dy;
  
  // Применяем трансформацию к контейнеру графа
  svg.value.select('g.mini-graph-container')
    .attr('transform', `translate(${viewTransform.value.x}, ${viewTransform.value.y})`);
  
  // Обновляем начальную позицию для следующего перемещения
  startPos.value = { x: event.clientX, y: event.clientY };
}

// Обработчик отпускания кнопки мыши
function handleMouseUp() {
  if (isPanning.value) {
    isPanning.value = false;
    document.body.style.cursor = '';
  }
}

// Проверяет, находится ли мышь внутри элемента
function checkIfMouseIsOver(event) {
  if (!miniMapContainer.value) return false;
  
  const rect = miniMapContainer.value.getBoundingClientRect();
  const headerRect = miniMapContainer.value.previousElementSibling.getBoundingClientRect();
  const x = event.clientX;
  const y = event.clientY;
  
  // Проверяем, находится ли мышь в контейнере или в заголовке
  const inContainer = x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
  const inHeader = x >= headerRect.left && x <= headerRect.right && y >= headerRect.top && y <= headerRect.bottom;
  
  return inContainer || inHeader;
}

// Улучшенная обработка выхода курсора
function handleMouseLeave(event) {
  // Сначала отключаем режим перемещения
  if (isPanning.value) {
    isPanning.value = false;
    document.body.style.cursor = '';
  }
  
  isMouseInside.value = false;
  
  // Запускаем интервал проверки положения мыши
  if (!mouseCheckInterval.value) {
    mouseCheckInterval.value = setInterval(() => {
      if (!isMouseInside.value && isExpanded.value) {
        const mouseEvent = { clientX: event.clientX, clientY: event.clientY };
        const isOver = checkIfMouseIsOver(mouseEvent);
        
        if (!isOver) {
          isExpanded.value = false;
          clearInterval(mouseCheckInterval.value);
          mouseCheckInterval.value = null;
        }
      } else if (!isExpanded.value) {
        // Если карта уже закрыта, останавливаем интервал
        clearInterval(mouseCheckInterval.value);
        mouseCheckInterval.value = null;
      }
    }, 500); // Проверяем каждые 500 мс
  }
}

// Функция для центрирования на центральном узле
function centerOnMainNode() {
  if (!svg.value || !centralNodePosition.value) return;
  
  const containerWidth = miniMapContainer.value.clientWidth;
  const containerHeight = miniMapContainer.value.clientHeight;
  
  // Рассчитываем смещение, чтобы центральный узел оказался в центре контейнера
  const offsetX = (containerWidth / 2) - centralNodePosition.value.x;
  const offsetY = (containerHeight / 2) - centralNodePosition.value.y;
  
  // Обновляем трансформацию и применяем ее
  viewTransform.value = { x: offsetX, y: offsetY };
  svg.value.select('g.mini-graph-container')
    .attr('transform', `translate(${viewTransform.value.x}, ${viewTransform.value.y})`);
}

// Определяем, какие события показывать на мини-карте
const miniMapEvents = computed(() => {
  if (props.events.length === 0) return []
  
  // Начинаем с текущего события
  const centralEvent = props.events.find(e => e.id === props.eventId)
  if (!centralEvent) return []
  
  // Получаем связанные события (первый уровень)
  const relatedEventIds = [
    ...props.connections
      .filter(conn => conn.source === props.eventId)
      .map(conn => conn.target),
    ...props.connections
      .filter(conn => conn.target === props.eventId)
      .map(conn => conn.source)
  ]
  
  // Собираем уникальные ID связанных событий
  const uniqueRelatedIds = [...new Set(relatedEventIds)]
  
  // Список всех событий, которые будем отображать
  const eventsToShow = []
  
  // Добавляем центральное событие
  eventsToShow.push(centralEvent)
  
  // Добавляем связанные события
  uniqueRelatedIds.forEach(id => {
    const event = props.events.find(e => e.id === id)
    if (event) eventsToShow.push(event)
  })
  
  // Если общее количество событий меньше maxEvents, добавляем другие события
  if (eventsToShow.length < props.maxEvents) {
    // Сколько ещё событий можем добавить
    const remainingSlots = props.maxEvents - eventsToShow.length
    
    // Получаем ID событий, которые уже добавлены
    const addedIds = eventsToShow.map(e => e.id)
    
    // Добавляем события, которых ещё нет в списке
    props.events
      .filter(e => !addedIds.includes(e.id))
      .slice(0, remainingSlots)
      .forEach(e => eventsToShow.push(e))
  }
  
  return eventsToShow
})

// Определяем связи для мини-карты
const miniMapConnections = computed(() => {
  const eventIds = miniMapEvents.value.map(e => e.id)
  return props.connections.filter(conn => 
    eventIds.includes(conn.source) && eventIds.includes(conn.target)
  )
})

// Инициализация мини-карты при монтировании компонента
onMounted(() => {
  initMiniMap()
  
  // Добавляем обработчик для завершения перетаскивания, если мышь была отпущена за пределами компонента
  window.addEventListener('mouseup', handleMouseUp)
  
  // Добавляем обработчик движения мыши для отслеживания положения
  document.addEventListener('mousemove', (event) => {
    if (miniMapContainer.value && isExpanded.value) {
      isMouseInside.value = checkIfMouseIsOver(event);
    }
  });
})

// Очистка обработчиков при размонтировании
onUnmounted(() => {
  if (simulation.value) {
    simulation.value.stop()
  }
  window.removeEventListener('mouseup', handleMouseUp)
  document.removeEventListener('mousemove', null);
  
  if (mouseCheckInterval.value) {
    clearInterval(mouseCheckInterval.value);
  }
})

// Обновление мини-карты при изменении событий
watch([miniMapEvents, miniMapConnections], () => {
  updateMiniMap()
  
  // После обновления, центрируем на главном узле
  nextTick(() => {
    // Небольшая задержка, чтобы симуляция успела обновить положения
    setTimeout(() => {
      centerOnMainNode();
    }, 100);
  });
}, { deep: true })

// Обработка изменения состояния развертывания
watch(isExpanded, (newVal) => {
  if (newVal) {
    // При разворачивании центрируем на главном узле
    nextTick(() => {
      centerOnMainNode();
    });
  }
})

// Инициализация D3.js графа для мини-карты
function initMiniMap() {
  const { $d3 } = useNuxtApp()
  
  // Инициализация SVG
  svg.value = $d3.select(miniMapContainer.value).select('svg')
  
  // Создаем контейнер для графа
  svg.value.append('g')
    .attr('class', 'mini-graph-container')

  // Инициализация симуляции для прямоугольной формы
  simulation.value = $d3.forceSimulation()
    .force('link', $d3.forceLink().id(d => d.id).distance(60))
    .force('charge', $d3.forceManyBody().strength(-150))
    .force('center', $d3.forceCenter(120, 67.5)) // Центрируем по размерам контейнера
    .force('collision', $d3.forceCollide().radius(20))
    .stop() // Останавливаем симуляцию до обновления данных
  
  // Первоначальное обновление
  updateMiniMap()
}

// Получаем цветовую информацию для категории
function getCategoryColor(categoryId) {
  const category = props.categories.find(c => c.id === categoryId)
  return category ? category.color : '#cccccc'
}

// Обновление данных графа и его визуализация
function updateMiniMap() {
  if (!svg.value || !simulation.value) return
  
  const { $d3 } = useNuxtApp()
  
  // Подготовка данных для графа
  graphData.value.nodes = miniMapEvents.value.map(event => ({
    id: event.id,
    name: event.title,
    group: event.category_id,
    data: event,
    isCurrent: event.id === props.eventId
  }))
  
  graphData.value.links = miniMapConnections.value.map(conn => ({
    source: conn.source,
    target: conn.target,
    value: conn.value || 1
  }))
  
  // Очищаем существующий граф
  svg.value.select('g.mini-graph-container').selectAll('*').remove()
  
  // Получаем контейнер графа
  const graphG = svg.value.select('g.mini-graph-container')
  
  // Настраиваем центр в зависимости от размера контейнера
  const containerWidth = miniMapContainer.value.clientWidth
  const containerHeight = miniMapContainer.value.clientHeight
  const centerX = containerWidth / 2
  const centerY = containerHeight / 2
  
  // Обновляем силу центрирования
  simulation.value.force('center', $d3.forceCenter(centerX, centerY))
  
  // Добавляем связи
  const link = graphG.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(graphData.value.links)
    .join('line')
    .style('stroke', '#999')
    .style('stroke-opacity', 0.6)
    .style('stroke-width', d => Math.sqrt(d.value))
  
  // Добавляем узлы
  const node = graphG.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(graphData.value.nodes)
    .join('g')
    .attr('class', 'node')
    .attr('data-id', d => d.id)
    .on('click', (event, d) => {
      event.stopPropagation()
      // Переходим на страницу события, если это не текущее событие
      if (d.id !== props.eventId) {
        emit('navigate', d.id)
      }
    })
    .style('cursor', d => d.isCurrent ? 'default' : 'pointer')
  
  // Добавляем круги для узлов с учётом категорий
  node.append('circle')
    .attr('r', d => {
      return d.isCurrent ? 10 : 6
    })
    .style('fill', d => getCategoryColor(d.group))
    .style('stroke', d => d.isCurrent ? '#000' : '#fff')
    .style('stroke-width', d => d.isCurrent ? 2 : 1.5)
    .attr('opacity', d => {
      // Центральный узел полностью непрозрачный
      if (d.isCurrent) return 1;
      
      // Для прямых связей используем среднюю непрозрачность
      const isDirectlyConnected = miniMapConnections.value.some(conn => 
        (conn.source === props.eventId && conn.target === d.id) || 
        (conn.target === props.eventId && conn.source === d.id)
      );
      
      return isDirectlyConnected ? 0.85 : 0.6;
    })
  
  // Добавляем текст для узлов (только в развернутом режиме)
  if (isExpanded.value) {
    node.append('text')
      .text(d => d.name)
      .attr('x', 12)
      .attr('y', 4)
      .style('font-family', 'Inter, sans-serif')
      .style('font-size', '11px')
      .style('pointer-events', 'none')
      .style('opacity', d => {
        // Текст для центрального узла полностью непрозрачный
        if (d.isCurrent) return 1;
        
        // Для прямых связей используем среднюю непрозрачность
        const isDirectlyConnected = miniMapConnections.value.some(conn => 
          (conn.source === props.eventId && conn.target === d.id) || 
          (conn.target === props.eventId && conn.source === d.id)
        );
        
        return isDirectlyConnected ? 0.85 : 0.6;
      })
  }
  
  // Запускаем симуляцию с более плавной анимацией
  simulation.value
    .nodes(graphData.value.nodes)
    .force('link', $d3.forceLink(graphData.value.links).id(d => d.id))
    .on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
  
      node
        .attr('transform', d => `translate(${d.x},${d.y})`)
      
      // Сохраняем позицию центрального узла
      const centralNode = graphData.value.nodes.find(n => n.isCurrent);
      if (centralNode) {
        centralNodePosition.value = { x: centralNode.x, y: centralNode.y };
      }
    })
    .alpha(1)
    .restart()
    
  // Добавляем возможность перетаскивания узлов
  node.call($d3.drag()
    .on('start', (event, d) => {
      if (!event.active) simulation.value.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on('drag', (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
      
      // Если перетаскиваем центральный узел, обновляем его позицию
      if (d.isCurrent) {
        centralNodePosition.value = { x: d.x, y: d.y };
      }
    })
    .on('end', (event, d) => {
      if (!event.active) simulation.value.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }));
}

// Переход к полному графу при клике на заголовок
function navigateToFullGraph() {
  router.push('/graph')
}
</script>

<style scoped>
.event-mini-map {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}

.mini-map-header {
  padding: 8px 12px;
  background-color: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-bottom: none;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  transition: background-color 0.2s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  user-select: none;
}

.mini-map-header:hover {
  background-color: #e1e8f0;
}

.mini-map-title {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin: 0;
  display: flex;
  align-items: center;
}

.header-icon {
  margin-left: 6px;
  opacity: 0.7;
}

.mini-map-container {
  position: relative;
  width: 100%;
  height: 135px;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  overflow: hidden;
  background-color: #f8fafc;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.mini-map-container svg {
  cursor: grab;
}

.mini-map-container svg:active {
  cursor: grabbing;
}

.mini-map-expanded {
  height: 350px; /* Увеличиваем высоту при раскрытии (только вниз) */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 5; /* Достаточно для перекрытия стандартных элементов, но не модальных окон */
}

/* Кнопка закрытия */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 24px;
  height: 24px;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
  z-index: 6;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

/* Стили для линий связи */
.links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

/* Стили для узлов */
.nodes circle {
  transition: all 0.2s ease;
}

.nodes text {
  fill: #4a5568;
  pointer-events: none;
  user-select: none;
}

/* Стиль при наведении на узел */
.node:hover circle {
  stroke-width: 2.5px;
  filter: brightness(1.1);
}

/* Стиль при наведении на текст */
.node:hover text {
  font-weight: 500;
}
</style> 