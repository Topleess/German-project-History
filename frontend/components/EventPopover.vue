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
          
          <div v-if="event.image_url" class="mb-4 relative rounded overflow-hidden h-36">
            <img :src="event.image_url" :alt="event.title" class="w-full h-full object-cover">
          </div>
          
          <!-- Связанные события - Причины -->
          <div v-if="causeEvents.length > 0" class="mb-4">
            <h3 class="text-sm font-semibold mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
              Причины ({{ causeEvents.length }})
            </h3>
            <div class="grid gap-2">
              <div 
                v-for="cause in causeEvents" 
                :key="cause.id" 
                class="border border-gray-200 rounded-md p-2 hover:bg-gray-50 cursor-pointer transition"
                @click="$emit('select-event', cause.id)"
              >
                <div class="flex justify-between">
                  <h4 class="font-medium text-blue-600 text-sm">{{ cause.title }}</h4>
                  <span class="text-xs text-gray-500">{{ formatYear(cause.date) }}</span>
                </div>
                <p class="text-xs text-gray-600 mt-1 line-clamp-2">
                  {{ findConnectionDescription(cause.id, event.id) || 'Связано как причина' }}
                </p>
              </div>
            </div>
          </div>
          
          <!-- Связанные события - Следствия -->
          <div v-if="effectEvents.length > 0" class="mb-4">
            <h3 class="text-sm font-semibold mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
              Следствия ({{ effectEvents.length }})
            </h3>
            <div class="grid gap-2">
              <div 
                v-for="effect in effectEvents" 
                :key="effect.id" 
                class="border border-gray-200 rounded-md p-2 hover:bg-gray-50 cursor-pointer transition"
                @click="$emit('select-event', effect.id)"
              >
                <div class="flex justify-between">
                  <h4 class="font-medium text-blue-600 text-sm">{{ effect.title }}</h4>
                  <span class="text-xs text-gray-500">{{ formatYear(effect.date) }}</span>
                </div>
                <p class="text-xs text-gray-600 mt-1 line-clamp-2">
                  {{ findConnectionDescription(event.id, effect.id) || 'Привело к этому событию' }}
                </p>
              </div>
            </div>
          </div>
          
          <!-- Связанные события по другим критериям (если есть) -->
          <div v-if="relatedEvents.length > 0" class="mb-4">
            <h3 class="text-sm font-semibold mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Другие связанные события ({{ relatedEvents.length }})
            </h3>
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

// События-причины для текущего события
const causeEvents = computed(() => {
  if (!props.event || !props.connections || !props.allEvents) return []
  
  // Находим все связи, где текущее событие является эффектом (следствием)
  const causesIds = props.connections
    .filter(conn => conn.target === props.event.id)
    .map(conn => conn.source)
  
  return props.allEvents.filter(event => causesIds.includes(event.id))
})

// События-следствия для текущего события
const effectEvents = computed(() => {
  if (!props.event || !props.connections || !props.allEvents) return []
  
  // Находим все связи, где текущее событие является причиной
  const effectsIds = props.connections
    .filter(conn => conn.source === props.event.id)
    .map(conn => conn.target)
  
  return props.allEvents.filter(event => effectsIds.includes(event.id))
})

// Другие события, связанные с текущим событием (не через причину-следствие)
const relatedEvents = computed(() => {
  if (!props.event || !props.event.related_events || !props.allEvents) return []
  
  // Получаем ID всех событий-причин и событий-следствий
  const connectedIds = [...causeEvents.value.map(e => e.id), ...effectEvents.value.map(e => e.id)]
  
  // Фильтруем только те связанные события, которые не входят в причины/следствия
  return props.allEvents.filter(e => 
    props.event.related_events.includes(e.id) && 
    !connectedIds.includes(e.id) && 
    e.id !== props.event.id
  )
})

// Находит описание связи между событиями
function findConnectionDescription(sourceId, targetId) {
  if (!props.connections) return null
  
  const connection = props.connections.find(
    conn => conn.source === sourceId && conn.target === targetId
  )
  
  return connection ? connection.description : null
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric', 
    month: 'long', 
    day: 'numeric'
  });
}

function formatYear(dateString) {
  if (!dateString) return ''
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