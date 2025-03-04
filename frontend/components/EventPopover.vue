<template>
  <div 
    v-if="isOpen"
    class="fixed z-50 right-4 top-0 h-full flex items-center pointer-events-none"
  >
    <!-- Всплывающее окно -->
    <div 
      class="bg-white rounded-lg shadow-xl w-80 h-[600px] overflow-y-auto relative pointer-events-auto"
      style="transform-origin: right center; animation: slideIn 0.2s ease-out;"
    >
      <div v-if="!event" class="p-4 bg-red-100 text-red-600 font-medium">
        Событие не было передано
      </div>
      
      <div v-if="event" class="flex flex-col h-full">
        <div class="flex justify-between items-center p-4 border-b">
          <h2 class="text-xl font-bold">{{ event.title }}</h2>
          <button @click="close" class="hover:bg-gray-100 rounded-full p-1 focus:outline-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-4 overflow-y-auto flex-grow">
          <div class="mb-3">
            <div class="flex items-center text-sm text-gray-600 mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{{ formatDate(event.date) }} {{ event.end_date ? `— ${formatDate(event.end_date)}` : '' }}</span>
            </div>

            <div v-if="event.location" class="flex items-center text-sm text-gray-600 mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{{ event.location }}</span>
            </div>

            <div class="flex items-center mb-2">
              <span 
                class="text-xs px-2 py-1 rounded-full font-medium"
                :style="{ 
                  backgroundColor: getCategoryColor(event.category_id), 
                  color: getContrastTextColor(getCategoryColor(event.category_id))
                }"
              >
                {{ getCategoryName(event.category_id) }}
              </span>
              
              <div v-if="event.importance" class="ml-3 flex items-center">
                <span class="text-xs text-gray-600 mr-1">Значимость:</span>
                <div class="flex">
                  <svg v-for="i in 5" :key="i" xmlns="http://www.w3.org/2000/svg" 
                      class="h-3 w-3" 
                      :class="i <= event.importance ? 'text-yellow-500' : 'text-gray-300'"
                      fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.45 4.73L5.82 21 12 17.27z"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
          
          <div class="mb-4">
            <h3 class="text-sm font-semibold mb-1">Описание</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{{ event.description }}</p>
          </div>
          
          <!-- Секция связей текущего события -->
          <div v-if="causalEvents.length > 0" class="mb-4 bg-blue-50 p-3 rounded-md">
            <h3 class="text-sm font-semibold mb-2">Это событие является причиной для:</h3>
            <ul class="list-disc pl-5 space-y-1">
              <li v-for="causeEvent in causalEvents" :key="causeEvent.id" class="text-sm">
                <span class="text-blue-700 cursor-pointer" @click="$emit('select-event', causeEvent.id)">
                  {{ causeEvent.title }}
                </span>
                <span v-if="causeEvent.connection.strength" class="text-xs text-gray-500 ml-1">
                  (Сила: {{ causeEvent.connection.strength }})
                </span>
                <p v-if="causeEvent.connection.description" class="text-xs text-gray-600 italic mt-0.5">
                  "{{ causeEvent.connection.description }}"
                </p>
              </li>
            </ul>
          </div>
          
          <div v-if="effectEvents.length > 0" class="mb-4 bg-green-50 p-3 rounded-md">
            <h3 class="text-sm font-semibold mb-2">Это событие является следствием для:</h3>
            <ul class="list-disc pl-5 space-y-1">
              <li v-for="effectEvent in effectEvents" :key="effectEvent.id" class="text-sm">
                <span class="text-green-700 cursor-pointer" @click="$emit('select-event', effectEvent.id)">
                  {{ effectEvent.title }}
                </span>
                <span v-if="effectEvent.connection.strength" class="text-xs text-gray-500 ml-1">
                  (Сила: {{ effectEvent.connection.strength }})
                </span>
                <p v-if="effectEvent.connection.description" class="text-xs text-gray-600 italic mt-0.5">
                  "{{ effectEvent.connection.description }}"
                </p>
              </li>
            </ul>
          </div>
          
          <div v-if="event.image_url" class="mb-4 relative rounded overflow-hidden h-36">
            <img :src="event.image_url" :alt="event.title" class="w-full h-full object-cover">
          </div>
          
          <div v-if="relatedEvents.length > 0" class="mb-4">
            <h3 class="text-sm font-semibold mb-2">Связанные события</h3>
            <div class="grid gap-2">
              <div 
                v-for="relatedEvent in relatedEvents" 
                :key="relatedEvent.id" 
                class="border border-gray-200 rounded-md p-2 hover:bg-gray-50 cursor-pointer transition"
                @click="$emit('select-event', relatedEvent.id)"
              >
                <div class="flex justify-between">
                  <h4 class="font-medium text-blue-600 text-sm">{{ relatedEvent.title }}</h4>
                  <span class="text-xs text-gray-500">{{ formatYear(relatedEvent.date) }}</span>
                </div>
                <div v-if="relatedEvent.connection" class="mt-1 flex items-center">
                  <span 
                    class="text-xs px-1.5 py-0.5 rounded-full"
                    :class="getConnectionTypeClass(relatedEvent.connection.type)"
                  >
                    {{ getConnectionLabel(relatedEvent.connection.type, relatedEvent.id) }}
                  </span>
                  <span v-if="relatedEvent.connection.strength" class="ml-1 text-xs text-gray-500">
                    (Сила: {{ relatedEvent.connection.strength }})
                  </span>
                </div>
                <p v-if="relatedEvent.connection && relatedEvent.connection.description" 
                   class="text-xs text-gray-600 mt-1 italic">
                  "{{ relatedEvent.connection.description }}"
                </p>
                <p class="text-xs text-gray-600 mt-1 line-clamp-2">
                  {{ relatedEvent.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-t bg-gray-50 mt-auto">
          <button 
            @click="$emit('view-details', event.id)" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded text-sm font-medium transition"
          >
            Подробнее о событии
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed, watch, ref } from 'vue'

const props = defineProps({
  event: {
    type: Object,
    default: null
  },
  allEvents: {
    type: Array,
    default: () => []
  },
  isOpen: {
    type: Boolean,
    default: false
  },
  categories: {
    type: Array,
    default: () => []
  },
  connections: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'select-event', 'view-details'])

const relatedEvents = computed(() => {
  if (!props.event || !props.allEvents) return []
  
  const result = []
  const eventId = props.event.id
  
  // Получаем все связи для текущего события
  const connections = []
  props.allEvents.forEach(event => {
    // Проверяем, есть ли у события массив connections
    if (event.connections) {
      event.connections.forEach(conn => {
        if (conn.cause_id === eventId || conn.effect_id === eventId) {
          connections.push(conn)
        }
      })
    }
  })
  
  // Ищем все связи между событиями в графе
  const allGraphConnections = []
  const graphLinks = document.querySelectorAll('.graph-container .links line')
  graphLinks.forEach(link => {
    const sourceId = parseInt(link.getAttribute('data-source') || '0')
    const targetId = parseInt(link.getAttribute('data-target') || '0')
    if (sourceId === eventId || targetId === eventId) {
      allGraphConnections.push({
        source: sourceId,
        target: targetId
      })
    }
  })
  
  // Получаем связанные события и добавляем информацию о связи
  props.allEvents.forEach(event => {
    if (event.id !== eventId) {
      const connection = connections.find(conn => 
        (conn.cause_id === eventId && conn.effect_id === event.id) || 
        (conn.cause_id === event.id && conn.effect_id === eventId)
      )
      
      // Если нашли связь в наших данных, используем ее
      if (connection) {
        result.push({
          ...event,
          connection: {
            id: connection.id,
            type: connection.cause_id === eventId ? 'cause' : 'effect',
            strength: connection.strength,
            description: connection.description
          }
        })
      } 
      // Иначе ищем связь в графе
      else if (allGraphConnections.some(conn => 
        (conn.source === eventId && conn.target === event.id) || 
        (conn.source === event.id && conn.target === eventId)
      )) {
        const graphConn = allGraphConnections.find(conn => 
          (conn.source === eventId && conn.target === event.id) || 
          (conn.source === event.id && conn.target === eventId)
        )
        
        result.push({
          ...event,
          connection: {
            type: graphConn.source === eventId ? 'cause' : 'effect',
            strength: 1  // По умолчанию
          }
        })
      }
      // Или если указано в related_events
      else if (props.event.related_events && props.event.related_events.includes(event.id)) {
        result.push(event)
      }
    }
  })
  
  return result
})

// События, для которых текущее событие является причиной
const causalEvents = computed(() => {
  if (!props.event || !props.allEvents) return []
  
  const result = []
  const eventId = props.event.id
  
  // Получаем все связи, где текущее событие является причиной
  const connections = []
  
  // Ищем связи в массиве соединений
  if (props.connections && props.connections.length > 0) {
    props.connections.forEach(conn => {
      if (conn.source === eventId) {
        connections.push({
          cause_id: conn.source,
          effect_id: conn.target,
          eventId: conn.target,
          strength: conn.value || 1,
          description: conn.description
        })
      }
    })
  }
  
  // Ищем связи в самих событиях (если они есть)
  props.allEvents.forEach(event => {
    if (event.connections) {
      event.connections.forEach(conn => {
        if (conn.cause_id === eventId && conn.effect_id === event.id) {
          connections.push({...conn, eventId: event.id})
        }
      })
    }
  })
  
  // Ищем связи в DOM графа, если не нашли достаточно соединений в других источниках
  if (connections.length === 0) {
    const graphLinks = document.querySelectorAll('.graph-container .links line')
    graphLinks.forEach(link => {
      const sourceId = parseInt(link.getAttribute('data-source') || '0')
      const targetId = parseInt(link.getAttribute('data-target') || '0')
      
      if (sourceId === eventId && targetId !== 0) {
        const existingConn = connections.find(c => c.eventId === targetId)
        if (!existingConn) {
          connections.push({
            cause_id: sourceId,
            effect_id: targetId,
            eventId: targetId,
            strength: 1
          })
        }
      }
    })
  }
  
  // Добавляем связанные события в результат
  connections.forEach(conn => {
    const relatedEvent = props.allEvents.find(e => e.id === conn.eventId || e.id === conn.effect_id)
    if (relatedEvent) {
      result.push({
        ...relatedEvent,
        connection: {
          id: conn.id,
          type: 'cause',
          strength: conn.strength,
          description: conn.description
        }
      })
    }
  })
  
  return result
})

// События, для которых текущее событие является следствием
const effectEvents = computed(() => {
  if (!props.event || !props.allEvents) return []
  
  const result = []
  const eventId = props.event.id
  
  // Получаем все связи, где текущее событие является следствием
  const connections = []
  
  // Ищем связи в массиве соединений
  if (props.connections && props.connections.length > 0) {
    props.connections.forEach(conn => {
      if (conn.target === eventId) {
        connections.push({
          cause_id: conn.source,
          effect_id: conn.target,
          eventId: conn.source,
          strength: conn.value || 1,
          description: conn.description
        })
      }
    })
  }
  
  // Ищем связи в самих событиях (если они есть)
  props.allEvents.forEach(event => {
    if (event.connections) {
      event.connections.forEach(conn => {
        if (conn.cause_id === event.id && conn.effect_id === eventId) {
          connections.push({...conn, eventId: event.id})
        }
      })
    }
  })
  
  // Ищем связи в DOM графа, если не нашли достаточно соединений в других источниках
  if (connections.length === 0) {
    const graphLinks = document.querySelectorAll('.graph-container .links line')
    graphLinks.forEach(link => {
      const sourceId = parseInt(link.getAttribute('data-source') || '0')
      const targetId = parseInt(link.getAttribute('data-target') || '0')
      
      if (targetId === eventId && sourceId !== 0) {
        const existingConn = connections.find(c => c.eventId === sourceId)
        if (!existingConn) {
          connections.push({
            cause_id: sourceId,
            effect_id: targetId,
            eventId: sourceId,
            strength: 1
          })
        }
      }
    })
  }
  
  // Добавляем связанные события в результат
  connections.forEach(conn => {
    const relatedEvent = props.allEvents.find(e => e.id === conn.eventId || e.id === conn.cause_id)
    if (relatedEvent) {
      result.push({
        ...relatedEvent,
        connection: {
          id: conn.id,
          type: 'effect',
          strength: conn.strength,
          description: conn.description
        }
      })
    }
  })
  
  return result
})

function formatDate(dateString) {
  if (!dateString) return '';
  
  // Если дата содержит время (ISO 8601), извлекаем только дату
  if (dateString.includes('T')) {
    dateString = dateString.split('T')[0];
  }
  
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric', 
    month: 'long', 
    day: 'numeric'
  });
}

