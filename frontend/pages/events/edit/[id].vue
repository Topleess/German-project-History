<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin h-10 w-10 border-4 border-primary-600 rounded-full border-t-transparent"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
      <strong class="font-bold">Ошибка!</strong>
      <span class="block sm:inline"> {{ error }}</span>
    </div>
    
    <div v-else>
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Редактирование события</h1>
        <Button @click="router.push('/events')" variant="outline">
          Вернуться к списку
        </Button>
      </div>
      
      <Card>
        <div class="mb-4">
          <EventForm 
            ref="eventForm" 
            :initial-data="event" 
            :categories="categories" 
            :events="events"
            :is-editing="true"
            :existing-connections="connections"
          />
        </div>
        
        <div class="flex justify-end space-x-3 mt-6">
          <Button variant="outline" @click="router.push('/events')">
            Отмена
          </Button>
          <Button :disabled="isSubmitting" @click="submit">
            <div v-if="isSubmitting" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Сохранение...
            </div>
            <span v-else>Сохранить изменения</span>
          </Button>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'
import { useToast } from '~/composables/useToast'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const eventId = route.params.id
const eventForm = ref(null)
const isSubmitting = ref(false)
const loading = ref(true)
const error = ref(null)
const event = ref(null)
const categories = ref([])
const events = ref([])
const connections = ref([])

// Загрузка данных события и связанных данных
onMounted(async () => {
  try {
    const [eventData, categoriesData, eventsData, connectionsData] = await Promise.all([
      useApi().get(`/events/${eventId}`),
      useApi().get('/categories'),
      useApi().get('/events'),
      useApi().get(`/events/${eventId}/connections`)
    ])
    
    if (!eventData.success || !eventData.data) {
      error.value = 'Событие не найдено'
      return
    }
    
    event.value = eventData.data
    
    if (categoriesData.success) {
      categories.value = categoriesData.data
    }
    
    if (eventsData.success) {
      // Исключаем текущее событие из списка
      events.value = eventsData.data.filter(e => e.id !== parseInt(eventId))
    }
    
    if (connectionsData.success) {
      connections.value = connectionsData.data
    }
  } catch (e) {
    console.error('Ошибка при загрузке данных:', e)
    error.value = 'Не удалось загрузить данные события'
  } finally {
    loading.value = false
  }
})

const submit = async () => {
  if (!eventForm.value.validateForm()) {
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    // Подготовка данных для отправки
    const eventData = { ...eventForm.value.formData };
    const connections = eventForm.value.connections;
    
    // Обновление события
    const response = await useApi().put(`/events/${eventId}`, { 
      event: eventData,
      connections: connections.filter(c => c.event_id) // Отправляем только связи с выбранными событиями
    });
    
    if (response.success) {
      toast.success('Событие успешно обновлено');
      router.push('/events');
    } else {
      toast.error('Ошибка при обновлении события: ' + (response.message || 'Неизвестная ошибка'));
    }
  } catch (error) {
    console.error('Ошибка при обновлении события:', error);
    toast.error('Ошибка при обновлении события: ' + (error.message || 'Неизвестная ошибка'));
  } finally {
    isSubmitting.value = false;
  }
};
</script> 