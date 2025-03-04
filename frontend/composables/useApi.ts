import { ref } from 'vue'
import { useRuntimeConfig } from 'nuxt/app'

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase
  const loading = ref(false)
  
  /**
   * Функция для форматирования даты для API
   * @param dateString строка с датой в формате YYYY-MM-DD
   * @returns строка с датой в формате ISO8601
   */
  const formatDateForApi = (dateString: string): string => {
    if (!dateString) return '';
    
    // Проверяем, что дата в формате YYYY-MM-DD
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
      // Добавляем время, чтобы получить полный ISO формат
      return `${dateString}T00:00:00`;
    }
    
    return dateString;
  }
  
  /**
   * Функция для форматирования данных события перед отправкой на сервер
   * @param data объект с данными события
   * @returns отформатированный объект
   */
  const formatDataForApi = (data: any): any => {
    if (!data) return data;
    
    // Копируем объект, чтобы не изменять исходный
    const formattedData = { ...data };
    
    // Если это объект с событием и связями
    if (formattedData.event) {
      // Форматируем даты события
      if (formattedData.event.date) {
        formattedData.event.date = formatDateForApi(formattedData.event.date);
      }
      
      if (formattedData.event.end_date) {
        formattedData.event.end_date = formatDateForApi(formattedData.event.end_date);
      } else if (formattedData.event.end_date === '') {
        formattedData.event.end_date = null;
      }
    } 
    // Если это просто объект события
    else {
      // Форматируем даты
      if (formattedData.date) {
        formattedData.date = formatDateForApi(formattedData.date);
      }
      
      if (formattedData.end_date) {
        formattedData.end_date = formatDateForApi(formattedData.end_date);
      } else if (formattedData.end_date === '') {
        formattedData.end_date = null;
      }
    }
    
    return formattedData;
  }
  
  /**
   * Выполняет GET запрос к API
   */
  const get = async <T>(url: string): Promise<T> => {
    loading.value = true;
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
    } finally {
      loading.value = false;
    }
  }
  
  /**
   * Выполняет POST запрос к API
   */
  const post = async <T>(url: string, data: any): Promise<T> => {
    loading.value = true;
    try {
      // Форматируем данные перед отправкой
      const formattedData = formatDataForApi(data);
      
      console.log('POST запрос на ' + url, formattedData);
      
      const response = await fetch(`${baseURL}${url}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedData),
      })
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Ошибка HTTP: ${response.status}`, errorText);
        throw new Error(`Ошибка HTTP: ${response.status} - ${errorText}`);
      }
      
      return await response.json() as T
    } catch (error) {
      console.error(`Ошибка при выполнении POST запроса на ${url}:`, error)
      throw error
    } finally {
      loading.value = false;
    }
  }
  
  /**
   * Выполняет PUT запрос к API
   */
  const put = async <T>(url: string, data: any): Promise<T> => {
    loading.value = true;
    try {
      // Форматируем данные перед отправкой
      const formattedData = formatDataForApi(data);
      
      console.log('PUT запрос на ' + url, formattedData);
      
      const response = await fetch(`${baseURL}${url}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedData),
      })
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Ошибка HTTP: ${response.status}`, errorText);
        throw new Error(`Ошибка HTTP: ${response.status} - ${errorText}`);
      }
      
      return await response.json() as T
    } catch (error) {
      console.error(`Ошибка при выполнении PUT запроса на ${url}:`, error)
      throw error
    } finally {
      loading.value = false;
    }
  }
  
  /**
   * Выполняет DELETE запрос к API
   */
  const del = async <T>(url: string): Promise<T> => {
    loading.value = true;
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
    } finally {
      loading.value = false;
    }
  }
  
  return {
    get,
    post,
    put,
    del,
    loading,
  }
} 