function formatYear(dateString) {
  if (!dateString) return ''
  
  // Если дата содержит время (ISO 8601), извлекаем только дату
  if (dateString.includes('T')) {
    dateString = dateString.split('T')[0];
  }
  
  const date = new Date(dateString)
  return date.getFullYear()
}

function getCategoryName(categoryId) {
  if (!props.categories || props.categories.length === 0) return ''
  const category = props.categories.find(c => c.id === categoryId)
  return category ? category.name : ''
}

function getCategoryColor(categoryId) {
  if (!props.categories || props.categories.length === 0) return '#cccccc'
  const category = props.categories.find(c => c.id === categoryId)
  return category ? category.color : '#cccccc'
}

function getContrastTextColor(hexColor) {
  // Если цвет не задан, возвращаем черный
  if (!hexColor) return '#000000'
  
  // Удаляем # из начала строки, если есть
  const hex = hexColor.replace('#', '')
  
  // Преобразуем hex в RGB
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)
  
  // Вычисляем яркость
  const brightness = (r * 299 + g * 587 + b * 114) / 1000
  
  // Возвращаем черный или белый в зависимости от яркости
  return brightness > 128 ? '#000000' : '#FFFFFF'
}

function getConnectionTypeClass(type) {
  return type === 'cause' 
    ? 'bg-blue-100 text-blue-800' 
    : 'bg-green-100 text-green-800'
}

function getConnectionLabel(type, relatedEventId) {
  if (type === 'cause') {
    return 'Это событие причина'
  } else {
    return 'Это событие следствие'
  }
}

function close() {
  emit('close')
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style> 