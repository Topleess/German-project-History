from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os

# Создаем базовый класс для ORM-моделей
Base = declarative_base()

# Путь к SQLite базе данных
DATABASE_URL = "sqlite+aiosqlite:///./history.db"

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)

# Создаем фабрику сессий
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии базы данных
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Инициализация базы данных
async def init_db():
    async with engine.begin() as conn:
        # Создаем все таблицы из моделей
        await conn.run_sync(Base.metadata.create_all) 