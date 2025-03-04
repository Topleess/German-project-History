export default defineNuxtPlugin(() => {
  /**
   * Форматирует дату в локализованный формат
   * @param dateString - строка с датой в формате ISO
   * @param locale - локаль для форматирования (по умолчанию ru-RU)
   * @returns отформатированная дата
   */
  const formatDate = (dateString: string | null | undefined, locale = 'ru-RU'): string => {
    if (!dateString) return ''
    
    try {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat(locale).format(date)
    } catch (error) {
      console.error('Ошибка при форматировании даты:', error)
      return dateString || ''
    }
  }
  
  /**
   * Форматирует дату и время в локализованный формат
   * @param dateString - строка с датой в формате ISO
   * @param locale - локаль для форматирования (по умолчанию ru-RU)
   * @returns отформатированная дата и время
   */
  const formatDateTime = (dateString: string | null | undefined, locale = 'ru-RU'): string => {
    if (!dateString) return ''
    
    try {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    } catch (error) {
      console.error('Ошибка при форматировании даты и времени:', error)
      return dateString || ''
    }
  }
  
  /**
   * Форматирует период между двумя датами
   * @param startDate - начальная дата в формате ISO
   * @param endDate - конечная дата в формате ISO
   * @param locale - локаль для форматирования (по умолчанию ru-RU)
   * @returns отформатированный период
   */
  const formatDateRange = (
    startDate: string | null | undefined, 
    endDate: string | null | undefined, 
    locale = 'ru-RU'
  ): string => {
    if (!startDate) return ''
    
    const formattedStart = formatDate(startDate, locale)
    
    if (!endDate) return formattedStart
    
    const formattedEnd = formatDate(endDate, locale)
    return `${formattedStart} - ${formattedEnd}`
  }
  
  return {
    provide: {
      formatDate,
      formatDateTime,
      formatDateRange
    }
  }
}) 