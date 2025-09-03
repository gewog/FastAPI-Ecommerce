"""
API взаимодействия к категориями товаров
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category # Импортирую SQLAlchemy модель
from app.backend.db_depends import get_session # Импортирую функцию зависимость

session = Annotated[AsyncSession, Depends(get_session)] # Создаю сессию.


router = APIRouter(prefix="/category",
                   tags=["category 🍔🍑🍅"])

@router.get("/all_categories",  summary="Получить все категории продуктов")
async def get_all_categories(session: session):
    """API просмотра всех категорий"""
    res = select(Category)
    res2 = await session.execute(res)
    return res2.scalars().one().name

@router.post("/create", summary="Создать категорию продуктов")
async def create_category():
    """API создания категории"""
    ...

@router.put("/update_category",  summary="Обновить категорию продуктов")
async def update_category():
    """API обновления категории (частичное обновление)"""
    ...

@router.delete("/delete",  summary="Удалить категорию продуктов")
async def delete_category():
    """API удаления категории"""
    ...