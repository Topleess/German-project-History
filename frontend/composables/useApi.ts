import { useRuntimeConfig } from 'nuxt/app'

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase
  
  /**
   * Выполняет GET запрос к API
   */
  const get = async <T>(url: string): Promise<T> => {
    try {
      const response = await fetch(`${baseURL}${url}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`)
      }
      
      return await response.json() as T
    } catch (error) {
      console.error(`Ошибка при выполнении GET запроса на ${url}:`, error)
      throw error
    }
  }
  
  /**
   * Выполняет POST запрос к API
   */
  const post = async <T>(url: string, data: any): Promise<T> => {
    try {
      const response = await fetch(`${baseURL}${url}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`)
      }
      
      return await response.json() as T
    } catch (error) {
      console.error(`Ошибка при выполнении POST запроса на ${url}:`, error)
      throw error
    }
  }
  
  /**
   * Выполняет PUT запрос к API
   */
  const put = async <T>(url: string, data: any): Promise<T> => {
    try {
      const response = await fetch(`${baseURL}${url}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`)
      }
      
      return await response.json() as T
    } catch (error) {
      console.error(`Ошибка при выполнении PUT запроса на ${url}:`, error)
      throw error
    }
  }
  
  /**
   * Выполняет DELETE запрос к API
   */
  const del = async <T>(url: string): Promise<T> => {
    try {
      const response = await fetch(`${baseURL}${url}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`)
      }
      
      return await response.json() as T
    } catch (error) {
      console.error(`Ошибка при выполнении DELETE запроса на ${url}:`, error)
      throw error
    }
  }
  
  return {
    get,
    post,
    put,
    del
  }
} 