from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from .db.database import get_db, init_db
from .api.routes import events, connections

app = FastAPI(
    title="История - API",
    description="API для интерактивной образовательной платформы по истории",
    version="0.1.0",
)

# CORS middleware для работы с frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Nuxt по умолчанию работает на порту 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Включаем маршруты API
app.include_router(events.router, prefix="/api", tags=["events"])
app.include_router(connections.router, prefix="/api", tags=["connections"])

@app.on_event("startup")
async def startup():
    # Инициализация базы данных при запуске
    await init_db()

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API интерактивной образовательной платформы по истории"} 