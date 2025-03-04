import asyncio
from datetime import datetime, timedelta
import random

from app.db.session import async_engine
from app.models.models import Category, Event, Connection
from app.db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

# Новые категории для добавления
new_categories = [
    {"name": "Архитектура", "color": "#8A2BE2", "description": "Важные архитектурные сооружения и стили"},
    {"name": "Спорт", "color": "#32CD32", "description": "Спортивные события и достижения"},
    {"name": "Технологии", "color": "#00CED1", "description": "Технологические инновации и изобретения"},
    {"name": "Религия", "color": "#FFD700", "description": "Религиозные события и движения"},
    {"name": "Исследования", "color": "#4682B4", "description": "Географические открытия и исследования"}
]

# Новые события для добавления
new_events = [
    {
        "title": "Строительство Берлинской стены",
        "date": datetime(1961, 8, 13),
        "end_date": datetime(1989, 11, 9),
        "description": "Возведение стены, разделившей Берлин на восточную и западную части",
        "location": "Берлин, Германия",
        "importance": 5,
        "category_id": 2  # Политика
    },
    {
        "title": "Падение Берлинской стены",
        "date": datetime(1989, 11, 9),
        "description": "Разрушение Берлинской стены, символизирующее окончание Холодной войны",
        "location": "Берлин, Германия",
        "importance": 5,
        "category_id": 2  # Политика
    },
    {
        "title": "Строительство Эйфелевой башни",
        "date": datetime(1887, 1, 28),
        "end_date": datetime(1889, 3, 31),
        "description": "Строительство одной из самых известных достопримечательностей в мире",
        "location": "Париж, Франция",
        "importance": 3,
        "category_id": 6  # Архитектура (новая категория)
    },
    {
        "title": "Олимпийские игры в Берлине",
        "date": datetime(1936, 8, 1),
        "end_date": datetime(1936, 8, 16),
        "description": "Летние Олимпийские игры, проходившие в нацистской Германии",
        "location": "Берлин, Германия",
        "importance": 4,
        "category_id": 7  # Спорт (новая категория)
    },
    {
        "title": "Создание Европейского Союза",
        "date": datetime(1993, 11, 1),
        "description": "Образование Европейского Союза после подписания Маастрихтского договора",
        "location": "Европа",
        "importance": 5,
        "category_id": 2  # Политика
    },
    {
        "title": "Изобретение World Wide Web",
        "date": datetime(1989, 3, 12),
        "description": "Тим Бернерс-Ли представил предложение о создании World Wide Web",
        "location": "ЦЕРН, Швейцария",
        "importance": 5,
        "category_id": 8  # Технологии (новая категория)
    },
    {
        "title": "Запуск первого iPhone",
        "date": datetime(2007, 6, 29),
        "description": "Запуск первого iPhone, ознаменовавший революцию в мобильных технологиях",
        "location": "США",
        "importance": 4,
        "category_id": 8  # Технологии
    },
    {
        "title": "Реформация",
        "date": datetime(1517, 10, 31),
        "end_date": datetime(1648, 10, 24),
        "description": "Религиозное движение в Западной Европе, направленное на реформирование церкви",
        "location": "Европа",
        "importance": 5,
        "category_id": 9  # Религия (новая категория)
    },
    {
        "title": "Путешествие Христофора Колумба",
        "date": datetime(1492, 8, 3),
        "end_date": datetime(1493, 3, 15),
        "description": "Первое путешествие Колумба в Америку",
        "location": "Атлантический океан",
        "importance": 5,
        "category_id": 10  # Исследования (новая категория)
    },
    {
        "title": "Полет на Луну",
        "date": datetime(1969, 7, 20),
        "description": "Первая высадка человека на Луну в рамках миссии Аполлон-11",
        "location": "Луна",
        "importance": 5,
        "category_id": 10  # Исследования
    },
    {
        "title": "Строительство Колизея",
        "date": datetime(72, 1, 1),
        "end_date": datetime(80, 1, 1),
        "description": "Строительство знаменитого римского амфитеатра",
        "location": "Рим, Италия",
        "importance": 4,
        "category_id": 6  # Архитектура
    },
    {
        "title": "Первый чемпионат мира по футболу",
        "date": datetime(1930, 7, 13),
        "end_date": datetime(1930, 7, 30),
        "description": "Первый международный турнир по футболу среди сборных команд",
        "location": "Уругвай",
        "importance": 3,
        "category_id": 7  # Спорт
    },
    {
        "title": "Изобретение парового двигателя",
        "date": datetime(1712, 1, 1),
        "description": "Изобретение Томасом Ньюкоменом первого практического парового двигателя",
        "location": "Англия",
        "importance": 5,
        "category_id": 8  # Технологии
    },
    {
        "title": "Второй Ватиканский собор",
        "date": datetime(1962, 10, 11),
        "end_date": datetime(1965, 12, 8),
        "description": "Важный собор католической церкви, внесший значительные изменения в литургию и отношения с другими конфессиями",
        "location": "Ватикан",
        "importance": 4,
        "category_id": 9  # Религия
    },
    {
        "title": "Экспедиция Магеллана",
        "date": datetime(1519, 9, 20),
        "end_date": datetime(1522, 9, 6),
        "description": "Первое кругосветное путешествие, начатое под руководством Фернана Магеллана",
        "location": "Мировой океан",
        "importance": 5,
        "category_id": 10  # Исследования
    },
    {
        "title": "Чернобыльская катастрофа",
        "date": datetime(1986, 4, 26),
        "description": "Крупнейшая в истории атомной энергетики авария",
        "location": "Чернобыль, УССР",
        "importance": 5,
        "category_id": 4  # Наука
    },
    {
        "title": "Глобальный финансовый кризис",
        "date": datetime(2008, 9, 15),
        "end_date": datetime(2009, 6, 1),
        "description": "Мировой экономический кризис, начавшийся с краха банка Lehman Brothers",
        "location": "Весь мир",
        "importance": 5,
        "category_id": 5  # Экономика
    },
    {
        "title": "Строительство Великой Китайской стены",
        "date": datetime(-700, 1, 1),
        "end_date": datetime(1644, 1, 1),
        "description": "Строительство одного из крупнейших архитектурных сооружений в истории",
        "location": "Китай",
        "importance": 5,
        "category_id": 6  # Архитектура
    },
    {
        "title": "Первые современные Олимпийские игры",
        "date": datetime(1896, 4, 6),
        "end_date": datetime(1896, 4, 15),
        "description": "Возрождение Олимпийских игр в современном формате",
        "location": "Афины, Греция",
        "importance": 4,
        "category_id": 7  # Спорт
    },
    {
        "title": "Изобретение микропроцессора",
        "date": datetime(1971, 11, 15),
        "description": "Создание Intel 4004, первого коммерчески доступного микропроцессора",
        "location": "США",
        "importance": 5,
        "category_id": 8  # Технологии
    }
]

