<template>
  <div class="fixed bottom-4 right-4 z-50 space-y-2">
    <div 
      v-for="toast in toasts" 
      :key="toast.id" 
      :class="[
        'p-4 rounded-lg shadow-lg max-w-sm transition-all duration-300 transform',
        'flex items-center justify-between',
        toastTypeClasses[toast.type] || toastTypeClasses.info
      ]"
    >
      <div class="flex items-center">
        <span v-if="toast.type === 'success'" class="mr-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
        </span>
        <span v-else-if="toast.type === 'error'" class="mr-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
        </span>
        <span v-else-if="toast.type === 'warning'" class="mr-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
        </span>
        <span v-else-if="toast.type === 'info'" class="mr-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"></path>
          </svg>
        </span>
        <p class="text-sm">{{ toast.message }}</p>
      </div>
      <button 
        class="ml-4 text-current opacity-70 hover:opacity-100 focus:outline-none"
        @click="removeToast(toast.id)"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useToast } from '~/composables/useToast'

const { toasts, remove: removeToast } = useToast()

// CSS классы для разных типов уведомлений
const toastTypeClasses = {
  success: 'bg-green-100 text-green-800 border-l-4 border-green-500',
  error: 'bg-red-100 text-red-800 border-l-4 border-red-500',
  warning: 'bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500',
  info: 'bg-blue-100 text-blue-800 border-l-4 border-blue-500'
}
</script>

<style scoped>
/* Анимация появления и исчезновения toast-уведомлений */
.toast-enter-active, .toast-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}
.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style> 