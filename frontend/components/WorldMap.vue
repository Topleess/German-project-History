<template>
  <div class="relative w-full h-full">
    <div ref="mapContainer" class="w-full h-full overflow-hidden"></div>
    <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-gray-50 bg-opacity-75">
      <span class="text-gray-500">Загрузка карты...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as d3 from 'd3';

const props = defineProps({
  countryData: {
    type: Object,
    default: () => ({})
  },
  height: {
    type: String,
    default: '100%'
  }
});

const emit = defineEmits(['country-selected']);

const mapContainer = ref(null);
const isLoading = ref(true);
const svg = ref(null);
const worldData = ref(null);

// Функция для рендеринга карты мира
const renderMap = async () => {
  if (!mapContainer.value) return;
  
  isLoading.value = true;
  
  try {
    // Если world data еще не загружены, загружаем их
    if (!worldData.value) {
      const response = await fetch('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson');
      worldData.value = await response.json();
    }
    
    // Получаем размеры контейнера
    const containerWidth = mapContainer.value.clientWidth;
    const containerHeight = mapContainer.value.clientHeight;
    
    // Если SVG уже создан, очищаем его
    if (svg.value) {
      d3.select(svg.value).selectAll('*').remove();
    } else {
      // Создаем SVG элемент
      svg.value = d3.select(mapContainer.value)
        .append('svg')
        .attr('width', containerWidth)
        .attr('height', containerHeight)
        .node();
    }
    
    const svgSelection = d3.select(svg.value);
    
    // Создаем проекцию
    const projection = d3.geoNaturalEarth1()
      .fitSize([containerWidth, containerHeight], worldData.value);
    
    // Создаем генератор пути
    const path = d3.geoPath().projection(projection);
    
    // Рисуем страны
    svgSelection.selectAll('path')
      .data(worldData.value.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', d => {
        // Определяем цвет заливки в зависимости от количества событий
        const countryCode = d.properties.iso_a3;
        const countryInfo = props.countryData[countryCode];
        
        if (countryInfo) {
          // Интенсивность цвета зависит от количества событий
          const intensity = Math.min(0.2 + (countryInfo.eventsCount / 150) * 0.8, 1);
          return `rgba(66, 133, 244, ${intensity})`;
        }
        return '#e2e8f0'; // Серый для стран без данных
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 0.5)
      .on('mouseover', function(event, d) {
        // Подсветка при наведении
        d3.select(this)
          .attr('fill', '#3b82f6')
          .attr('stroke-width', 1);
        
        // Отправляем событие выбора страны
        const countryCode = d.properties.iso_a3;
        const countryInfo = props.countryData[countryCode];
        
        if (countryInfo) {
          emit('country-selected', {
            code: countryCode,
            name: d.properties.name,
            ...countryInfo
          });
        }
      })
      .on('mouseout', function() {
        // Возвращаем исходный цвет
        d3.select(this)
          .attr('fill', d => {
            const countryCode = d.properties.iso_a3;
            const countryInfo = props.countryData[countryCode];
            
            if (countryInfo) {
              const intensity = Math.min(0.2 + (countryInfo.eventsCount / 150) * 0.8, 1);
              return `rgba(66, 133, 244, ${intensity})`;
            }
            return '#e2e8f0';
          })
          .attr('stroke-width', 0.5);
      })
      .on('click', function(event, d) {
        // Обработка клика по стране
        const countryCode = d.properties.iso_a3;
        const countryInfo = props.countryData[countryCode];
        
        if (countryInfo) {
          emit('country-selected', {
            code: countryCode,
            name: d.properties.name,
            ...countryInfo,
            clicked: true
          });
        }
      });
    
    isLoading.value = false;
  } catch (error) {
    console.error('Ошибка при рендеринге карты:', error);
    isLoading.value = false;
  }
};

// Перерисовка карты при изменении размеров контейнера
const handleResize = () => {
  if (mapContainer.value && svg.value) {
    const containerWidth = mapContainer.value.clientWidth;
    const containerHeight = mapContainer.value.clientHeight;
    
    d3.select(svg.value)
      .attr('width', containerWidth)
      .attr('height', containerHeight);
    
    renderMap();
  }
};

// Следим за изменениями countryData
watch(() => props.countryData, () => {
  renderMap();
}, { deep: true });

onMounted(() => {
  renderMap();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.world-map {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style> 