# Новые связи между событиями
new_connections = [
    {
        "cause_id": 16,  # Строительство Берлинской стены
        "effect_id": 17,  # Падение Берлинской стены
        "description": "Строительство стены привело к последующему падению",
        "strength": 3
    },
    {
        "cause_id": 16,  # Строительство Берлинской стены
        "effect_id": 7,  # Холодная война
        "description": "Берлинская стена как символ Холодной войны",
        "strength": 2
    },
    {
        "cause_id": 17,  # Падение Берлинской стены
        "effect_id": 11,  # Распад СССР
        "description": "Падение стены способствовало распаду СССР",
        "strength": 2
    },
    {
        "cause_id": 7,  # Холодная война
        "effect_id": 25,  # Полет на Луну
        "description": "Космическая гонка как результат Холодной войны",
        "strength": 3
    },
    {
        "cause_id": 21,  # Создание Европейского Союза
        "effect_id": 11,  # Распад СССР
        "description": "Распад СССР способствовал созданию ЕС",
        "strength": 1
    },
    {
        "cause_id": 22,  # Изобретение World Wide Web
        "effect_id": 23,  # Запуск первого iPhone
        "description": "Развитие веб-технологий привело к созданию смартфонов",
        "strength": 2
    },
    {
        "cause_id": 24,  # Путешествие Колумба
        "effect_id": 30,  # Экспедиция Магеллана
        "description": "Открытия Колумба вдохновили другие экспедиции",
        "strength": 2
    },
    {
        "cause_id": 28,  # Изобретение парового двигателя
        "effect_id": 22,  # Изобретение WWW (как символ технического прогресса)
        "description": "Промышленная революция привела к информационной революции",
        "strength": 1
    },
    {
        "cause_id": 31,  # Чернобыльская катастрофа
        "effect_id": 15,  # Пандемия COVID-19
        "description": "Влияние на глобальное осознание опасностей технологий",
        "strength": 1
    },
    {
        "cause_id": 32,  # Глобальный финансовый кризис
        "effect_id": 13,  # Экономический кризис 2008
        "description": "Продолжающееся влияние кризиса",
        "strength": 3
    }
]

