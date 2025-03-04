<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen p-4">
      <!-- Затемненный фон -->
      <div class="fixed inset-0 transition-opacity bg-black bg-opacity-50" @click="$emit('close')"></div>
      
      <!-- Модальное окно -->
      <div class="relative z-10 w-full max-w-2xl p-6 mx-auto bg-white rounded-lg shadow-xl">
        <!-- Заголовок -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold text-gray-900">{{ title }}</h3>
          <button 
            type="button"
            class="text-gray-400 hover:text-gray-600 focus:outline-none"
            @click="$emit('close')"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Содержимое модального окна -->
        <div class="mt-4">
          <slot></slot>
        </div>
        
        <!-- Кнопки действий -->
        <div v-if="hasFooter" class="flex justify-end mt-6 space-x-2">
          <slot name="footer">
            <button 
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              @click="$emit('close')"
            >
              Отмена
            </button>
            <button 
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              @click="$emit('confirm')"
            >
              Подтвердить
            </button>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Модальное окно'
  },
  hasFooter: {
    type: Boolean,
    default: true
  }
})

defineEmits(['close', 'confirm'])
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style> 