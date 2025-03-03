<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="headline">
            Интерактивная образовательная платформа по истории
          </v-card-title>
          <v-card-text>
            <p>Добро пожаловать в образовательную платформу, где вы можете изучать исторические события и их взаимосвязи.</p>
            <p>Платформа предлагает следующие возможности:</p>
            <ul>
              <li>Интерактивные графы событий с причинно-следственными связями</li>
              <li>Категоризация событий по типам с цветовой кодировкой</li>
              <li>Детальная информация о каждом историческом событии</li>
              <li>Режимы "Лекция" и "Презентация" для обучения</li>
              <li>Библиотечный (списковый) режим для удобного просмотра</li>
            </ul>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" to="/graph">
              Интерактивный граф
            </v-btn>
            <v-btn color="secondary" to="/events">
              Библиотека событий
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
  head() {
    return {
      title: 'Главная - Интерактивная образовательная платформа по истории'
    }
  }
}
</script>

<style scoped>
.headline {
  text-align: center;
}
</style> 