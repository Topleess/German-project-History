<template>
  <div ref="chartContainer" class="w-full h-full"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as d3 from 'd3';

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['category-selected']);
const chartContainer = ref(null);
let simulation = null;

// Функция для рендеринга bubble chart
const renderChart = () => {
  if (!chartContainer.value || !props.data || props.data.length === 0) return;
  
  // Очищаем контейнер
  d3.select(chartContainer.value).selectAll('*').remove();
  
  // Определяем размеры графика
  const width = chartContainer.value.clientWidth;
  const height = chartContainer.value.clientHeight;
  
  // Создаем SVG элемент
  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height);
  
  // Создаем simulation для размещения пузырьков
  simulation = d3.forceSimulation(props.data)
    .force('charge', d3.forceManyBody().strength(5))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => Math.sqrt(d.count) * 2 + 5))
    .on('tick', ticked);
  
  // Создаем группу для пузырьков
  const bubbles = svg.selectAll('.bubble')
    .data(props.data)
    .enter()
    .append('g')
    .attr('class', 'bubble')
    .style('cursor', 'pointer')
    .on('click', (event, d) => {
      emit('category-selected', d);
    });
  
  // Добавляем круги
  bubbles.append('circle')
    .attr('r', d => Math.sqrt(d.count) * 2)
    .attr('fill', d => d.color)
    .attr('stroke', '#fff')
    .attr('stroke-width', 1)
    .on('mouseover', function() {
      d3.select(this)
        .attr('stroke-width', 2)
        .attr('stroke', '#333');
    })
    .on('mouseout', function() {
      d3.select(this)
        .attr('stroke-width', 1)
        .attr('stroke', '#fff');
    });
  
  // Добавляем текст
  bubbles.append('text')
    .text(d => d.name)
    .attr('text-anchor', 'middle')
    .attr('font-size', d => Math.min(2 * Math.sqrt(d.count), 16))
    .attr('fill', '#fff')
    .attr('dy', '0.3em')
    .style('pointer-events', 'none');
  
  // Добавляем количество событий в категории, только для крупных пузырьков
  bubbles.filter(d => Math.sqrt(d.count) * 2 > 25)
    .append('text')
    .text(d => d.count)
    .attr('text-anchor', 'middle')
    .attr('font-size', d => Math.min(1.5 * Math.sqrt(d.count), 14))
    .attr('fill', '#fff')
    .attr('dy', '1.5em')
    .style('pointer-events', 'none');
  
  // Обновление позиций при каждом тике симуляции
  function ticked() {
    bubbles.attr('transform', d => `translate(${d.x},${d.y})`);
  }
};

// Перерисовка графика при изменении размеров контейнера
const handleResize = () => {
  renderChart();
};

// Следим за изменениями данных
watch(() => props.data, () => {
  renderChart();
}, { deep: true });

onMounted(() => {
  renderChart();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  
  // Останавливаем симуляцию при размонтировании компонента
  if (simulation) {
    simulation.stop();
  }
});
</script>

<style scoped>
/* Дополнительные стили, если нужны */
</style> 