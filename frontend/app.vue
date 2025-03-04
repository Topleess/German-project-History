<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <h1 class="text-3xl font-bold tracking-tight text-gray-900 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span>(Ис-Кис)</span>
          </h1>
          <div class="flex items-center">
            <nav>
              <ul class="flex space-x-6">
                <li>
                  <NuxtLink to="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path === '/' }">
                    Главная
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/graph" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path === '/graph' }">
                    Граф событий
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/events" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path.startsWith('/events') }">
                    Библиотека событий
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/learning" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition font-medium" :class="{ 'bg-gray-100': $route.path === '/learning' }">
                    Обучение
                  </NuxtLink>
                </li>
              </ul>
            </nav>
            <div class="ml-8 flex space-x-3">
              <button 
                @click="openLoginModal" 
                class="text-primary-600 hover:text-primary-800 border border-primary-600 px-4 py-1.5 rounded-md transition-colors text-sm font-medium"
              >
                Войти
              </button>
              <button 
                @click="openRegisterModal" 
                class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-1.5 rounded-md transition-colors text-sm font-medium"
              >
                Регистрация
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
    <main>
      <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <NuxtPage />
      </div>
    </main>
    
    <!-- Модальное окно для входа -->
    <Modal
      :show="showLoginModal"
      title="Вход в систему"
      confirm-text="Войти"
      @close="closeLoginModal"
      @confirm="handleLogin"
    >
      <div class="space-y-4">
        <div>
          <label for="login-email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            id="login-email"
            v-model="loginForm.email"
            type="email"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="Ваш email"
          />
        </div>
        <div>
          <label for="login-password" class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <input
            id="login-password"
            v-model="loginForm.password"
            type="password"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="Ваш пароль"
          />
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-700">
              Запомнить меня
            </label>
          </div>
          <div class="text-sm">
            <a href="#" class="font-medium text-primary-600 hover:text-primary-500">
              Забыли пароль?
            </a>
          </div>
        </div>
        <div>
          <button 
            @click="switchToRegister" 
            class="mt-2 text-sm text-primary-600 hover:text-primary-800"
          >
            Ещё нет аккаунта? Зарегистрируйтесь
          </button>
        </div>
      </div>
    </Modal>

    <!-- Модальное окно для регистрации -->
    <Modal
      :show="showRegisterModal"
      title="Регистрация"
      confirm-text="Зарегистрироваться"
      @close="closeRegisterModal"
      @confirm="handleRegister"
    >
      <div class="space-y-4">
        <div>
          <label for="register-name" class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
          <input
            id="register-name"
            v-model="registerForm.name"
            type="text"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="Ваше имя"
          />
        </div>
        <div>
          <label for="register-email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            id="register-email"
            v-model="registerForm.email"
            type="email"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="Ваш email"
          />
        </div>
        <div>
          <label for="register-password" class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <input
            id="register-password"
            v-model="registerForm.password"
            type="password"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="Придумайте пароль"
          />
        </div>
        <div>
          <label for="register-password-confirm" class="block text-sm font-medium text-gray-700 mb-1">Подтверждение пароля</label>
          <input
            id="register-password-confirm"
            v-model="registerForm.passwordConfirm"
            type="password"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="Повторите пароль"
          />
        </div>
        <div>
          <button 
            @click="switchToLogin" 
            class="mt-2 text-sm text-primary-600 hover:text-primary-800"
          >
            Уже есть аккаунт? Войдите
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Modal from '~/components/Modal.vue';

// Состояния для модальных окон
const showLoginModal = ref(false);
const showRegisterModal = ref(false);

// Формы для входа и регистрации
const loginForm = ref({
  email: '',
  password: ''
});

const registerForm = ref({
  name: '',
  email: '',
  password: '',
  passwordConfirm: ''
});

// Функции для открытия/закрытия модальных окон
const openLoginModal = () => {
  showLoginModal.value = true;
  showRegisterModal.value = false;
};

const closeLoginModal = () => {
  showLoginModal.value = false;
};

const openRegisterModal = () => {
  showRegisterModal.value = true;
  showLoginModal.value = false;
};

const closeRegisterModal = () => {
  showRegisterModal.value = false;
};

// Переключение между модальными окнами
const switchToRegister = () => {
  closeLoginModal();
  openRegisterModal();
};

const switchToLogin = () => {
  closeRegisterModal();
  openLoginModal();
};

// Обработчики событий для формы (заглушки)
const handleLogin = () => {
  console.log('Вход в систему с данными:', loginForm.value);
  closeLoginModal();
};

const handleRegister = () => {
  console.log('Регистрация с данными:', registerForm.value);
  closeRegisterModal();
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html {
  font-family: 'Inter', sans-serif;
}

body {
  @apply antialiased text-gray-900;
}
</style> 