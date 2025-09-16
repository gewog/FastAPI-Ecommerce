"""
Модуль для работы с базой данных.

Этот модуль предоставляет функции для инициализации таблиц,
тестирования подключения к PostgreSQL и получения данных из базы.
"""

from typing import Optional

from sqlalchemy import text
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
    """
    Создаёт все таблицы в базе данных на основе моделей SQLAlchemy.

    Использует `Base.metadata.create_all()` для создания таблиц.
    В случае ошибки выводит сообщение об ошибке.

    Raises:
        Exception: Если произошла ошибка при создании таблиц.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


async def get_version() -> None:
    """
    Тестовая функция для получения версии PostgreSQL.

    Выполняет запрос `SELECT version();` и выводит результат в консоль.
    Эта функция предназначена для проверки подключения к базе данных
    и должна быть удалена после завершения тестирования.
    """
    async with session() as ss:
        res = await ss.execute(text("select version();"))
        print(res.fetchone())


async def get_data(id: int) -> Optional[str]:
    """
    Тестовая функция для получения данных из таблицы категорий продуктов.

    Args:
        id (int): Идентификатор категории.

    Returns:
        Optional[str]: Название категории, если найдена, иначе None.

    Notes:
        Эта функция предназначена для тестирования и должна быть удалена
        после завершения разработки. Также необходимо очистить тестовые данные.
    """
    async with session() as ss:
        res: Optional[Category] = await ss.get(Category, id)
        if res:
            print(res.name)
            return res.name
        return None
