import os
from app.db.database import Base, engine

async def run_migrations():
    """
    Выполняет миграции базы данных
    """
    print('Запуск миграций...')
    async with engine.begin() as conn:
        # Создаем все таблицы из моделей, если их нет
        await conn.run_sync(Base.metadata.create_all)
    print('Миграции успешно выполнены') 