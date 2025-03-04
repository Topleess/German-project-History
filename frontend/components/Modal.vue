<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <!-- Затемнение фона -->
    <div class="fixed inset-0 bg-black opacity-50" @click="$emit('close')"></div>
    
    <!-- Модальное окно -->
    <div class="flex items-center justify-center min-h-screen p-4">
      <div 
        class="relative bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] flex flex-col"
        style="animation: modalFadeIn 0.2s ease-out"
      >
        <!-- Заголовок -->
        <div class="flex justify-between items-center border-b px-6 py-4">
          <h3 class="text-xl font-semibold text-gray-900">{{ title }}</h3>
          <button 
            @click="$emit('close')" 
            class="text-gray-400 hover:text-gray-500 focus:outline-none"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Содержимое -->
        <div class="p-6 overflow-y-auto flex-grow">
          <slot></slot>
        </div>
        
        <!-- Кнопки -->
        <div class="border-t px-6 py-4 bg-gray-50 flex justify-end space-x-3 rounded-b-lg">
          <slot name="footer">
            <Button 
              variant="outline" 
              @click="$emit('close')"
            >
              Отмена
            </Button>
            <Button 
              @click="$emit('confirm')"
            >
              {{ confirmText }}
            </Button>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Модальное окно'
  },
  confirmText: {
    type: String,
    default: 'Подтвердить'
  }
})

defineEmits(['close', 'confirm'])
</script>

<style scoped>
@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 