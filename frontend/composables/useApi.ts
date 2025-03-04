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

  /**
   * Получает список всех исторических событий
   */
  const getAllEvents = async () => {
    try {
      // Если API-endpoint еще не реализован, возвращаем тестовые данные
      /*return [
        {
          id: 1,
          title: "Начало Первой мировой войны",
          description: "Военный конфликт с участием 38 государств, один из самых масштабных и кровопролитных в истории человечества.",
          date: "1914-07-28",
          end_date: "1918-11-11",
          year: 1914,
          importance: 10,
          location: "Европа",
          category_id: 2
        },
        {
          id: 2,
          title: "Октябрьская революция",
          description: "Вооружённое восстание, организованное партией большевиков в Петрограде 25 октября (7 ноября) 1917 года.",
          date: "1917-11-07",
          year: 1917,
          importance: 9,
          location: "Россия",
          category_id: 1
        },
        // Другие примеры событий...
      ];*/
      
      return await get<any[]>('/events');
    } catch (error) {
      console.error('Ошибка при получении списка событий:', error);
      // Возвращаем пустой массив в случае ошибки
      return [];
    }
  };

  /**
   * Получает список стран с количеством событий в каждой
   */
  const getCountries = async () => {
    try {
      // Если API-endpoint еще не реализован, возвращаем тестовые данные
      return [
        { code: "RUS", name: "Россия", count: 120 },
        { code: "USA", name: "США", count: 85 },
        { code: "FRA", name: "Франция", count: 65 },
        { code: "DEU", name: "Германия", count: 75 },
        { code: "GBR", name: "Великобритания", count: 68 }
      ];
      
      // Раскомментируйте, когда будет готов API endpoint
      // return await get<any[]>('/countries/events-count');
    } catch (error) {
      console.error('Ошибка при получении списка стран:', error);
      // Возвращаем пустой массив в случае ошибки
      return [];
    }
  };

  /**
   * Получает количество событий по категориям
   */
  const getCategoryCounts = async () => {
    try {
      // Если API-endpoint еще не реализован, возвращаем тестовые данные
      return [
        { id: 1, name: "Политические", count: 120 },
        { id: 2, name: "Военные", count: 85 },
        { id: 3, name: "Экономические", count: 65 },
        { id: 4, name: "Культурные", count: 75 },
        { id: 5, name: "Научные", count: 55 },
        { id: 6, name: "Социальные", count: 40 },
        { id: 7, name: "Религиозные", count: 30 },
        { id: 8, name: "Другие", count: 25 }
      ];
      
      // Раскомментируйте, когда будет готов API endpoint
      // return await get<any[]>('/categories/events-count');
    } catch (error) {
      console.error('Ошибка при получении количества событий по категориям:', error);
      // Возвращаем пустой массив в случае ошибки
      return [];
    }
  };

  /**
   * Получает годовой рост количества событий
   */
  const getYearlyGrowth = async () => {
    try {
      // Если API-endpoint еще не реализован, возвращаем тестовые данные
      return [
        { year: "1900", count: 10 },
        { year: "1910", count: 15 },
        { year: "1920", count: 25 },
        { year: "1930", count: 35 },
        { year: "1940", count: 60 },
        { year: "1950", count: 45 },
        { year: "1960", count: 50 },
        { year: "1970", count: 65 },
        { year: "1980", count: 70 },
        { year: "1990", count: 85 },
        { year: "2000", count: 95 },
        { year: "2010", count: 110 },
        { year: "2020", count: 120 }
      ];
      
      // Раскомментируйте, когда будет готов API endpoint
      // return await get<any[]>('/events/yearly-growth');
    } catch (error) {
      console.error('Ошибка при получении данных о годовом росте событий:', error);
      // Возвращаем пустой массив в случае ошибки
      return [];
    }
  };
  
  return {
    get,
    post,
    put,
    del,
    loading,
    getAllEvents,
    getCountries,
    getCategoryCounts,
    getYearlyGrowth
  }
} 