<template>
  <div class="event-form">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Название события -->
      <div class="md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">Название события *</label>
        <Input v-model="formData.title" placeholder="Введите название события" />
        <div v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</div>
      </div>
      
      <!-- Дата начала -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Дата начала *</label>
        <Input v-model="formData.date" type="date" />
        <div v-if="errors.date" class="text-red-500 text-xs mt-1">{{ errors.date }}</div>
      </div>
      
      <!-- Дата окончания -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Дата окончания</label>
        <Input v-model="formData.end_date" type="date" />
      </div>
      
      <!-- Категория -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Категория *</label>
        <select 
          v-model="formData.category_id"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
        >
          <option value="" disabled selected>Выберите категорию</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <div v-if="errors.category_id" class="text-red-500 text-xs mt-1">{{ errors.category_id }}</div>
      </div>
      
      <!-- Местоположение -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Местоположение</label>
        <Input v-model="formData.location" placeholder="Где произошло событие" />
      </div>
      
      <!-- Значимость -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Значимость (1-5)</label>
        <div class="flex items-center">
          <span class="mr-2 text-sm text-gray-600">1</span>
          <input 
            v-model="formData.importance" 
            type="range" 
            min="1" 
            max="5" 
            step="1"
            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <span class="ml-2 text-sm text-gray-600">5</span>
          <span class="ml-3 text-sm font-semibold">{{ formData.importance }}</span>
        </div>
      </div>
      
      <!-- URL изображения -->
      <div class="md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">URL изображения</label>
        <Input v-model="formData.image_url" placeholder="https://example.com/image.jpg" />
      </div>
      
      <!-- Описание -->
      <div class="md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">Описание *</label>
        <textarea
          v-model="formData.description"
          rows="4"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          placeholder="Опишите событие подробно"
        ></textarea>
        <div v-if="errors.description" class="text-red-500 text-xs mt-1">{{ errors.description }}</div>
      </div>
      
      <!-- Секция создания связей с другими событиями -->
      <div class="md:col-span-2 mt-4">
        <h3 class="text-lg font-medium text-gray-900 mb-3">Создание связей</h3>
        <div class="space-y-3 border border-gray-300 rounded-md p-3 bg-gray-50">
          <div v-for="(connection, index) in connections" :key="index" class="grid grid-cols-1 md:grid-cols-3 gap-3 pb-3 border-b border-gray-200">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Тип связи</label>
              <select 
                v-model="connection.type"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="cause">Это событие причина</option>
                <option value="effect">Это событие следствие</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Связанное событие</label>
              <select 
                v-model="connection.event_id"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="">Выберите событие</option>
                <option 
                  v-for="event in availableEvents" 
                  :key="event.id" 
                  :value="event.id"
                >
                  {{ event.title }} ({{ formatYear(event.date) }})
                </option>
              </select>
            </div>
            <div class="flex items-end">
              <div class="flex-grow mr-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Сила связи (1-3)</label>
                <input 
                  v-model="connection.strength" 
                  type="range" 
                  min="1" 
                  max="3" 
                  step="1"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
              </div>
              <button 
                @click="removeConnection(index)"
                class="mb-2 px-2 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="md:col-span-3">
              <label class="block text-sm font-medium text-gray-700 mb-1">Описание связи</label>
              <Input 
                v-model="connection.description" 
                placeholder="Опишите как события связаны между собой"
              />
            </div>
          </div>
          <button 
            @click="addConnection"
            class="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 w-full"
          >
            Добавить новую связь
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      date: '',
      end_date: '',
      category_id: '',
      description: '',
      location: '',
      importance: 3,
      image_url: '',
      related_events: []
    })
  },
  categories: {
    type: Array,
    default: () => []
  },
  events: {
    type: Array,
    default: () => []
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  existingConnections: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['submit', 'cancel'])

