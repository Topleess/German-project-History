<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold">{{ isEditMode ? 'Редактирование события' : 'Создание нового события' }}</h2>
      <button 
        @click="$emit('close')" 
        class="text-gray-500 hover:text-gray-700 rounded-full p-1 focus:outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Заголовок события -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Название события *</label>
        <input 
          id="title" 
          v-model="formData.title" 
          type="text" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
          required
        />
      </div>
      
      <!-- Описание события -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Описание *</label>
        <textarea 
          id="description" 
          v-model="formData.description" 
          rows="4" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        ></textarea>
      </div>
      
      <!-- Даты -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="date" class="block text-sm font-medium text-gray-700 mb-1">Дата начала *</label>
          <input 
            id="date" 
            v-model="formData.date" 
            type="date" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label for="end_date" class="block text-sm font-medium text-gray-700 mb-1">Дата окончания</label>
          <input 
            id="end_date" 
            v-model="formData.end_date" 
            type="date" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      
      <!-- Местоположение и категория -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="location" class="block text-sm font-medium text-gray-700 mb-1">Местоположение</label>
          <input 
            id="location" 
            v-model="formData.location" 
            type="text" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700 mb-1">Категория *</label>
          <select 
            id="category" 
            v-model="formData.category_id" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="" disabled>Выберите категорию</option>
            <option 
              v-for="category in categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
      
      <!-- Значимость события -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Значимость события</label>
        <div class="flex items-center">
          <div class="flex">
            <button 
              type="button"
              v-for="i in 5" 
              :key="i" 
              @click="formData.importance = i"
              class="focus:outline-none"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                class="h-8 w-8" 
                :class="i <= formData.importance ? 'text-yellow-500' : 'text-gray-300'"
                fill="currentColor" 
                viewBox="0 0 24 24"
              >
                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.45 4.73L5.82 21 12 17.27z"/>
              </svg>
            </button>
          </div>
          <span class="ml-2 text-sm text-gray-500">{{ formData.importance }} из 5</span>
        </div>
      </div>
      
      <!-- URL изображения -->
      <div>
        <label for="image_url" class="block text-sm font-medium text-gray-700 mb-1">URL изображения</label>
        <input 
          id="image_url" 
          v-model="formData.image_url" 
          type="url" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="https://example.com/image.jpg"
        />
      </div>
      
      <!-- Связи события (только в режиме редактирования) -->
      <div v-if="isEditMode" class="border-t pt-4">
        <h3 class="text-lg font-medium mb-3">Связи события</h3>
        
        <!-- Табы для переключения между типами связей -->
        <div class="flex border-b mb-4">
          <button 
            type="button"
            class="px-4 py-2 border-b-2 font-medium text-sm"
            :class="activeTab === 'causes' 
              ? 'border-blue-500 text-blue-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'"
            @click="activeTab = 'causes'"
          >
            Причины
          </button>
          <button 
            type="button"
            class="px-4 py-2 border-b-2 font-medium text-sm"
            :class="activeTab === 'effects' 
              ? 'border-blue-500 text-blue-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700'"
            @click="activeTab = 'effects'"
          >
            Следствия
          </button>
        </div>
        
        <!-- Список причин -->
        <div v-if="activeTab === 'causes'">
          <p class="text-sm text-gray-600 mb-2">События, которые привели к данному событию:</p>
          
          <div class="space-y-3 mb-4">
            <!-- Существующие причины -->
            <div 
              v-for="(cause, index) in causeConnections" 
              :key="index"
              class="flex items-center p-2 bg-gray-50 rounded border"
            >
              <div class="flex-grow">
                <div class="font-medium">{{ getEventTitle(cause.cause_id) }}</div>
                <div class="text-sm text-gray-600">{{ cause.description || 'Нет описания' }}</div>
              </div>
              <div class="ml-2 flex items-center">
                <select 
                  v-model="cause.strength" 
                  class="mr-2 border-gray-300 rounded-md text-sm"
                >
                  <option value="1">Слабая</option>
                  <option value="2">Средняя</option>
                  <option value="3">Сильная</option>
                </select>
                <button 
                  type="button"
                  @click="removeCauseConnection(index)"
                  class="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Добавление новой причины -->
            <div class="border rounded p-3">
              <h4 class="text-sm font-medium mb-2">Добавить причину</h4>
              <div class="grid grid-cols-2 gap-2 mb-2">
                <select 
                  v-model="newCause.event_id" 
                  class="w-full px-2 py-1 border border-gray-300 rounded-md"
                >
                  <option value="" disabled>Выберите событие</option>
                  <option 
                    v-for="event in availableCauseEvents" 
                    :key="event.id" 
                    :value="event.id"
                  >
                    {{ event.title }}
                  </option>
                </select>
                <select 
                  v-model="newCause.strength" 
                  class="w-full px-2 py-1 border border-gray-300 rounded-md"
                >
                  <option value="1">Слабая связь</option>
                  <option value="2">Средняя связь</option>
                  <option value="3">Сильная связь</option>
                </select>
              </div>
              <div class="mb-2">
                <input 
                  v-model="newCause.description" 
                  placeholder="Описание связи" 
                  class="w-full px-2 py-1 border border-gray-300 rounded-md"
                />
              </div>
              <button 
                type="button"
                @click="addCauseConnection"
                :disabled="!newCause.event_id"
                class="w-full px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50"
              >
                Добавить
              </button>
            </div>
          </div>
        </div>
        
        <!-- Список следствий -->
        <div v-if="activeTab === 'effects'">
          <p class="text-sm text-gray-600 mb-2">События, к которым привело данное событие:</p>
          
          <div class="space-y-3 mb-4">
            <!-- Существующие следствия -->
            <div 
              v-for="(effect, index) in effectConnections" 
              :key="index"
              class="flex items-center p-2 bg-gray-50 rounded border"
            >
              <div class="flex-grow">
                <div class="font-medium">{{ getEventTitle(effect.effect_id) }}</div>
                <div class="text-sm text-gray-600">{{ effect.description || 'Нет описания' }}</div>
              </div>
              <div class="ml-2 flex items-center">
                <select 
                  v-model="effect.strength" 
                  class="mr-2 border-gray-300 rounded-md text-sm"
                >
                  <option value="1">Слабая</option>
                  <option value="2">Средняя</option>
                  <option value="3">Сильная</option>
                </select>
                <button 
                  type="button"
                  @click="removeEffectConnection(index)"
                  class="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Добавление нового следствия -->
            <div class="border rounded p-3">
              <h4 class="text-sm font-medium mb-2">Добавить следствие</h4>
              <div class="grid grid-cols-2 gap-2 mb-2">
                <select 
                  v-model="newEffect.event_id" 
                  class="w-full px-2 py-1 border border-gray-300 rounded-md"
                >
                  <option value="" disabled>Выберите событие</option>
                  <option 
                    v-for="event in availableEffectEvents" 
                    :key="event.id" 
                    :value="event.id"
                  >
                    {{ event.title }}
                  </option>
                </select>
                <select 
                  v-model="newEffect.strength" 
                  class="w-full px-2 py-1 border border-gray-300 rounded-md"
                >
                  <option value="1">Слабая связь</option>
                  <option value="2">Средняя связь</option>
                  <option value="3">Сильная связь</option>
                </select>
              </div>
              <div class="mb-2">
                <input 
                  v-model="newEffect.description" 
                  placeholder="Описание связи" 
                  class="w-full px-2 py-1 border border-gray-300 rounded-md"
                />
              </div>
              <button 
                type="button"
                @click="addEffectConnection"
                :disabled="!newEffect.event_id"
                class="w-full px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50"
              >
                Добавить
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="flex justify-end space-x-3 pt-4 border-t">
        <button 
          type="button" 
          @click="$emit('close')"
          class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded font-medium"
        >
          Отмена
        </button>
        <button 
          type="submit" 
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
        >
          {{ isEditMode ? 'Сохранить изменения' : 'Создать событие' }}
        </button>
      </div>
    </form>
    
    <!-- Индикатор загрузки -->
    <div 
      v-if="loading" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-4 rounded-lg shadow-lg">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500 mx-auto"></div>
        <p class="text-center mt-2">{{ loadingMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useApi } from '../composables/useApi'

const props = defineProps({
  event: {
    type: Object,
    default: null
  },
  categories: {
    type: Array,
    default: () => []
  },
  allEvents: {
    type: Array,
    default: () => []
  },
  connections: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'submit', 'submit-success'])

const { post, put, delete: apiDelete } = useApi()

// Состояние формы
const loading = ref(false)
const loadingMessage = ref('Сохранение данных...')
const isEditMode = computed(() => !!props.event)
const activeTab = ref('causes')

// Инициализация данных формы
const defaultFormData = {
  title: '',
  description: '',
  date: formatDateForInput(new Date()),
  end_date: '',
  location: '',
  category_id: '',
  importance: 1,
  image_url: ''
}

const formData = reactive({ ...defaultFormData })

// Настройка данных формы при редактировании
watch(() => props.event, (newEvent) => {
  if (newEvent) {
    Object.assign(formData, {
      ...newEvent,
      date: formatDateForInput(new Date(newEvent.date)),
      end_date: newEvent.end_date ? formatDateForInput(new Date(newEvent.end_date)) : '',
      category_id: newEvent.category_id
    })
  } else {
    Object.assign(formData, defaultFormData)
  }
}, { immediate: true })

// Связи для режима редактирования
const causeConnections = reactive([])
const effectConnections = reactive([])

// Данные для новых связей
const newCause = reactive({
  event_id: '',
  description: '',
  strength: '2'
})

const newEffect = reactive({
  event_id: '',
  description: '',
  strength: '2'
})

// Получение связей при изменении props.event или props.connections
watch([() => props.event, () => props.connections], ([newEvent, newConnections]) => {
  if (newEvent && newConnections.length > 0) {
    // Очищаем предыдущие связи
    causeConnections.splice(0, causeConnections.length)
    effectConnections.splice(0, effectConnections.length)
    
    // Заполняем связи-причины (где текущее событие - следствие)
    const causes = newConnections.filter(conn => conn.target === newEvent.id)
    causes.forEach(cause => {
      causeConnections.push({
        cause_id: cause.source,
        effect_id: newEvent.id,
        description: cause.description,
        strength: cause.value.toString()
      })
    })
    
    // Заполняем связи-следствия (где текущее событие - причина)
    const effects = newConnections.filter(conn => conn.source === newEvent.id)
    effects.forEach(effect => {
      effectConnections.push({
        cause_id: newEvent.id,
        effect_id: effect.target,
        description: effect.description,
        strength: effect.value.toString()
      })
    })
  }
}, { immediate: true })

// Вычисляемые свойства для доступных событий
const availableCauseEvents = computed(() => {
  if (!props.event) return []
  
  // Исключаем текущее событие и уже выбранные причины
  const existingCauseIds = causeConnections.map(c => c.cause_id)
  return props.allEvents.filter(e => 
    e.id !== props.event.id && 
    !existingCauseIds.includes(e.id) &&
    new Date(e.date) <= new Date(props.event.date)
  )
})

const availableEffectEvents = computed(() => {
  if (!props.event) return []
  
  // Исключаем текущее событие и уже выбранные следствия
  const existingEffectIds = effectConnections.map(e => e.effect_id)
  return props.allEvents.filter(e => 
    e.id !== props.event.id && 
    !existingEffectIds.includes(e.id) &&
    new Date(e.date) >= new Date(props.event.date)
  )
})

// Методы для работы с формой
function getEventTitle(eventId) {
  const event = props.allEvents.find(e => e.id === eventId)
  return event ? event.title : 'Неизвестное событие'
}

function formatDateForInput(date) {
  if (!date) return ''
  
  return date.toISOString().split('T')[0]
}

// Методы для работы со связями
function addCauseConnection() {
  if (!newCause.event_id) return
  
  causeConnections.push({
    cause_id: newCause.event_id,
    effect_id: props.event.id,
    description: newCause.description,
    strength: newCause.strength
  })
  
  // Сброс формы
  newCause.event_id = ''
  newCause.description = ''
  newCause.strength = '2'
}

function addEffectConnection() {
  if (!newEffect.event_id) return
  
  effectConnections.push({
    cause_id: props.event.id,
    effect_id: newEffect.event_id,
    description: newEffect.description,
    strength: newEffect.strength
  })
  
  // Сброс формы
  newEffect.event_id = ''
  newEffect.description = ''
  newEffect.strength = '2'
}

function removeCauseConnection(index) {
  causeConnections.splice(index, 1)
}

function removeEffectConnection(index) {
  effectConnections.splice(index, 1)
}

// Отправка формы
async function handleSubmit() {
  try {
    loading.value = true
    loadingMessage.value = 'Сохранение события...'
    
    let eventId = props.event?.id
    let eventData = { ...formData }
    
    // Преобразуем данные формы в правильный формат
    if (eventData.end_date === '') {
      delete eventData.end_date
    }
    
    // Убедимся, что даты в правильном формате
    if (typeof eventData.date === 'string') {
      eventData.date = new Date(eventData.date).toISOString();
    }
    
    if (eventData.end_date && typeof eventData.end_date === 'string') {
      eventData.end_date = new Date(eventData.end_date).toISOString();
    }
    
    // Убедимся, что importance - это число
    if (eventData.importance) {
      eventData.importance = Number(eventData.importance);
    }
    
    // Убедимся, что category_id - это число
    if (eventData.category_id) {
      eventData.category_id = Number(eventData.category_id);
    }
    
    console.log('Отправляемые данные:', eventData);
    
    // Создание нового события или обновление существующего
    if (isEditMode.value) {
      await put(`/api/events/${eventId}`, eventData)
    } else {
      const newEvent = await post('/api/events', eventData)
      eventId = newEvent.id
    }
    
    // Работа со связями, только если мы в режиме редактирования
    if (isEditMode.value) {
      loadingMessage.value = 'Обновление связей...'
      
      // Сначала получаем текущие связи для событий
      const currentConnections = props.connections.filter(
        conn => conn.source === eventId || conn.target === eventId
      )
      
      // Получаем ID текущих связей для последующего удаления
      const connectionIdsToKeep = []
      
      // Обрабатываем связи-причины
      for (const cause of causeConnections) {
        const connectionData = {
          cause_id: cause.cause_id,
          effect_id: cause.effect_id,
          description: cause.description,
          strength: parseInt(cause.strength)
        }
        
        // Проверяем, существует ли такая связь
        const existingConn = currentConnections.find(
          conn => conn.source === cause.cause_id && conn.target === cause.effect_id
        )
        
        if (existingConn) {
          connectionIdsToKeep.push(existingConn.id)
          // Обновляем только если данные изменились
          if (existingConn.description !== cause.description || 
              existingConn.value !== parseInt(cause.strength)) {
            await put(`/api/connections/${existingConn.id}`, connectionData)
          }
        } else {
          // Создаем новую связь
          const newConn = await post('/api/connections', connectionData)
          connectionIdsToKeep.push(newConn.id)
        }
      }
      
      // Обрабатываем связи-следствия
      for (const effect of effectConnections) {
        const connectionData = {
          cause_id: effect.cause_id,
          effect_id: effect.effect_id,
          description: effect.description,
          strength: parseInt(effect.strength)
        }
        
        // Проверяем, существует ли такая связь
        const existingConn = currentConnections.find(
          conn => conn.source === effect.cause_id && conn.target === effect.effect_id
        )
        
        if (existingConn) {
          connectionIdsToKeep.push(existingConn.id)
          // Обновляем только если данные изменились
          if (existingConn.description !== effect.description || 
              existingConn.value !== parseInt(effect.strength)) {
            await put(`/api/connections/${existingConn.id}`, connectionData)
          }
        } else {
          // Создаем новую связь
          const newConn = await post('/api/connections', connectionData)
          connectionIdsToKeep.push(newConn.id)
        }
      }
      
      // Удаляем связи, которые больше не нужны
      for (const conn of currentConnections) {
        if (!connectionIdsToKeep.includes(conn.id)) {
          await apiDelete(`/api/connections/${conn.id}`)
        }
      }
    }
    
    emit('submit-success', eventId)
  } catch (error) {
    console.error('Ошибка при сохранении данных:', error)
    alert('Не удалось сохранить данные. Пожалуйста, попробуйте еще раз.')
  } finally {
    loading.value = false
  }
}
</script> 