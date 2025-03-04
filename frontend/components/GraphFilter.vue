<template>
  <div class="bg-white p-4 rounded-md shadow-sm mb-4">
    <div class="mb-4">
      <Input 
        v-model="searchQuery" 
        placeholder="Поиск событий..."
        class="w-full"
        @update:modelValue="updateFilters"
      >
        <template #prefix>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
        </template>
      </Input>
    </div>
    
    <div class="mb-4">
      <h3 class="text-sm font-medium text-gray-700 mb-2">Категории событий:</h3>
      <div class="flex flex-wrap gap-2">
        <div 
          v-for="category in categories" 
          :key="category.id"
          class="flex items-center rounded-full py-1 px-3 cursor-pointer select-none transition-all"
          :class="[
            'hover:shadow-md',
            isCategorySelected(category.id) 
              ? 'ring-2 ring-offset-1 shadow-sm' 
              : 'opacity-80'
          ]"
          :style="{
            backgroundColor: category.color,
            color: getContrastTextColor(category.color),
            ringColor: category.color,
          }"
          @click="toggleCategory(category.id)"
        >
          <span class="text-sm font-medium">{{ category.name }}</span>
        </div>
      </div>
    </div>
    
    <div class="mb-4">
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-sm font-medium text-gray-700">Временной период:</h3>
        <div class="flex items-center space-x-2 text-sm">
          <input 
            type="number" 
            v-model.number="startYear" 
            class="w-20 p-1 border rounded"
            :min="minYear"
            :max="endYear"
            @change="updateTimeRange"
          />
          <span>—</span>
          <input 
            type="number" 
            v-model.number="endYear" 
            class="w-20 p-1 border rounded"
            :min="startYear"
            :max="maxYear"
            @change="updateTimeRange"
          />
        </div>
      </div>
      <Timeline 
        :min-year="minYear"
        :max-year="maxYear"
        :initial-start-year="startYear"
        :initial-end-year="endYear"
        @update:range="updateTimeRange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Timeline from './Timeline.vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  minYear: {
    type: Number,
    required: true
  },
  maxYear: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:filters'])

const searchQuery = ref('')
const selectedCategories = ref([])
const startYear = ref(props.minYear)
const endYear = ref(props.maxYear)

function toggleCategory(categoryId) {
  const index = selectedCategories.value.indexOf(categoryId)
  if (index === -1) {
    if (selectedCategories.value.length === 0) {
      selectedCategories.value = [categoryId]
    } else {
      selectedCategories.value.push(categoryId)
    }
  } else {
    selectedCategories.value.splice(index, 1)
  }
  updateFilters()
}

function isCategorySelected(categoryId) {
  return selectedCategories.value.includes(categoryId)
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

function updateTimeRange(range) {
  if (typeof range === 'object') {
    startYear.value = range.startYear
    endYear.value = range.endYear
  }
  updateFilters()
}

function updateFilters() {
  emit('update:filters', {
    search: searchQuery.value,
    categories: selectedCategories.value.length > 0 ? selectedCategories.value : null,
    startYear: startYear.value,
    endYear: endYear.value
  })
}

// Инициализация фильтров
updateFilters()
</script> 