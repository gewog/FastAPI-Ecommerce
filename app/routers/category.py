"""
API для взаимодействия с категориями товаров.
Предоставляет CRUD-операции для управления категориями продуктов.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from slugify import slugify

from app.schemas import CreateCategory

from app.models.category import Category  # Импортирую SQLAlchemy модель
from app.backend.db_depends import get_session  # Импортирую функцию зависимость


session = Annotated[AsyncSession, Depends(get_session)]  # Аннотация типа для зависимости сессии


router = APIRouter(prefix="/category", tags=["category 🍔🍑🍅"])


@router.get("/all_categories", summary="Получить все категории продуктов")
async def get_all_categories(session: session):
    """Возвращает список всех активных категорий продуктов.
    Args:
        session: Асинхронная сессия SQLAlchemy.
    Returns:
        List[Category]: Список объектов Category.
    Raises:
        HTTPException: Если не удалось выполнить запрос."""
    query = select(Category).where(Category.is_active == True)
    catherories = await session.execute(query)
    all_catherories = catherories.scalars().all()
    return all_catherories


@router.post("/create", summary="Создать категорию продуктов")
async def create_category(session: session, category: CreateCategory) -> dict:
    """Создает новую категорию продуктов.
    Args:
        session: Асинхронная сессия SQLAlchemy.
        category: Данные для создания категории.
    Returns:
        dict: Сообщение об успешном создании.
    Raises:
        HTTPException: Если не удалось создать категорию."""
    category_create = insert(Category).values(
        {
            "parent_id": category.parent_id,
            "name": category.name,
            "slug": slugify(category.name),
        },
    )
    await session.execute(category_create)
    await session.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update_category", summary="Обновить категорию продуктов")
async def update_category(session: session, category_id: int, new_data: CreateCategory):
    """Обновляет данные категории продуктов.
    Args:
        session: Асинхронная сессия SQLAlchemy.
        category_id: ID категории для обновления.
        new_data: Новые данные категории.
    Returns:
        dict: Сообщение об успешном обновлении.
    Raises:
        HTTPException: Если категория не найдена.
    """
    category_update = select(Category).where(Category.id == category_id)
    result = await session.execute(category_update)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no category found"
        )
    query = (
        update(Category)
        .values(
            {
                "parent_id": new_data.parent_id,
                "name": new_data.name,
                "slug": slugify(new_data.name),
            },
        )
        .filter_by(id=category_id)
    )
    await session.execute(query)
    await session.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Category update is successful",
    }


@router.delete("/delete", summary="Удалить категорию продуктов")
async def delete_category(session: session, category_id: int) -> dict:
    """Выполняет мягкое удаление категории (is_active=False).
    Args:
        session: Асинхронная сессия SQLAlchemy.
        category_id: ID категории для удаления.
    Returns:
        dict: Сообщение об успешном удалении.
    Raises:
        HTTPException: Если категория не найдена.
    """
    category_delete = select(Category).where(Category.id == category_id)
    result = await session.execute(category_delete)

    if not result.scalars().one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no category found"
        )
    query = update(Category).values(is_active=False).filter_by(id=category_id)
    await session.execute(query)
    await session.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Category delete is successful",
    }
