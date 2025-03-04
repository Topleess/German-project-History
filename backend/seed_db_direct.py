import sqlite3
import datetime

def seed_db():
    """Заполняет базу данных тестовыми данными напрямую через SQLite"""
    print("Начинаем заполнение базы данных...")
    
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли уже данные в базе
    cursor.execute("SELECT COUNT(*) FROM categories")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("База данных уже содержит данные. Пропускаем заполнение.")
        conn.close()
        return
    
    # Создаем категории
    categories = [
        (1, "Войны", "#ff7f0e", "Военные конфликты и сражения"),
        (2, "Политика", "#1f77b4", "Политические события и решения"),
        (3, "Культура", "#2ca02c", "Культурные события и достижения"),
        (4, "Наука", "#9467bd", "Научные открытия и изобретения"),
        (5, "Экономика", "#d62728", "Экономические события и кризисы")
    ]
    
    cursor.executemany(
        "INSERT INTO categories (id, name, color, description) VALUES (?, ?, ?, ?)",
        categories
    )
    
    # Текущее время для полей created_at и updated_at
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Создаем события
    events = [
        (1, "Первая мировая война", "1914-07-28", "1918-11-11", 
         "Один из самых широкомасштабных военных конфликтов в истории человечества.",
         "Европа", 5, None, 1, now, now),
        (2, "Революция 1917 года", "1917-02-23", "1917-11-07", 
         "Цепь революционных событий в России в 1917 году, которые привели к свержению монархии и установлению советской власти.",
         "Россия", 5, None, 2, now, now),
        (3, "Версальский договор", "1919-06-28", None, 
         "Мирный договор, официально завершивший Первую мировую войну.",
         "Версаль, Франция", 4, None, 2, now, now),
        (4, "Теория относительности Эйнштейна", "1915-11-25", None, 
         "Публикация общей теории относительности Альбертом Эйнштейном.",
         "Германия", 5, None, 4, now, now),
        (5, "Великая депрессия", "1929-10-29", "1939-09-01", 
         "Мировой экономический кризис, начавшийся после краха на Нью-Йоркской фондовой бирже.",
         "США, мир", 5, None, 5, now, now)
    ]
    
    cursor.executemany(
        """INSERT INTO events 
           (id, title, date, end_date, description, location, importance, image_url, category_id, created_at, updated_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        events
    )
    
    # Создаем связи между событиями
    connections = [
        (1, 1, 2, "Война привела к революции", 1, now),
        (2, 1, 3, "Результат войны", 2, now),
        (3, 2, 3, "Влияние на договор", 1, now)
    ]
    
    cursor.executemany(
        """INSERT INTO connections 
           (id, cause_id, effect_id, description, strength, created_at) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        connections
    )
    
    # Сохраняем изменения
    conn.commit()
    conn.close()
    
    print("База данных успешно заполнена тестовыми данными!")

if __name__ == "__main__":
    seed_db() 