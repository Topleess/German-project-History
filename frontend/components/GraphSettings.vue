<template>
  <div class="p-4 bg-white rounded-lg shadow mb-4">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-semibold text-lg">Настройки графа</h3>
      <button 
        @click="isOpen = !isOpen" 
        class="text-gray-500 hover:text-gray-700 focus:outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="isOpen ? 'transform rotate-180' : ''" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
    
    <div v-if="isOpen" class="space-y-4">
      <!-- Сила заряда (отталкивание/притяжение узлов) -->
      <div>
        <div class="flex justify-between mb-1">
          <label class="text-sm font-medium text-gray-700">Сила отталкивания узлов</label>
          <span class="text-sm text-gray-500">{{ settings.chargeStrength }}</span>
        </div>
        <input 
          type="range" 
          v-model.number="settings.chargeStrength" 
          @input="updateSettings" 
          min="-2000" 
          max="-100" 
          step="100"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Сильнее</span>
          <span>Слабее</span>
        </div>
      </div>
      
      <!-- Расстояние между связанными узлами -->
      <div>
        <div class="flex justify-between mb-1">
          <label class="text-sm font-medium text-gray-700">Расстояние между связанными узлами</label>
          <span class="text-sm text-gray-500">{{ settings.linkDistance }}</span>
        </div>
        <input 
          type="range" 
          v-model.number="settings.linkDistance" 
          @input="updateSettings" 
          min="50" 
          max="300" 
          step="10"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Ближе</span>
          <span>Дальше</span>
        </div>
      </div>
      
      <!-- Радиус коллизии (минимальное расстояние между узлами) -->
      <div>
        <div class="flex justify-between mb-1">
          <label class="text-sm font-medium text-gray-700">Минимальное расстояние между узлами</label>
          <span class="text-sm text-gray-500">{{ settings.collisionRadius }}</span>
        </div>
        <input 
          type="range" 
          v-model.number="settings.collisionRadius" 
          @input="updateSettings" 
          min="20" 
          max="100" 
          step="5"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Меньше</span>
          <span>Больше</span>
        </div>
      </div>
      
      <!-- Размер узлов -->
      <div>
        <div class="flex justify-between mb-1">
          <label class="text-sm font-medium text-gray-700">Базовый размер узлов</label>
          <span class="text-sm text-gray-500">{{ settings.nodeBaseSize }}</span>
        </div>
        <input 
          type="range" 
          v-model.number="settings.nodeBaseSize" 
          @input="updateSettings" 
          min="5" 
          max="25" 
          step="1"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Меньше</span>
          <span>Больше</span>
        </div>
      </div>
      
      <!-- Дополнительные настройки -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="inline-flex items-center">
            <input 
              type="checkbox" 
              v-model="settings.showLabels" 
              @change="updateSettings"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">Показывать подписи</span>
          </label>
        </div>
        
        <div>
          <label class="inline-flex items-center">
            <input 
              type="checkbox" 
              v-model="settings.useImportanceSize" 
              @change="updateSettings"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">Размер по значимости</span>
          </label>
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="flex justify-between pt-4 border-t">
        <button 
          @click="resetToDefault" 
          class="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded font-medium transition"
        >
          Сбросить настройки
        </button>
        
        <button 
          @click="$emit('apply-settings')" 
          class="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition"
        >
          Применить настройки
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineEmits, defineProps, watch } from 'vue'

const props = defineProps({
  initialSettings: {
    type: Object,
    default: () => ({
      chargeStrength: -100,
      linkDistance: 50,
      collisionRadius: 20,
      nodeBaseSize: 25,
      showLabels: true,
      useImportanceSize: true,
    })
  }
})

const emit = defineEmits(['update:settings', 'apply-settings'])

const isOpen = ref(false)
const settings = reactive({...props.initialSettings})

// Следит за изменениями initialSettings
watch(() => props.initialSettings, (newVal) => {
  Object.assign(settings, newVal)
}, { deep: true })

function updateSettings() {
  emit('update:settings', {...settings})
}

function resetToDefault() {
  Object.assign(settings, {
    chargeStrength: -100,
    linkDistance: 50,
    collisionRadius: 20,
    nodeBaseSize: 25,
    showLabels: true,
    useImportanceSize: true
  })
  updateSettings()
}
</script> 