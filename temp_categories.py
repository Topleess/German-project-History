from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from ...db.database import get_db
from ...db.models import Category
from ..schemas import Category as CategorySchema, CategoryCreate

router = APIRouter()

@router.get("/categories", response_model=List[CategorySchema])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список категорий событий
    """
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    categories = result.scalars().all()

    return categories

@router.get("/categories/{category_id}", response_model=CategorySchema)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о конкретной категории по её ID
    """
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    return category

@router.post("/categories", response_model=CategorySchema)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новую категорию
    """
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)

    return db_category 