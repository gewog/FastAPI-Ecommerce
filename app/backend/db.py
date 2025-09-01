import asyncio

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.backend.settings import setting  # Экземпляр класса Settings

from app.models.category import Category, Base
from app.models.products import Product, Base

engine = create_async_engine(setting.get_path, echo=True)
session = async_sessionmaker(bind=engine)


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

async def get_version():
    """Тестовое получение версии постгерс"""
    async with session() as ss:
        res = await ss.execute(text("select version();"))
        print(res.fetchone())


if __name__ == "__main__":
    asyncio.run(create_tables())
