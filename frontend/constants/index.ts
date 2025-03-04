import { EventCategory } from '~/types'

/**
 * Категории исторических событий
 */
export const EVENT_CATEGORIES: EventCategory[] = [
  { id: 1, name: 'Политические', color: 'bg-blue-500' },
  { id: 2, name: 'Военные', color: 'bg-red-500' },
  { id: 3, name: 'Экономические', color: 'bg-green-500' },
  { id: 4, name: 'Культурные', color: 'bg-purple-500' },
  { id: 5, name: 'Социальные', color: 'bg-yellow-500' }
]

/**
 * Варианты количества элементов на странице
 */
export const PER_PAGE_OPTIONS = [10, 20, 50, 100]

/**
 * Значения важности событий
 */
export const IMPORTANCE_LEVELS = [
  { value: 1, label: 'Низкая' },
  { value: 2, label: 'Ниже среднего' },
  { value: 3, label: 'Средняя' },
  { value: 4, label: 'Выше среднего' },
  { value: 5, label: 'Высокая' }
]

/**
 * API пути
 */
export const API_ROUTES = {
  EVENTS: '/events',
  CATEGORIES: '/categories',
  CONNECTIONS: '/connections'
} 