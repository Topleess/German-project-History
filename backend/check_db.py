import sqlite3

def check_db():
    """Проверяет наличие данных в базе данных"""
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    
    print("Проверка таблицы категорий:")
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    print(f"Найдено {len(categories)} категорий:")
    for category in categories:
        print(category)
    
    print("\nПроверка таблицы событий:")
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    print(f"Найдено {len(events)} событий:")
    for event in events:
        print(event)
    
    print("\nПроверка таблицы связей:")
    cursor.execute('SELECT * FROM connections')
    connections = cursor.fetchall()
    print(f"Найдено {len(connections)} связей:")
    for connection in connections:
        print(connection)
    
    conn.close()

if __name__ == "__main__":
    check_db() 