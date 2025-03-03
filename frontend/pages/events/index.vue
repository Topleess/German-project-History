<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Библиотека исторических событий
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
          @input="applyFilter"
        ></v-text-field>
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="4" md="3">
            <v-select
              v-model="selectedCategory"
              :items="categories"
              item-text="name"
              item-value="id"
              label="Категория"
              clearable
              @change="applyFilter"
            ></v-select>
          </v-col>
          
          <v-col cols="12" sm="4" md="3">
            <v-menu
              ref="startDateMenu"
              v-model="startDateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="startDateFormatted"
                  label="От"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  clearable
                  @click:clear="startDate = null; applyFilter()"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="startDate"
                @input="startDateMenu = false; applyFilter()"
              ></v-date-picker>
            </v-menu>
          </v-col>
          
          <v-col cols="12" sm="4" md="3">
            <v-menu
              ref="endDateMenu"
              v-model="endDateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="endDateFormatted"
                  label="До"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  clearable
                  @click:clear="endDate = null; applyFilter()"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="endDate"
                @input="endDateMenu = false; applyFilter()"
              ></v-date-picker>
            </v-menu>
          </v-col>
          
          <v-col cols="12" sm="12" md="3" class="d-flex align-center">
            <v-btn color="primary" @click="resetFilters">
              Сбросить фильтры
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      
      <v-data-table
        :headers="headers"
        :items="filteredEvents"
        :loading="loading"
        :items-per-page="10"
        :footer-props="{
          'items-per-page-options': [10, 25, 50, 100]
        }"
        class="elevation-1"
      >
        <template v-slot:item.category_id="{ item }">
          <v-chip
            :color="getCategoryColor(item.category_id)"
            text-color="white"
            small
          >
            {{ getCategoryName(item.category_id) }}
          </v-chip>
        </template>
        
        <template v-slot:item.date="{ item }">
          {{ formatDate(item.date) }}
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            small
            :to="`/events/${item.id}`"
          >
            <v-icon small>mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'EventsPage',
  
  data() {
    return {
      events: [],
      filteredEvents: [],
      categories: [],
      loading: true,
      search: '',
      selectedCategory: null,
      startDate: null,
      endDate: null,
      startDateMenu: false,
      endDateMenu: false,
      
      headers: [
        { text: 'Название', value: 'title', sortable: true },
        { text: 'Дата', value: 'date', sortable: true },
        { text: 'Категория', value: 'category_id', sortable: true },
        { text: 'Важность', value: 'importance', sortable: true },
        { text: 'Действия', value: 'actions', sortable: false }
      ]
    }
  },
  
  computed: {
    startDateFormatted() {
      return this.startDate ? this.formatDate(this.startDate) : ''
    },
    
    endDateFormatted() {
      return this.endDate ? this.formatDate(this.endDate) : ''
    }
  },
  
  head() {
    return {
      title: 'Библиотека событий - История'
    }
  },
  
  async mounted() {
    await this.fetchData()
  },
  
  methods: {
    async fetchData() {
      this.loading = true
      try {
        // Получаем данные о категориях
        const categoriesResponse = await this.$axios.get('/api/categories/')
        this.categories = categoriesResponse.data
        
        // Получаем данные о событиях
        const eventsResponse = await this.$axios.get('/api/events/')
        this.events = eventsResponse.data
        this.filteredEvents = [...this.events]
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error)
      } finally {
        this.loading = false
      }
    },
    
    applyFilter() {
      this.filteredEvents = this.events.filter(event => {
        // Фильтрация по поиску
        if (this.search && 
            !event.title.toLowerCase().includes(this.search.toLowerCase()) && 
            !event.description.toLowerCase().includes(this.search.toLowerCase())) {
          return false
        }
        
        // Фильтрация по категории
        if (this.selectedCategory && event.category_id !== this.selectedCategory) {
          return false
        }
        
        // Фильтрация по дате начала
        if (this.startDate) {
          const eventDate = new Date(event.date)
          const filterDate = new Date(this.startDate)
          if (eventDate < filterDate) {
            return false
          }
        }
        
        // Фильтрация по дате окончания
        if (this.endDate) {
          const eventDate = new Date(event.date)
          const filterDate = new Date(this.endDate)
          if (eventDate > filterDate) {
            return false
          }
        }
        
        return true
      })
    },
    
    resetFilters() {
      this.search = ''
      this.selectedCategory = null
      this.startDate = null
      this.endDate = null
      this.filteredEvents = [...this.events]
    },
    
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : 'Неизвестно'
    },
    
    getCategoryColor(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.color : '#3498db'
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU')
    }
  }
}
</script> 