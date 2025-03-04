from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from datetime import datetime

from ...db.database import get_db
from ...db.models import Event
from ..schemas import Event as EventSchema, EventCreate, EventUpdate

router = APIRouter()

@router.get("/events", response_model=List[EventSchema])
async def read_events(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список событий с возможностью фильтрации
    """
    query = select(Event)
    
    # Применяем фильтры, если они указаны
    if category_id:
        query = query.where(Event.category_id == category_id)
    if start_date:
        query = query.where(Event.date >= start_date)
    if end_date:
        query = query.where(Event.date <= end_date)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    events = result.scalars().all()
    
    return events

@router.get("/events/{event_id}", response_model=EventSchema)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о конкретном событии по его ID
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    return event

@router.post("/events", response_model=EventSchema)
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новое событие
    """
    db_event = Event(**event.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    
    return db_event

@router.put("/events/{event_id}", response_model=EventSchema)
async def update_event(
    event_id: int, 
    event_update: EventUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить существующее событие
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    db_event = result.scalar_one_or_none()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    # Обновляем только предоставленные поля
    update_data = event_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    await db.commit()
    await db.refresh(db_event)
    
    return db_event

@router.delete("/events/{event_id}", response_model=dict)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить событие
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    db_event = result.scalar_one_or_none()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    await db.delete(db_event)
    await db.commit()
    
    return {"message": "Событие успешно удалено"} 