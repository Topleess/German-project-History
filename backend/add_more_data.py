import sqlite3
import datetime

def add_more_data():
    """Добавляет дополнительные тестовые данные в существующую базу данных"""
    print("Начинаем добавление дополнительных тестовых данных...")
    
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    
    # Получаем максимальные ID, чтобы не было конфликтов
    cursor.execute("SELECT MAX(id) FROM events")
    max_event_id = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT MAX(id) FROM connections")
    max_connection_id = cursor.fetchone()[0] or 0
    
    # Текущее время для полей created_at и updated_at
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Добавляем новые события (10 событий)
    new_events = [
        (max_event_id + 1, "Вторая мировая война", "1939-09-01", "1945-09-02", 
         "Глобальный военный конфликт, в котором участвовало большинство стран мира, включая все великие державы.",
         "Весь мир", 5, None, 1, now, now),
        
        (max_event_id + 2, "Холодная война", "1947-03-12", "1991-12-26", 
         "Геополитическое, военное, экономическое и идеологическое противостояние между СССР и западными странами.",
         "Весь мир", 5, None, 2, now, now),
        
        (max_event_id + 3, "Полет человека в космос", "1961-04-12", None, 
         "Первый полет человека в космос, совершенный Юрием Гагариным на корабле 'Восток-1'.",
         "СССР", 5, None, 4, now, now),
        
        (max_event_id + 4, "Культурная революция в Китае", "1966-05-16", "1976-09-09", 
         "Политическая кампания, начатая Мао Цзэдуном с целью укрепления своей власти.",
         "Китай", 4, None, 3, now, now),
        
        (max_event_id + 5, "Нефтяной кризис 1973 года", "1973-10-17", "1974-03-18", 
         "Энергетический кризис, вызванный эмбарго на поставки нефти странами ОПЕК.",
         "Западные страны", 4, None, 5, now, now),
        
        (max_event_id + 6, "Распад СССР", "1991-12-26", None, 
         "Прекращение существования Союза Советских Социалистических Республик.",
         "СССР", 5, None, 2, now, now),
        
        (max_event_id + 7, "Изобретение Интернета", "1989-03-12", None, 
         "Создание Всемирной паутины Тимом Бернерсом-Ли.",
         "Швейцария", 5, None, 4, now, now),
        
        (max_event_id + 8, "Экономический кризис 2008 года", "2008-09-15", "2009-06-01", 
         "Мировой финансово-экономический кризис, начавшийся с краха банка Lehman Brothers.",
         "Весь мир", 4, None, 5, now, now),
        
        (max_event_id + 9, "Арабская весна", "2010-12-18", "2012-12-01", 
         "Волна демонстраций и протестов в странах Северной Африки и Ближнего Востока.",
         "Ближний Восток, Северная Африка", 4, None, 2, now, now),
        
        (max_event_id + 10, "Пандемия COVID-19", "2019-12-01", None, 
         "Глобальная пандемия коронавирусной инфекции, вызванная вирусом SARS-CoV-2.",
         "Весь мир", 5, None, 4, now, now)
    ]
    
    cursor.executemany(
        """INSERT INTO events 
           (id, title, date, end_date, description, location, importance, image_url, category_id, created_at, updated_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        new_events
    )
    
    # Добавляем новые связи между событиями
    new_connections = [
        (max_connection_id + 1, 1, max_event_id + 1, "Первая мировая война создала условия для Второй", 3, now),
        (max_connection_id + 2, max_event_id + 1, max_event_id + 2, "Вторая мировая война привела к началу Холодной войны", 3, now),
        (max_connection_id + 3, max_event_id + 2, max_event_id + 3, "Космическая гонка как часть Холодной войны", 2, now),
        (max_connection_id + 4, max_event_id + 2, max_event_id + 4, "Влияние идеологического противостояния на Китай", 2, now),
        (max_connection_id + 5, max_event_id + 5, max_event_id + 2, "Нефтяной кризис усилил напряженность Холодной войны", 1, now),
        (max_connection_id + 6, max_event_id + 2, max_event_id + 6, "Холодная война привела к распаду СССР", 3, now),
        (max_connection_id + 7, max_event_id + 2, max_event_id + 7, "Ранние разработки интернета связаны с военными технологиями времен Холодной войны", 1, now),
        (max_connection_id + 8, max_event_id + 6, max_event_id + 8, "Экономические изменения после распада СССР влияли на мировую экономику", 1, now),
        (max_connection_id + 9, max_event_id + 8, max_event_id + 9, "Экономический кризис усилил социальную напряженность в странах Ближнего Востока", 2, now),
        (max_connection_id + 10, max_event_id + 9, max_event_id + 10, "Глобальные перемещения людей влияли на распространение вирусов", 1, now)
    ]
    
    cursor.executemany(
        """INSERT INTO connections 
           (id, cause_id, effect_id, description, strength, created_at) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        new_connections
    )
    
    # Сохраняем изменения
    conn.commit()
    conn.close()
    
    print("Дополнительные тестовые данные успешно добавлены в базу данных!")

if __name__ == "__main__":
    add_more_data() 