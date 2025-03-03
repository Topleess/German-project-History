<template>
  <v-container fluid class="graph-container">
    <v-row>
      <v-col cols="12">
        <v-card class="graph-card">
          <v-card-title>
            Интерактивный граф исторических событий
          </v-card-title>
          <v-card-text>
            <div ref="graphContainer" class="graph-visualization">
              <svg width="100%" height="600"></svg>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'GraphPage',
  
  data() {
    return {
      // Тестовые данные для графа
      nodes: [
        { id: 1, name: "Первая мировая война", group: 1 },
        { id: 2, name: "Революция 1917 года", group: 1 },
        { id: 3, name: "Версальский договор", group: 2 }
      ],
      links: [
        { source: 1, target: 2, value: 1 },
        { source: 1, target: 3, value: 1 },
        { source: 2, target: 3, value: 1 }
      ]
    }
  },
  
  head() {
    return {
      title: 'Интерактивный граф - История'
    }
  },
  
  mounted() {
    this.initGraph()
  },

  methods: {
    initGraph() {
      const svg = this.$d3.select(this.$refs.graphContainer).select('svg')
      const width = svg.node().getBoundingClientRect().width
      const height = 600

      // Создаем симуляцию для графа
      const simulation = this.$d3.forceSimulation(this.nodes)
        .force('link', this.$d3.forceLink(this.links).id(d => d.id))
        .force('charge', this.$d3.forceManyBody().strength(-400))
        .force('center', this.$d3.forceCenter(width / 2, height / 2))

      // Добавляем связи
      const link = svg.append('g')
        .selectAll('line')
        .data(this.links)
        .join('line')
        .style('stroke', '#999')
        .style('stroke-opacity', 0.6)
        .style('stroke-width', d => Math.sqrt(d.value))

      // Добавляем узлы
      const node = svg.append('g')
        .selectAll('g')
        .data(this.nodes)
        .join('g')
        .call(this.drag(simulation))

      // Добавляем круги для узлов
      node.append('circle')
        .attr('r', 10)
        .style('fill', d => d.group === 1 ? '#ff7f0e' : '#1f77b4')

      // Добавляем текст
      node.append('text')
        .text(d => d.name)
        .attr('x', 15)
        .attr('y', 5)
        .style('font-family', 'Arial')
        .style('font-size', '12px')

      // Обновляем позиции при каждом тике симуляции
      simulation.on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y)

        node
          .attr('transform', d => `translate(${d.x},${d.y})`)
      })
    },

    // Функция для перетаскивания узлов
    drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart()
        event.subject.fx = event.subject.x
        event.subject.fy = event.subject.y
      }

      function dragged(event) {
        event.subject.fx = event.x
        event.subject.fy = event.y
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0)
        event.subject.fx = null
        event.subject.fy = null
      }

      return this.$d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
    }
  }
}
</script>

<style scoped>
.graph-container {
  padding: 1rem;
}
.graph-card {
  min-height: 400px;
}
.graph-visualization {
  width: 100%;
  height: 600px;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style> 