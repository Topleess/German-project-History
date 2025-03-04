<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-2">
      <div class="text-sm font-medium">{{ formatYear(minYear) }}</div>
      <div class="text-sm font-medium">{{ formatYear(maxYear) }}</div>
    </div>

    <div class="relative h-12">
      <!-- Линия шкалы -->
      <div class="absolute top-6 left-0 right-0 h-1 bg-gray-300 rounded"></div>
      
      <!-- Отметки -->
      <div 
        v-for="year in timelineMarks" 
        :key="year" 
        class="absolute top-4 w-0.5 h-5 bg-gray-400"
        :style="{ left: `${getPositionPercentage(year)}%` }"
      >
        <div 
          class="absolute -left-6 -top-7 w-12 text-center text-xs"
          :class="{ 'font-bold': isMajorMark(year) }"
        >
          {{ formatYear(year) }}
        </div>
      </div>
      
      <!-- Ползунок начальной даты -->
      <div 
        class="absolute top-3 w-4 h-7 bg-blue-500 hover:bg-blue-600 rounded cursor-pointer transform -translate-x-1/2 transition-colors shadow-md z-10"
        :style="{ left: `${getPositionPercentage(selectedStartYear)}%` }"
        @mousedown="startDrag('start', $event)"
        @touchstart="startDrag('start', $event)"
      ></div>
      
      <!-- Ползунок конечной даты -->
      <div 
        class="absolute top-3 w-4 h-7 bg-blue-500 hover:bg-blue-600 rounded cursor-pointer transform -translate-x-1/2 transition-colors shadow-md z-10"
        :style="{ left: `${getPositionPercentage(selectedEndYear)}%` }"
        @mousedown="startDrag('end', $event)"
        @touchstart="startDrag('end', $event)"
      ></div>
      
      <!-- Выделенный диапазон -->
      <div 
        class="absolute top-6 h-1 bg-blue-500 rounded transition-all"
        :style="{ 
          left: `${getPositionPercentage(selectedStartYear)}%`,
          width: `${getPositionPercentage(selectedEndYear) - getPositionPercentage(selectedStartYear)}%`
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  minYear: {
    type: Number,
    required: true
  },
  maxYear: {
    type: Number,
    required: true
  },
  initialStartYear: {
    type: Number,
    default: null
  },
  initialEndYear: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update:range'])

const selectedStartYear = ref(props.initialStartYear || props.minYear)
const selectedEndYear = ref(props.initialEndYear || props.maxYear)
const dragging = ref(null)
const containerRef = ref(null)

// Отслеживаем изменения props и обновляем значения
watch(() => props.initialStartYear, (newVal) => {
  if (newVal !== null && newVal !== selectedStartYear.value) {
    selectedStartYear.value = newVal
  }
}, { immediate: true })

watch(() => props.initialEndYear, (newVal) => {
  if (newVal !== null && newVal !== selectedEndYear.value) {
    selectedEndYear.value = newVal
  }
}, { immediate: true })

// Расчет отметок временной шкалы
const timelineMarks = computed(() => {
  const marks = []
  const range = props.maxYear - props.minYear
  const majorStep = calculateMajorStep(range)
  
  for (let year = Math.ceil(props.minYear / majorStep) * majorStep; year <= props.maxYear; year += majorStep) {
    marks.push(year)
  }
  
  return marks
})

function calculateMajorStep(range) {
  if (range <= 30) return 5
  if (range <= 60) return 10
  if (range <= 150) return 20
  if (range <= 300) return 50
  if (range <= 1000) return 100
  return 200
}

function isMajorMark(year) {
  return year % 50 === 0
}

function formatYear(year) {
  if (year < 0) {
    return `${Math.abs(year)} до н.э.`
  }
  return `${year} г.`
}

function getPositionPercentage(year) {
  const range = props.maxYear - props.minYear
  return ((year - props.minYear) / range) * 100
}

function startDrag(handle, event) {
  if (event.type.startsWith('touch')) {
    event.preventDefault()
    event.clientX = event.touches[0].clientX
  }
  
  dragging.value = handle
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('touchmove', handleDragTouch, { passive: false })
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchend', stopDrag)
  
  // Запоминаем контейнер для расчета позиции
  containerRef.value = event.currentTarget.parentElement
}

function handleDrag(event) {
  if (!dragging.value) return
  
  const sliderRect = containerRef.value.getBoundingClientRect()
  updateSliderPosition(event.clientX, sliderRect)
}

function handleDragTouch(event) {
  if (!dragging.value) return
  
  event.preventDefault()
  const sliderRect = containerRef.value.getBoundingClientRect()
  updateSliderPosition(event.touches[0].clientX, sliderRect)
}

function updateSliderPosition(clientX, sliderRect) {
  const percentage = Math.max(0, Math.min(100, ((clientX - sliderRect.left) / sliderRect.width) * 100))
  const range = props.maxYear - props.minYear
  const year = Math.round(props.minYear + (percentage / 100) * range)
  
  if (dragging.value === 'start') {
    selectedStartYear.value = Math.min(year, selectedEndYear.value)
  } else {
    selectedEndYear.value = Math.max(year, selectedStartYear.value)
  }
  
  emit('update:range', { 
    startYear: selectedStartYear.value,
    endYear: selectedEndYear.value
  })
}

function stopDrag() {
  dragging.value = null
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('touchmove', handleDragTouch)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchend', stopDrag)
}

onMounted(() => {
  emit('update:range', { 
    startYear: selectedStartYear.value,
    endYear: selectedEndYear.value
  })
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('touchmove', handleDragTouch)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchend', stopDrag)
})
</script> 