<template>
  <v-container>
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
    
    <template v-else-if="event">
      <v-row>
        <v-col cols="12">
          <v-btn color="primary" text @click="$router.go(-1)">
            <v-icon left>mdi-arrow-left</v-icon> Назад
          </v-btn>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="headline">
              {{ event.title }}
              <v-chip 
                class="ml-2" 
                :color="getCategoryColor(event.category_id)" 
                text-color="white"
              >
                {{ getCategoryName(event.category_id) }}
              </v-chip>
            </v-card-title>
            
            <v-card-subtitle>
              {{ formatDate(event.date) }}
              <span v-if="event.end_date"> - {{ formatDate(event.end_date) }}</span>
              <span v-if="event.location"> • {{ event.location }}</span>
            </v-card-subtitle>
            
            <v-card-text class="event-description">
              <div v-if="event.image_url" class="mb-4">
                <v-img
                  :src="event.image_url"
                  max-height="400"
                  contain
                ></v-img>
              </div>
              
              <div class="text-body-1">{{ event.description }}</div>
            </v-card-text>
          </v-card>
          
          <!-- Связи события -->
          <v-card class="mt-4">
            <v-card-title>Причинно-следственные связи</v-card-title>
            <v-card-text>
              <v-tabs>
                <v-tab>
                  <v-icon left>mdi-arrow-left</v-icon>
                  Причины ({{ event.causes.length }})
                </v-tab>
                <v-tab>
                  <v-icon left>mdi-arrow-right</v-icon>
                  Следствия ({{ event.effects.length }})
                </v-tab>
                
                <v-tab-item>
                  <v-list v-if="event.causes.length > 0">
                    <v-list-item
                      v-for="cause in event.causes"
                      :key="cause.id"
                      :to="`/events/${cause.cause_id}`"
                    >
                      <v-list-item-content>
                        <v-list-item-title>{{ getCauseTitle(cause.cause_id) }}</v-list-item-title>
                        <v-list-item-subtitle v-if="cause.description">{{ cause.description }}</v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-icon>
                        <v-icon>mdi-arrow-right</v-icon>
                      </v-list-item-icon>
                    </v-list-item>
                  </v-list>
                  <v-alert v-else type="info" class="mt-3">
                    Для этого события не указаны причины
                  </v-alert>
                </v-tab-item>
                
                <v-tab-item>
                  <v-list v-if="event.effects.length > 0">
                    <v-list-item
                      v-for="effect in event.effects"
                      :key="effect.id"
                      :to="`/events/${effect.effect_id}`"
                    >
                      <v-list-item-content>
                        <v-list-item-title>{{ getEffectTitle(effect.effect_id) }}</v-list-item-title>
                        <v-list-item-subtitle v-if="effect.description">{{ effect.description }}</v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-icon>
                        <v-icon>mdi-arrow-right</v-icon>
                      </v-list-item-icon>
                    </v-list-item>
                  </v-list>
                  <v-alert v-else type="info" class="mt-3">
                    Для этого события не указаны следствия
                  </v-alert>
                </v-tab-item>
              </v-tabs>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="12" md="4">
          <!-- Мини-граф связей события -->
          <v-card>
            <v-card-title>Визуализация связей</v-card-title>
            <v-card-text>
              <div ref="miniGraph" class="mini-graph"></div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text :to="`/graph?focus=${event.id}`">
                Открыть в полном графе
                <v-icon right>mdi-open-in-new</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
          
          <!-- Метаданные события -->
          <v-card class="mt-4">
            <v-card-title>Информация</v-card-title>
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Создано</v-list-item-subtitle>
                  <v-list-item-title>{{ formatDateTime(event.created_at) }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Обновлено</v-list-item-subtitle>
                  <v-list-item-title>{{ formatDateTime(event.updated_at) }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Важность</v-list-item-subtitle>
                  <v-list-item-title>
                    <v-rating
                      :value="event.importance"
                      readonly
                      dense
                      color="amber"
                      background-color="grey lighten-1"
                      half-increments
                      size="18"
                    ></v-rating>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </template>
    
    <v-alert v-else type="error">
      Событие не найдено
    </v-alert>
  </v-container>
</template>

<script>
export default {
  name: 'EventDetailPage',
  
  data() {
    return {
      event: null,
      events: [],
      categories: [],
      loading: true,
      network: null
    }
  },
  
  head() {
    return {
      title: this.event ? `${this.event.title} - История` : 'Событие - История'
    }
  },
  
  async mounted() {
    await this.fetchData()
    if (this.event) {
      this.$nextTick(() => {
        this.initMiniGraph()
      })
    }
  },
  
  methods: {
    async fetchData() {
      this.loading = true
      try {
        // Получаем данные о категориях
        const categoriesResponse = await this.$axios.get('/api/categories/')
        this.categories = categoriesResponse.data
        
        // Получаем данные о всех событиях (для связей)
        const eventsResponse = await this.$axios.get('/api/events/')
        this.events = eventsResponse.data
        
        // Получаем данные о конкретном событии
        const eventId = this.$route.params.id
        const eventResponse = await this.$axios.get(`/api/events/${eventId}`)
        this.event = eventResponse.data
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error)
        this.event = null
      } finally {
        this.loading = false
      }
    },
    
    initMiniGraph() {
      if (!this.$refs.miniGraph) return
      
      const nodes = []
      const edges = []
      
      // Добавляем центральное событие
      const category = this.categories.find(c => c.id === this.event.category_id)
      nodes.push({
        id: this.event.id,
        label: this.event.title,
        color: category ? category.color : '#3498db',
        size: 25,
        shape: 'dot',
        font: { size: 12 }
      })
      
      // Добавляем причины
      if (this.event.causes && this.event.causes.length) {
        this.event.causes.forEach(cause => {
          const causeEvent = this.events.find(e => e.id === cause.cause_id)
          if (causeEvent) {
            const causeCategory = this.categories.find(c => c.id === causeEvent.category_id)
            nodes.push({
              id: causeEvent.id,
              label: causeEvent.title,
              color: causeCategory ? causeCategory.color : '#3498db',
              size: 20,
              shape: 'dot',
              font: { size: 10 }
            })
            
            edges.push({
              from: causeEvent.id,
              to: this.event.id,
              arrows: { to: true },
              title: cause.description || '',
              width: cause.strength || 1
            })
          }
        })
      }
      
      // Добавляем следствия
      if (this.event.effects && this.event.effects.length) {
        this.event.effects.forEach(effect => {
          const effectEvent = this.events.find(e => e.id === effect.effect_id)
          if (effectEvent) {
            const effectCategory = this.categories.find(c => c.id === effectEvent.category_id)
            nodes.push({
              id: effectEvent.id,
              label: effectEvent.title,
              color: effectCategory ? effectCategory.color : '#3498db',
              size: 20,
              shape: 'dot',
              font: { size: 10 }
            })
            
            edges.push({
              from: this.event.id,
              to: effectEvent.id,
              arrows: { to: true },
              title: effect.description || '',
              width: effect.strength || 1
            })
          }
        })
      }
      
      // Настройки графа
      const options = {
        height: '300px',
        nodes: {
          borderWidth: 2,
          shadow: true
        },
        edges: {
          width: 2,
          shadow: true
        },
        physics: {
          stabilization: true,
          barnesHut: {
            gravitationalConstant: -2000,
            springConstant: 0.04,
            springLength: 95
          }
        },
        interaction: {
          navigationButtons: true,
          keyboard: true,
          tooltipDelay: 300
        }
      }
      
      // Создаем граф
      const container = this.$refs.miniGraph
      const data = { nodes, edges }
      
      this.network = new this.$visNetwork(container, data, options)
      
      // Обработчик клика
      this.network.on('click', params => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0]
          if (nodeId !== this.event.id) {
            this.$router.push(`/events/${nodeId}`)
          }
        }
      })
    },
    
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : 'Неизвестно'
    },
    
    getCategoryColor(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.color : '#3498db'
    },
    
    getCauseTitle(causeId) {
      const event = this.events.find(e => e.id === causeId)
      return event ? event.title : 'Неизвестное событие'
    },
    
    getEffectTitle(effectId) {
      const event = this.events.find(e => e.id === effectId)
      return event ? event.title : 'Неизвестное событие'
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU')
    },
    
    formatDateTime(dateString) {
      const date = new Date(dateString)
      return `${date.toLocaleDateString('ru-RU')} ${date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}`
    }
  }
}
</script>

<style scoped>
.event-description {
  font-size: 1.1rem;
  line-height: 1.6;
}

.mini-graph {
  width: 100%;
  height: 300px;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style> 