<template>
  <div class="event-carousel relative">
    <button 
      @click="prevSlide" 
      class="absolute left-0 top-1/2 transform -translate-y-1/2 z-10 bg-white bg-opacity-75 rounded-full p-2 shadow-md hover:bg-opacity-100 focus:outline-none"
      aria-label="Предыдущий слайд"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    
    <div class="overflow-hidden">
      <div 
        class="flex transition-transform duration-500 ease-in-out" 
        :style="{ transform: `translateX(-${currentSlide * 100 / visibleSlides}%)` }"
      >
        <div 
          v-for="(event, idx) in events" 
          :key="idx" 
          :class="`w-full md:w-1/${visibleSlides} flex-shrink-0 px-2`"
        >
          <div 
            @click="handleEventClick(event)" 
            class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer h-full"
          >
            <div class="h-40 bg-gray-200 relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-t from-black to-transparent"></div>
              <div class="absolute bottom-2 left-2 right-2">
                <span 
                  class="inline-block px-2 py-1 text-xs text-white rounded-md"
                  :style="{ backgroundColor: getCategoryColor(event.category_id) }"
                >
                  {{ formatYear(event.year) }}
                </span>
                <h3 class="mt-1 text-white text-lg font-medium line-clamp-2">{{ event.title }}</h3>
              </div>
            </div>
            <div class="p-4">
              <p class="text-gray-600 text-sm line-clamp-3">{{ event.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <button 
      @click="nextSlide" 
      class="absolute right-0 top-1/2 transform -translate-y-1/2 z-10 bg-white bg-opacity-75 rounded-full p-2 shadow-md hover:bg-opacity-100 focus:outline-none"
      aria-label="Следующий слайд"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
    
    <!-- Индикаторы позиции карусели -->
    <div class="flex justify-center mt-4 gap-2">
      <button
        v-for="(_, i) in slideGroups"
        :key="i"
        @click="goToSlideGroup(i)"
        :class="[
          'w-2 h-2 rounded-full focus:outline-none transition-colors',
          currentSlideGroup === i ? 'bg-primary-600' : 'bg-gray-300 hover:bg-gray-400'
        ]"
        :aria-label="`Перейти к слайду ${i + 1}`"
      ></button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  events: {
    type: Array,
    required: true
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  interval: {
    type: Number,
    default: 5000
  }
});

const router = useRouter();
const currentSlide = ref(0);

// Адаптивное количество видимых слайдов
const visibleSlides = computed(() => {
  if (typeof window === 'undefined') return 3; // SSR fallback
  return window.innerWidth < 768 ? 1 : 3;
});

// Группы слайдов для индикаторов
const slideGroups = computed(() => {
  const totalSlides = props.events.length;
  const groupsCount = Math.ceil(totalSlides / visibleSlides.value);
  return Array.from({ length: groupsCount });
});

// Текущая группа слайдов
const currentSlideGroup = computed(() => 
  Math.floor(currentSlide.value / visibleSlides.value)
);

// Цвета для категорий событий
const categoryColors = {
  1: '#4285F4', // Политические события - синий
  2: '#EA4335', // Военные события - красный
  3: '#FBBC05', // Экономические события - желтый
  4: '#34A853', // Культурные события - зеленый
  5: '#9C27B0', // Научные открытия - фиолетовый
  6: '#FF9800', // Социальные изменения - оранжевый
  7: '#795548', // Религиозные события - коричневый
  8: '#607D8B'  // Другие события - серый
};

// Получить цвет для категории
const getCategoryColor = (categoryId) => {
  return categoryColors[categoryId] || '#607D8B';
};

// Форматирование года
const formatYear = (year) => {
  if (!year) return '';
  
  // Если год отрицательный, добавляем "до н.э."
  if (year < 0) {
    return `${Math.abs(year)} до н.э.`;
  }
  
  return year.toString();
};

// Переход к предыдущему слайду
const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--;
  } else {
    // Переход к последнему слайду при достижении начала
    currentSlide.value = Math.max(0, props.events.length - visibleSlides.value);
  }
  resetAutoplayTimer();
};

// Переход к следующему слайду
const nextSlide = () => {
  if (currentSlide.value < props.events.length - visibleSlides.value) {
    currentSlide.value++;
  } else {
    // Переход к первому слайду при достижении конца
    currentSlide.value = 0;
  }
  resetAutoplayTimer();
};

// Переход к конкретной группе слайдов
const goToSlideGroup = (groupIndex) => {
  currentSlide.value = groupIndex * visibleSlides.value;
  resetAutoplayTimer();
};

// Обработка клика по событию
const handleEventClick = (event) => {
  if (event.id) {
    router.push(`/events/${event.id}`);
  }
};

// Автоматическое переключение слайдов
let autoplayTimer = null;

const startAutoplay = () => {
  if (props.autoplay && props.events.length > visibleSlides.value) {
    stopAutoplay();
    autoplayTimer = setInterval(() => {
      nextSlide();
    }, props.interval);
  }
};

const stopAutoplay = () => {
  if (autoplayTimer) {
    clearInterval(autoplayTimer);
    autoplayTimer = null;
  }
};

const resetAutoplayTimer = () => {
  if (props.autoplay) {
    stopAutoplay();
    startAutoplay();
  }
};

// Обновление при изменении размера окна
let resizeTimeout;
const handleResize = () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    // Если текущий слайд становится больше максимально возможного,
    // корректируем его значение
    const maxSlide = Math.max(0, props.events.length - visibleSlides.value);
    if (currentSlide.value > maxSlide) {
      currentSlide.value = maxSlide;
    }
  }, 200);
};

// Следим за изменениями в списке событий
watch(() => props.events, () => {
  currentSlide.value = 0; // Сбрасываем карусель при изменении списка событий
  resetAutoplayTimer();
});

// Следим за изменениями в autoplay
watch(() => props.autoplay, (newVal) => {
  if (newVal) {
    startAutoplay();
  } else {
    stopAutoplay();
  }
});

onMounted(() => {
  if (process.client) {
    window.addEventListener('resize', handleResize);
    startAutoplay();
  }
});

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener('resize', handleResize);
    stopAutoplay();
  }
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 