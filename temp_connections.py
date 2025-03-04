from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional

from ...db.database import get_db
from ...db.models import Connection, Event
from ..schemas import Connection as ConnectionSchema, ConnectionCreate, ConnectionUpdate

router = APIRouter()

@router.get("/connections", response_model=List[ConnectionSchema])
async def read_connections(
    skip: int = 0,
    limit: int = 100,
    cause_id: Optional[int] = None,
    effect_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список связей между событиями с возможностью фильтрации
    """
    query = select(Connection)
    
    # Применяем фильтры, если они указаны
    if cause_id:
        query = query.where(Connection.cause_id == cause_id)
    if effect_id:
        query = query.where(Connection.effect_id == effect_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    connections = result.scalars().all()
    
    return connections

@router.get("/connections/{connection_id}", response_model=ConnectionSchema)
async def read_connection(connection_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о конкретной связи по её ID
    """
    query = select(Connection).where(Connection.id == connection_id)
    result = await db.execute(query)
    connection = result.scalar_one_or_none()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    
    return connection

@router.post("/connections", response_model=ConnectionSchema)
async def create_connection(connection: ConnectionCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новую связь между событиями
    """
    # Проверяем существование событий
    cause_query = select(Event).where(Event.id == connection.cause_id)
    cause_result = await db.execute(cause_query)
    cause_event = cause_result.scalar_one_or_none()
    
    if not cause_event:
        raise HTTPException(status_code=404, detail="Событие-причина не найдено")
    
    effect_query = select(Event).where(Event.id == connection.effect_id)
    effect_result = await db.execute(effect_query)
    effect_event = effect_result.scalar_one_or_none()
    
    if not effect_event:
        raise HTTPException(status_code=404, detail="Событие-следствие не найдено")
    
    db_connection = Connection(**connection.dict())
    db.add(db_connection)
    await db.commit()
    await db.refresh(db_connection)
    
    return db_connection

@router.put("/connections/{connection_id}", response_model=ConnectionSchema)
async def update_connection(
    connection_id: int, 
    connection_update: ConnectionUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить существующую связь
    """
    query = select(Connection).where(Connection.id == connection_id)
    result = await db.execute(query)
    db_connection = result.scalar_one_or_none()
    
    if not db_connection:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    
    # Обновляем только предоставленные поля
    update_data = connection_update.dict(exclude_unset=True)
    
    # Если меняются связанные события, проверяем их существование
    if 'cause_id' in update_data:
        cause_query = select(Event).where(Event.id == update_data['cause_id'])
        cause_result = await db.execute(cause_query)
        cause_event = cause_result.scalar_one_or_none()
        
        if not cause_event:
            raise HTTPException(status_code=404, detail="Событие-причина не найдено")
    
    if 'effect_id' in update_data:
        effect_query = select(Event).where(Event.id == update_data['effect_id'])
        effect_result = await db.execute(effect_query)
        effect_event = effect_result.scalar_one_or_none()
        
        if not effect_event:
            raise HTTPException(status_code=404, detail="Событие-следствие не найдено")
    
    for key, value in update_data.items():
        setattr(db_connection, key, value)
    
    await db.commit()
    await db.refresh(db_connection)
    
    return db_connection

@router.delete("/connections/{connection_id}", response_model=dict)
async def delete_connection(connection_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить связь
    """
    query = select(Connection).where(Connection.id == connection_id)
    result = await db.execute(query)
    db_connection = result.scalar_one_or_none()
    
    if not db_connection:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    
    await db.delete(db_connection)
    await db.commit()
    
    return {"message": "Связь успешно удалена"} 