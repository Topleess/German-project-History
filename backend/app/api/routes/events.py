from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from datetime import datetime

from ...db.database import get_db
from ...db.models import Event, Category
from ..schemas import Event as EventSchema, EventCreate, EventDetail, EventUpdate

router = APIRouter()

@router.get("/events/", response_model=List[EventSchema])
async def read_events(
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список исторических событий с возможностью фильтрации
    """
    query = select(Event)
    
    # Применяем фильтры, если они указаны
    if category_id:
        query = query.where(Event.category_id == category_id)
    if start_date:
        query = query.where(Event.date >= start_date)
    if end_date:
        query = query.where(Event.date <= end_date)
    if search:
        query = query.where(Event.title.ilike(f"%{search}%") | Event.description.ilike(f"%{search}%"))
    
    # Добавляем пагинацию
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    return events

@router.get("/events/{event_id}", response_model=EventDetail)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить детальную информацию о конкретном событии по его ID
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalars().first()
    
    if event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    return event

@router.post("/events/", response_model=EventSchema)
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новое историческое событие
    """
    # Проверяем, существует ли указанная категория
    category_query = select(Category).where(Category.id == event.category_id)
    category_result = await db.execute(category_query)
    category = category_result.scalars().first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Указанная категория не существует")
    
    # Создаем новое событие
    db_event = Event(**event.model_dump())
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
    Обновить существующее историческое событие
    """
    # Проверяем, существует ли событие
    event_query = select(Event).where(Event.id == event_id)
    event_result = await db.execute(event_query)
    db_event = event_result.scalars().first()
    
    if db_event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    # Если указана категория, проверяем её существование
    if event_update.category_id is not None:
        category_query = select(Category).where(Category.id == event_update.category_id)
        category_result = await db.execute(category_query)
        category = category_result.scalars().first()
        
        if category is None:
            raise HTTPException(status_code=404, detail="Указанная категория не существует")
    
    # Обновляем только переданные поля
    update_data = event_update.model_dump(exclude_unset=True)
    if update_data:
        update_query = update(Event).where(Event.id == event_id).values(update_data)
        await db.execute(update_query)
        await db.commit()
    
    # Получаем обновленное событие
    result = await db.execute(event_query)
    updated_event = result.scalars().first()
    
    return updated_event

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить историческое событие
    """
    # Проверяем, существует ли событие
    event_query = select(Event).where(Event.id == event_id)
    event_result = await db.execute(event_query)
    db_event = event_result.scalars().first()
    
    if db_event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    # Удаляем событие
    delete_query = delete(Event).where(Event.id == event_id)
    await db.execute(delete_query)
    await db.commit()
    
    return {"ok": True, "message": "Событие успешно удалено"} 