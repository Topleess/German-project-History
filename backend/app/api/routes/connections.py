from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional

from ...db.database import get_db
from ...db.models import Connection, Event
from ..schemas import Connection as ConnectionSchema, ConnectionCreate, ConnectionDetail

router = APIRouter()

@router.get("/connections/", response_model=List[ConnectionSchema])
async def read_connections(
    skip: int = 0, 
    limit: int = 100,
    cause_id: Optional[int] = None,
    effect_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список связей между историческими событиями с возможностью фильтрации
    """
    query = select(Connection)
    
    # Применяем фильтры, если они указаны
    if cause_id:
        query = query.where(Connection.cause_id == cause_id)
    if effect_id:
        query = query.where(Connection.effect_id == effect_id)
    
    # Добавляем пагинацию
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    connections = result.scalars().all()
    
    return connections

@router.get("/connections/{connection_id}", response_model=ConnectionDetail)
async def read_connection(connection_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить детальную информацию о конкретной связи по её ID
    """
    query = select(Connection).where(Connection.id == connection_id)
    result = await db.execute(query)
    connection = result.scalars().first()
    
    if connection is None:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    
    return connection

@router.post("/connections/", response_model=ConnectionSchema)
async def create_connection(connection: ConnectionCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новую связь между историческими событиями
    """
    # Проверяем, существуют ли события
    cause_query = select(Event).where(Event.id == connection.cause_id)
    cause_result = await db.execute(cause_query)
    cause_event = cause_result.scalars().first()
    
    if cause_event is None:
        raise HTTPException(status_code=404, detail="Событие-причина не найдено")
    
    effect_query = select(Event).where(Event.id == connection.effect_id)
    effect_result = await db.execute(effect_query)
    effect_event = effect_result.scalars().first()
    
    if effect_event is None:
        raise HTTPException(status_code=404, detail="Событие-следствие не найдено")
    
    # Проверяем, что события не одинаковые
    if connection.cause_id == connection.effect_id:
        raise HTTPException(status_code=400, detail="Событие не может быть связано само с собой")
    
    # Проверяем, что такая связь еще не существует
    existing_query = select(Connection).where(
        (Connection.cause_id == connection.cause_id) & 
        (Connection.effect_id == connection.effect_id)
    )
    existing_result = await db.execute(existing_query)
    existing_connection = existing_result.scalars().first()
    
    if existing_connection is not None:
        raise HTTPException(status_code=400, detail="Такая связь уже существует")
    
    # Создаем новую связь
    db_connection = Connection(**connection.model_dump())
    db.add(db_connection)
    await db.commit()
    await db.refresh(db_connection)
    
    return db_connection

@router.put("/connections/{connection_id}", response_model=ConnectionSchema)
async def update_connection(
    connection_id: int, 
    connection_update: ConnectionCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить существующую связь между историческими событиями
    """
    # Проверяем, существует ли связь
    connection_query = select(Connection).where(Connection.id == connection_id)
    connection_result = await db.execute(connection_query)
    db_connection = connection_result.scalars().first()
    
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    
    # Проверяем, существуют ли события
    cause_query = select(Event).where(Event.id == connection_update.cause_id)
    cause_result = await db.execute(cause_query)
    cause_event = cause_result.scalars().first()
    
    if cause_event is None:
        raise HTTPException(status_code=404, detail="Событие-причина не найдено")
    
    effect_query = select(Event).where(Event.id == connection_update.effect_id)
    effect_result = await db.execute(effect_query)
    effect_event = effect_result.scalars().first()
    
    if effect_event is None:
        raise HTTPException(status_code=404, detail="Событие-следствие не найдено")
    
    # Проверяем, что события не одинаковые
    if connection_update.cause_id == connection_update.effect_id:
        raise HTTPException(status_code=400, detail="Событие не может быть связано само с собой")
    
    # Обновляем связь
    update_data = connection_update.model_dump()
    update_query = update(Connection).where(Connection.id == connection_id).values(update_data)
    await db.execute(update_query)
    await db.commit()
    
    # Получаем обновленную связь
    result = await db.execute(connection_query)
    updated_connection = result.scalars().first()
    
    return updated_connection

@router.delete("/connections/{connection_id}")
async def delete_connection(connection_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить связь между историческими событиями
    """
    # Проверяем, существует ли связь
    connection_query = select(Connection).where(Connection.id == connection_id)
    connection_result = await db.execute(connection_query)
    db_connection = connection_result.scalars().first()
    
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    
    # Удаляем связь
    delete_query = delete(Connection).where(Connection.id == connection_id)
    await db.execute(delete_query)
    await db.commit()
    
    return {"ok": True, "message": "Связь успешно удалена"} 