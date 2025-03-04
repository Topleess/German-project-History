import sqlite3

def check_tables():
    """Проверяет наличие таблиц в базе данных"""
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"Найдено {len(tables)} таблиц:")
    for table in tables:
        print(table[0])
        
        # Выводим структуру таблицы
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"  Структура таблицы {table[0]}:")
        for column in columns:
            print(f"    {column}")
    
    conn.close()

if __name__ == "__main__":
    check_tables() 