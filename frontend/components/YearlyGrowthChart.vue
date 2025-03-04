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

const chartContainer = ref(null);

// Функция для рендеринга графика
const renderChart = () => {
  if (!chartContainer.value || !props.data || props.data.length === 0) return;
  
  // Очищаем контейнер
  d3.select(chartContainer.value).selectAll('*').remove();
  
  // Определяем размеры графика
  const width = chartContainer.value.clientWidth;
  const height = chartContainer.value.clientHeight;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Создаем SVG элемент
  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height);
  
  // Создаем группу с отступами
  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);
  
  // Определяем шкалы
  const xScale = d3.scaleBand()
    .domain(props.data.map(d => d.year))
    .range([0, innerWidth])
    .padding(0.1);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(props.data, d => d.count) * 1.1])
    .range([innerHeight, 0]);
  
  // Рисуем оси
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale))
    .selectAll('text')
    .style('text-anchor', 'end')
    .attr('dx', '-.8em')
    .attr('dy', '.15em')
    .attr('transform', 'rotate(-45)');
  
  g.append('g')
    .call(d3.axisLeft(yScale));
  
  // Добавляем подписи осей
  g.append('text')
    .attr('text-anchor', 'middle')
    .attr('x', innerWidth / 2)
    .attr('y', innerHeight + margin.bottom - 5)
    .text('Год')
    .attr('fill', '#4B5563')
    .attr('font-size', '12px');
  
  g.append('text')
    .attr('text-anchor', 'middle')
    .attr('transform', 'rotate(-90)')
    .attr('y', -margin.left + 12)
    .attr('x', -innerHeight / 2)
    .text('Количество событий')
    .attr('fill', '#4B5563')
    .attr('font-size', '12px');
  
  // Рисуем линию графика
  const line = d3.line()
    .x(d => xScale(d.year) + xScale.bandwidth() / 2)
    .y(d => yScale(d.count))
    .curve(d3.curveMonotoneX);
  
  g.append('path')
    .datum(props.data)
    .attr('fill', 'none')
    .attr('stroke', '#4285F4')
    .attr('stroke-width', 2)
    .attr('d', line);
  
  // Создаем группу для интерактивных точек
  const points = g.selectAll('.data-point')
    .data(props.data)
    .enter()
    .append('g')
    .attr('class', 'data-point')
    .attr('transform', d => `translate(${xScale(d.year) + xScale.bandwidth() / 2},${yScale(d.count)})`);
  
  // Добавляем точки на линии
  points.append('circle')
    .attr('r', 4)
    .attr('fill', '#4285F4')
    .style('cursor', 'pointer')
    .on('mouseover', function(event, d) {
      d3.select(this).attr('r', 6);
      
      // Показываем всплывающую подсказку
      tooltip
        .style('opacity', 1)
        .html(`<strong>${d.year}</strong>: ${d.count} событий`)
        .style('left', `${event.pageX + 10}px`)
        .style('top', `${event.pageY - 20}px`);
    })
    .on('mouseout', function() {
      d3.select(this).attr('r', 4);
      tooltip.style('opacity', 0);
    });
  
  // Создаем всплывающую подсказку
  const tooltip = d3.select(chartContainer.value)
    .append('div')
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('background-color', 'rgba(0, 0, 0, 0.8)')
    .style('color', 'white')
    .style('padding', '5px')
    .style('border-radius', '4px')
    .style('font-size', '12px')
    .style('pointer-events', 'none')
    .style('opacity', 0);
  
  // Опциональный градиент под линией
  const defs = svg.append('defs');
  
  const gradient = defs.append('linearGradient')
    .attr('id', 'area-gradient')
    .attr('x1', '0%')
    .attr('y1', '0%')
    .attr('x2', '0%')
    .attr('y2', '100%');
  
  gradient.append('stop')
    .attr('offset', '0%')
    .attr('stop-color', '#4285F4')
    .attr('stop-opacity', 0.5);
  
  gradient.append('stop')
    .attr('offset', '100%')
    .attr('stop-color', '#4285F4')
    .attr('stop-opacity', 0);
  
  // Рисуем область под линией с градиентом
  const area = d3.area()
    .x(d => xScale(d.year) + xScale.bandwidth() / 2)
    .y0(innerHeight)
    .y1(d => yScale(d.count))
    .curve(d3.curveMonotoneX);
  
  g.append('path')
    .datum(props.data)
    .attr('fill', 'url(#area-gradient)')
    .attr('d', area);
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
});
</script>

<style scoped>
.tooltip {
  transition: opacity 0.3s;
  z-index: 10;
}
</style> 