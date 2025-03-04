import asyncio
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.database import async_session, init_db
from app.db.models import Category, Event, Connection

async def seed_data():
    """Заполняет базу данных тестовыми данными"""
    print("Начинаем заполнение базы данных...")
    
    # Инициализируем базу данных
    await init_db()
    
    async with async_session() as session:
        # Проверяем, есть ли уже данные в базе
        result = await session.execute(text("SELECT COUNT(*) FROM categories"))
        count = result.scalar()
        
        if count > 0:
            print("База данных уже содержит данные. Пропускаем заполнение.")
            return
        
        # Создаем категории
        categories = [
            Category(name="Войны", color="#ff7f0e", description="Военные конфликты и сражения"),
            Category(name="Политика", color="#1f77b4", description="Политические события и решения"),
            Category(name="Культура", color="#2ca02c", description="Культурные события и достижения"),
            Category(name="Наука", color="#9467bd", description="Научные открытия и изобретения"),
            Category(name="Экономика", color="#d62728", description="Экономические события и кризисы")
        ]
        
        session.add_all(categories)
        await session.commit()
        
        # Получаем ID созданных категорий
        for cat in categories:
            await session.refresh(cat)
        
        # Создаем события
        events = [
            Event(
                title="Первая мировая война",
                date=datetime.datetime(1914, 7, 28),
                end_date=datetime.datetime(1918, 11, 11),
                description="Один из самых широкомасштабных военных конфликтов в истории человечества.",
                location="Европа",
                importance=5,
                category_id=categories[0].id
            ),
            Event(
                title="Революция 1917 года",
                date=datetime.datetime(1917, 2, 23),
                end_date=datetime.datetime(1917, 11, 7),
                description="Цепь революционных событий в России в 1917 году, которые привели к свержению монархии и установлению советской власти.",
                location="Россия",
                importance=5,
                category_id=categories[1].id
            ),
            Event(
                title="Версальский договор",
                date=datetime.datetime(1919, 6, 28),
                description="Мирный договор, официально завершивший Первую мировую войну.",
                location="Версаль, Франция",
                importance=4,
                category_id=categories[1].id
            ),
            Event(
                title="Теория относительности Эйнштейна",
                date=datetime.datetime(1915, 11, 25),
                description="Публикация общей теории относительности Альбертом Эйнштейном.",
                location="Германия",
                importance=5,
                category_id=categories[3].id
            ),
            Event(
                title="Великая депрессия",
                date=datetime.datetime(1929, 10, 29),
                end_date=datetime.datetime(1939, 9, 1),
                description="Мировой экономический кризис, начавшийся после краха на Нью-Йоркской фондовой бирже.",
                location="США, мир",
                importance=5,
                category_id=categories[4].id
            )
        ]
        
        session.add_all(events)
        await session.commit()
        
        # Получаем ID созданных событий
        for event in events:
            await session.refresh(event)
        
        # Создаем связи между событиями
        connections = [
            Connection(
                cause_id=events[0].id,  # Первая мировая война
                effect_id=events[1].id,  # Революция 1917 года
                description="Война привела к революции",
                strength=1
            ),
            Connection(
                cause_id=events[0].id,  # Первая мировая война
                effect_id=events[2].id,  # Версальский договор
                description="Результат войны",
                strength=2
            ),
            Connection(
                cause_id=events[1].id,  # Революция 1917 года
                effect_id=events[2].id,  # Версальский договор
                description="Влияние на договор",
                strength=1
            )
        ]
        
        session.add_all(connections)
        await session.commit()
        
        print("База данных успешно заполнена тестовыми данными!")

if __name__ == "__main__":
    asyncio.run(seed_data()) 