// Копируем данные из props для редактирования
const formData = reactive({
  title: '',
  date: '',
  end_date: '',
  category_id: '',
  description: '',
  location: '',
  importance: 3,
  image_url: '',
  related_events: []
})

// Инициализация данных из props
function initializeFormData() {
  formData.title = props.initialData.title || '';
  formData.date = props.initialData.date ? formatDateForForm(props.initialData.date) : '';
  formData.end_date = props.initialData.end_date ? formatDateForForm(props.initialData.end_date) : '';
  formData.category_id = props.initialData.category_id || '';
  formData.description = props.initialData.description || '';
  formData.location = props.initialData.location || '';
  formData.importance = props.initialData.importance || 3;
  formData.image_url = props.initialData.image_url || '';
  formData.related_events = [...(props.initialData.related_events || [])];
}

// Форматирование даты из ISO 8601 в YYYY-MM-DD для формы
function formatDateForForm(dateString) {
  if (!dateString) return '';
  // Если это полная ISO строка (с временем), извлекаем только дату
  if (dateString.includes('T')) {
    return dateString.split('T')[0];
  }
  return dateString;
}

// Инициализация при монтировании
onMounted(() => {
  initializeFormData();
  initializeConnections();
})

// Отслеживаем изменения initialData
watch(() => props.initialData, () => {
  initializeFormData();
}, { deep: true })

// Отслеживаем изменения existingConnections
watch(() => props.existingConnections, () => {
  initializeConnections();
}, { deep: true })

// Состояние для создания связей
const connections = ref([]);
const selectedRelation = ref('')
const errors = reactive({})

// Инициализация соединений из существующих данных
function initializeConnections() {
  // Очищаем текущие соединения
  connections.value = [];
  
  if (props.isEditing && props.existingConnections && props.existingConnections.length > 0) {
    // Добавляем существующие соединения
    props.existingConnections.forEach(conn => {
      let connection = null;
      
      // Определяем тип связи и id связанного события
      if (conn.cause_id !== undefined && conn.effect_id !== undefined) {
        // Формат cause_id/effect_id
        if (conn.cause_id === props.initialData.id) {
          connection = {
            id: conn.id || null,
            type: 'cause',
            event_id: conn.effect_id,
            strength: conn.strength || conn.value || 2,
            description: conn.description || ''
          };
        } else if (conn.effect_id === props.initialData.id) {
          connection = {
            id: conn.id || null,
            type: 'effect',
            event_id: conn.cause_id,
            strength: conn.strength || conn.value || 2,
            description: conn.description || ''
          };
        }
      } else if (conn.source !== undefined && conn.target !== undefined) {
        // Формат source/target
        if (conn.source === props.initialData.id) {
          connection = {
            id: conn.id || null,
            type: 'cause',
            event_id: conn.target,
            strength: conn.strength || conn.value || 2,
            description: conn.description || ''
          };
        } else if (conn.target === props.initialData.id) {
          connection = {
            id: conn.id || null,
            type: 'effect',
            event_id: conn.source,
            strength: conn.strength || conn.value || 2,
            description: conn.description || ''
          };
        }
      }
      
      // Добавляем только те соединения, где event_id определен
      if (connection && connection.event_id) {
        connections.value.push(connection);
      }
    });
  }
  
  // Если нет существующих соединений или массив пуст, добавляем пустую форму соединения
  if (connections.value.length === 0) {
    addConnection();
  }
}

