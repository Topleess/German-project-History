import { ref, reactive } from 'vue'

interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
  timeout: number
}

// Создаем состояние для уведомлений
const toasts = reactive<Toast[]>([])
let toastCounter = 0

export function useToast() {
  const defaultTimeout = 5000 // 5 секунд по умолчанию
  
  // Добавление нового уведомления
  const add = (message: string, type: Toast['type'] = 'info', timeout: number = defaultTimeout) => {
    const id = ++toastCounter
    
    // Добавляем уведомление в массив
    toasts.push({
      id,
      message,
      type,
      timeout
    })
    
    // Автоматически удаляем уведомление после истечения таймаута
    if (timeout > 0) {
      setTimeout(() => {
        remove(id)
      }, timeout)
    }
    
    return id
  }
  
  // Удаление уведомления по ID
  const remove = (id: number) => {
    const index = toasts.findIndex(toast => toast.id === id)
    if (index !== -1) {
      toasts.splice(index, 1)
    }
  }
  
  // Специализированные методы для разных типов уведомлений
  const success = (message: string, timeout: number = defaultTimeout) => {
    return add(message, 'success', timeout)
  }
  
  const error = (message: string, timeout: number = defaultTimeout) => {
    return add(message, 'error', timeout)
  }
  
  const warning = (message: string, timeout: number = defaultTimeout) => {
    return add(message, 'warning', timeout)
  }
  
  const info = (message: string, timeout: number = defaultTimeout) => {
    return add(message, 'info', timeout)
  }
  
  return {
    toasts, // Реактивный массив уведомлений
    add,    // Общий метод добавления
    remove, // Метод удаления
    success,
    error,
    warning,
    info
  }
} 