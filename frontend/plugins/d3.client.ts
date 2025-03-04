import * as d3 from 'd3'

export default defineNuxtPlugin(() => {
  // Убедимся, что D3 полностью загружен
  if (!d3) {
    console.error('D3.js не загружен корректно')
    return {
      provide: {
        d3: null
      }
    }
  }
  
  // Принудительно получим версию
  const version = d3.version || 'неизвестно'
  console.log('D3.js успешно инициализирован', version)
  
  // Проверка наличия необходимых модулей
  if (!d3.select || !d3.forceSimulation) {
    console.error('D3.js: не найдены необходимые модули')
  }
  
  // Выводим информацию о доступных модулях для отладки
  const modules = [
    'select', 'forceSimulation', 'forceManyBody', 
    'forceLink', 'forceCenter', 'forceCollide', 
    'zoom', 'zoomIdentity', 'drag'
  ]
  
  const moduleStatus = modules.reduce((acc, name) => {
    acc[name] = !!d3[name];
    return acc;
  }, {} as Record<string, boolean>);
  
  console.log('D3 модули:', moduleStatus)
  
  // Расширим функциональность d3 для отладки
  const enhancedD3 = {
    ...d3,
    debug: true,
    version
  }
  
  return {
    provide: {
      d3: enhancedD3
    }
  }
}) 