// Доступные события для создания связей
const availableEvents = computed(() => {
  // Если нет данных о событиях, возвращаем пустой массив
  if (!props.events || props.events.length === 0) {
    return []
  }
  
  // Исключаем текущее событие из списка доступных событий
  const filteredEvents = props.events.filter(event => {
    if (props.initialData && props.initialData.id) {
      return event.id !== props.initialData.id
    }
    return true
  })
  
  // Если режим создания нового события (не редактирование), показываем все события
  if (!props.isEditing) {
    return filteredEvents
  }
  
  // Если режим редактирования и есть ID текущего события
  if (props.isEditing && props.initialData && props.initialData.id) {
    // Проверяем, есть ли в connections пустые соединения (где не выбрано связанное событие)
    const hasEmptyConnections = connections.value.some(conn => !conn.event_id)
    
    // Если есть пустые соединения, возвращаем все события для возможности создания новых связей
    if (hasEmptyConnections) {
      return filteredEvents
    }
    
    // Если нет пустых соединений, то работаем только с существующими связями
    // (эта логика сохраняется от предыдущего решения)
    const eventId = props.initialData.id
    
    // Используем Set для избежания дубликатов
    const addedEventIds = new Set()
    const relatedEvents = []
    
    // 1. Добавляем события, которые уже выбраны в текущих соединениях формы
    connections.value.forEach(conn => {
      if (conn.event_id) {
        const relatedEvent = filteredEvents.find(event => event.id === conn.event_id)
        if (relatedEvent && !addedEventIds.has(relatedEvent.id)) {
          addedEventIds.add(relatedEvent.id)
          relatedEvents.push(relatedEvent)
        }
      }
    })
    
    // 2. Добавляем события из existingConnections
    if (props.existingConnections && props.existingConnections.length > 0) {
      props.existingConnections.forEach(conn => {
        let relatedEventId = null
        
        // Проверяем формат cause_id/effect_id
        if (conn.cause_id === eventId && conn.effect_id) {
          relatedEventId = conn.effect_id
        } 
        else if (conn.effect_id === eventId && conn.cause_id) {
          relatedEventId = conn.cause_id
        }
        // Проверяем формат source/target
        else if (conn.source === eventId && conn.target) {
          relatedEventId = conn.target
        }
        else if (conn.target === eventId && conn.source) {
          relatedEventId = conn.source
        }
        
        if (relatedEventId && !addedEventIds.has(relatedEventId)) {
          const relatedEvent = filteredEvents.find(event => event.id === relatedEventId)
          if (relatedEvent) {
            addedEventIds.add(relatedEventId)
            relatedEvents.push(relatedEvent)
          }
        }
      })
    }
    
    // 3. Добавляем события из related_events
    if (props.initialData.related_events && props.initialData.related_events.length > 0) {
      props.initialData.related_events.forEach(relatedId => {
        if (!addedEventIds.has(relatedId)) {
          const relatedEvent = filteredEvents.find(event => event.id === relatedId)
          if (relatedEvent) {
            addedEventIds.add(relatedId)
            relatedEvents.push(relatedEvent)
          }
        }
      })
    }
    
    return relatedEvents
  }
  
  // Если не попадает ни в одно из условий выше
  return filteredEvents
})

// Форматирование года
function formatYear(dateString) {
  if (!dateString) return ''
  // Если это полная ISO строка (с временем), извлекаем только дату
  if (dateString.includes('T')) {
    dateString = dateString.split('T')[0];
  }
  return new Date(dateString).getFullYear()
}

// Получение названия события по ID
function getEventTitle(id) {
  const event = props.events.find(e => e.id === id)
  return event ? event.title : 'Неизвестное событие'
}

// Добавление новой связи
function addConnection() {
  connections.value.push({
    type: 'cause', // по умолчанию - это событие причина
    event_id: '',
    strength: 2,
    description: ''
  })
}

// Удаление связи
function removeConnection(index) {
  connections.value.splice(index, 1)
}

// Валидация формы
function validateForm() {
  errors.title = !formData.title ? 'Название события обязательно' : ''
  errors.date = !formData.date ? 'Дата начала обязательна' : ''
  errors.category_id = !formData.category_id ? 'Категория обязательна' : ''
  errors.description = !formData.description ? 'Описание обязательно' : ''
  
  return !Object.values(errors).some(error => error)
}

// Экспорт методов для использования в родительском компоненте
defineExpose({
  formData,
  connections,
  validateForm
})
</script> 