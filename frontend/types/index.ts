/**
 * Интерфейс для исторического события
 */
export interface HistoricalEvent {
  id: number
  title: string
  date: string
  end_date?: string
  category_id: number
  description: string
  location?: string
  importance?: number
  image_url?: string
  sources?: EventSource[]
  related_events?: number[]
}

/**
 * Интерфейс для источника информации
 */
export interface EventSource {
  title: string
  url: string
}

/**
 * Интерфейс для категории события
 */
export interface EventCategory {
  id: number
  name: string
  color: string
}

/**
 * Интерфейс для связи между событиями
 */
export interface EventConnection {
  source: number
  target: number
  value: number
  description?: string
}

/**
 * Интерфейс для параметров фильтрации событий
 */
export interface EventFilterParams {
  search?: string
  category_id?: number
  start_date?: string
  end_date?: string
  importance?: number
  page?: number
  per_page?: number
}

/**
 * Интерфейс для пагинированного ответа
 */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  total_pages: number
} 