from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Схемы для категорий
class CategoryBase(BaseModel):
    name: str
    color: str = "#3498db"
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Схемы для событий
class EventBase(BaseModel):
    title: str
    date: datetime
    end_date: Optional[datetime] = None
    description: str
    location: Optional[str] = None
    importance: int = 1
    image_url: Optional[str] = None
    category_id: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    location: Optional[str] = None
    importance: Optional[int] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EventDetail(Event):
    category: Category
    causes: List['ConnectionBase'] = []
    effects: List['ConnectionBase'] = []
    
    class Config:
        from_attributes = True

# Схемы для связей
class ConnectionBase(BaseModel):
    cause_id: int
    effect_id: int
    description: Optional[str] = None
    strength: int = 1

class ConnectionCreate(ConnectionBase):
    pass

class Connection(ConnectionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConnectionDetail(Connection):
    cause: Event
    effect: Event
    
    class Config:
        from_attributes = True

# Обновляем ссылки на EventDetail
EventDetail.update_forward_refs() 