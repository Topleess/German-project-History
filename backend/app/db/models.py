from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Таблица для категорий событий
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, unique=True)
    color = Column(String(7), default="#3498db")  # Цветовой код в формате HEX
    description = Column(Text, nullable=True)
    
    # Связь с событиями
    events = relationship("Event", back_populates="category")
    
    def __repr__(self):
        return f"<Category {self.name}>"

# Таблица для исторических событий (узлов графа)
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    date = Column(DateTime, index=True)
    end_date = Column(DateTime, nullable=True)  # Для событий с продолжительностью
    description = Column(Text)
    location = Column(String(200), nullable=True)
    importance = Column(Integer, default=1)  # Значимость события (может влиять на размер узла в графе)
    image_url = Column(String(500), nullable=True)  # URL к изображению события
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Связи
    category = relationship("Category", back_populates="events")
    causes = relationship(
        "Connection",
        foreign_keys="Connection.effect_id",
        back_populates="effect",
    )
    effects = relationship(
        "Connection",
        foreign_keys="Connection.cause_id",
        back_populates="cause",
    )
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Event {self.title}>"

# Таблица для связей между событиями (рёбра графа)
class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(Integer, primary_key=True, index=True)
    cause_id = Column(Integer, ForeignKey("events.id"), index=True)
    effect_id = Column(Integer, ForeignKey("events.id"), index=True)
    description = Column(Text, nullable=True)  # Описание связи
    strength = Column(Integer, default=1)  # Сила связи (может влиять на толщину линии в графе)
    
    # Связи с событиями
    cause = relationship("Event", foreign_keys=[cause_id], back_populates="effects")
    effect = relationship("Event", foreign_keys=[effect_id], back_populates="causes")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Connection {self.id}: {self.cause_id} -> {self.effect_id}>" 