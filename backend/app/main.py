from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from .db.database import get_db, init_db
from .api.routes import events, connections, categories

app = FastAPI(
    title="История - API",
    description="API для интерактивной образовательной платформы по истории",
    version="0.1.0",
    redirect_slashes=False,
)

# CORS middleware для работы с frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3005", "http://localhost", "*"],  # Добавляем больше вариантов
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Явно указываем поддержку OPTIONS
    allow_headers=["*"],
    max_age=86400,  # Кэшировать предварительные запросы на 24 часа
)

# Включаем маршруты API
app.include_router(events.router, prefix="/api", tags=["events"])
app.include_router(connections.router, prefix="/api", tags=["connections"])
app.include_router(categories.router, prefix="/api", tags=["categories"])

@app.on_event("startup")
async def startup():
    # Инициализация базы данных при запуске
    await init_db()

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API интерактивной образовательной платформы по истории"} 