async def create_test_data():
    try:
        # Создаем сессию
        async with AsyncSession(async_engine) as session:
            # Добавляем новые категории
            print("Добавление новых категорий...")
            for category_data in new_categories:
                # Проверяем, существует ли уже категория с таким именем
                result = await session.execute(
                    select(Category).where(Category.name == category_data["name"])
                )
                existing_category = result.scalars().first()
                if not existing_category:
                    category = Category(**category_data)
                    session.add(category)
            
            # Сохраняем изменения, чтобы получить ID категорий
            await session.commit()
            
            # Добавляем новые события
            print("Добавление новых событий...")
            for event_data in new_events:
                # Проверяем, существует ли уже событие с таким названием
                result = await session.execute(
                    select(Event).where(Event.title == event_data["title"])
                )
                existing_event = result.scalars().first()
                if not existing_event:
                    # Проверим, существует ли категория с указанным ID
                    result = await session.execute(
                        select(Category).where(Category.id == event_data["category_id"])
                    )
                    category = result.scalars().first()
                    if category:
                        event = Event(**event_data)
                        session.add(event)
                    else:
                        print(f"Категория с ID {event_data['category_id']} не найдена")
            
            # Сохраняем изменения, чтобы получить ID событий
            await session.commit()
            
            # Добавляем новые связи
            print("Добавление новых связей...")
            for connection_data in new_connections:
                # Проверяем, существует ли уже такая связь
                result = await session.execute(
                    select(Connection).where(
                        Connection.cause_id == connection_data["cause_id"],
                        Connection.effect_id == connection_data["effect_id"]
                    )
                )
                existing_connection = result.scalars().first()
                if not existing_connection:
                    # Проверим, существуют ли события с указанными ID
                    cause_result = await session.execute(
                        select(Event).where(Event.id == connection_data["cause_id"])
                    )
                    effect_result = await session.execute(
                        select(Event).where(Event.id == connection_data["effect_id"])
                    )
                    cause = cause_result.scalars().first()
                    effect = effect_result.scalars().first()
                    if cause and effect:
                        connection = Connection(**connection_data)
                        session.add(connection)
                    else:
                        print(f"События с ID {connection_data['cause_id']} или {connection_data['effect_id']} не найдены")
            
            # Сохраняем все изменения
            await session.commit()
            
            # Выводим количество записей в каждой таблице
            categories_count = await session.execute(select(func.count()).select_from(Category))
            events_count = await session.execute(select(func.count()).select_from(Event))
            connections_count = await session.execute(select(func.count()).select_from(Connection))
            
            print(f"Всего категорий: {categories_count.scalar()}")
            print(f"Всего событий: {events_count.scalar()}")
            print(f"Всего связей: {connections_count.scalar()}")
            
            print("Тестовые данные успешно добавлены!")
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_data()) 