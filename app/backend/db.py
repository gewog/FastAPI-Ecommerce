"""
Основнйо файл работы с бд
"""

import asyncio

from sqlalchemy import text, select
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.backend.settings import setting  # Экземпляр класса Settings

from app.models.category import Category
from app.models.products import Product
from app.models.user import User
from app.models.review import Review, Base

engine = create_async_engine(setting.get_path, echo=False)
session = async_sessionmaker(bind=engine)


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

async def get_version():
    """Тестовое получение версии постгерс
       Необходиом удалить эту функцию
    """
    async with session() as ss:
        res = await ss.execute(text("select version();"))
        print(res.fetchone())

async def get_data(id: int) -> str:
    """Тестовое получение данных из таблицы Категории продуктов
       Необходимо дропнуть данные из таблицы и удалить эту функцию
    """
    async with session() as ss:
        res = await ss.get(Category, id)
        print(res.name)


if __name__ == "__main__":
    try:
        ...
    except Exception as e:
        print(e)
