<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Создание нового события</h1>
      <Button @click="router.push('/events')" variant="outline">
        Вернуться к списку
      </Button>
    </div>
    
    <Card>
      <div class="mb-4">
        <EventForm ref="eventForm" :categories="categories" :events="events" />
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
            Создание...
          </div>
          <span v-else>Создать событие</span>
        </Button>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'
import { useToast } from '~/composables/useToast'

const router = useRouter()
const toast = useToast()
const eventForm = ref(null)
const isSubmitting = ref(false)
const categories = ref([])
const events = ref([])

// Загрузка списка категорий и событий
onMounted(async () => {
  try {
    const [categoriesData, eventsData] = await Promise.all([
      useApi().get('/categories'),
      useApi().get('/events')
    ])
    
    if (categoriesData.success) {
      categories.value = categoriesData.data
    }
    
    if (eventsData.success) {
      events.value = eventsData.data
    }
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error)
    toast.error('Не удалось загрузить необходимые данные')
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
    
    // Создание события
    const response = await useApi().post('/events', { 
      event: eventData,
      connections: connections.filter(c => c.event_id) // Отправляем только связи с выбранными событиями
    });
    
    if (response.success) {
      toast.success('Событие успешно создано');
      router.push('/events');
    } else {
      toast.error('Ошибка при создании события: ' + (response.message || 'Неизвестная ошибка'));
    }
  } catch (error) {
    console.error('Ошибка при создании события:', error);
    toast.error('Ошибка при создании события: ' + (error.message || 'Неизвестная ошибка'));
  } finally {
    isSubmitting.value = false;
  }
};
</script> 