<script setup>
const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  maxVisibleButtons: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['page-change'])

const pages = computed(() => {
  if (props.totalPages <= props.maxVisibleButtons) {
    return Array.from({ length: props.totalPages }, (_, i) => i + 1)
  }
  
  const halfWay = Math.floor(props.maxVisibleButtons / 2)
  
  if (props.currentPage <= halfWay) {
    return Array.from({ length: props.maxVisibleButtons }, (_, i) => i + 1)
  }
  
  if (props.currentPage > props.totalPages - halfWay) {
    return Array.from(
      { length: props.maxVisibleButtons }, 
      (_, i) => props.totalPages - props.maxVisibleButtons + i + 1
    )
  }
  
  return Array.from(
    { length: props.maxVisibleButtons }, 
    (_, i) => props.currentPage - halfWay + i
  )
})

const changePage = (page) => {
  if (page === props.currentPage) return
  if (page < 1 || page > props.totalPages) return
  
  emit('page-change', page)
}

const isFirstPage = computed(() => props.currentPage === 1)
const isLastPage = computed(() => props.currentPage === props.totalPages)
</script>

<template>
  <div class="flex items-center justify-center space-x-1">
    <!-- Кнопка "Предыдущая" -->
    <button
      class="px-3 py-1 rounded-md text-sm font-medium"
      :class="isFirstPage ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
      :disabled="isFirstPage"
      @click="changePage(currentPage - 1)"
    >
      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    
    <!-- Кнопка "Первая страница" -->
    <button
      v-if="!pages.includes(1)"
      class="px-3 py-1 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100"
      @click="changePage(1)"
    >
      1
    </button>
    
    <!-- Многоточие в начале -->
    <span v-if="!pages.includes(1) && !pages.includes(2)" class="px-3 py-1 text-gray-500">...</span>
    
    <!-- Номера страниц -->
    <button
      v-for="page in pages"
      :key="page"
      class="px-3 py-1 rounded-md text-sm font-medium"
      :class="page === currentPage ? 'bg-primary-600 text-white' : 'text-gray-700 hover:bg-gray-100'"
      @click="changePage(page)"
    >
      {{ page }}
    </button>
    
    <!-- Многоточие в конце -->
    <span 
      v-if="!pages.includes(totalPages) && !pages.includes(totalPages - 1)" 
      class="px-3 py-1 text-gray-500"
    >...</span>
    
    <!-- Кнопка "Последняя страница" -->
    <button
      v-if="!pages.includes(totalPages)"
      class="px-3 py-1 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100"
      @click="changePage(totalPages)"
    >
      {{ totalPages }}
    </button>
    
    <!-- Кнопка "Следующая" -->
    <button
      class="px-3 py-1 rounded-md text-sm font-medium"
      :class="isLastPage ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'"
      :disabled="isLastPage"
      @click="changePage(currentPage + 1)"
    >
      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template> 