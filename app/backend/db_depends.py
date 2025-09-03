"""
Модуль для предоставления асинхронной сессии базы данных.

Этот модуль содержит функцию для создания и управления асинхронными сессиями SQLAlchemy,
которые используются для взаимодействия с базой данных в асинхронном режиме.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db import session

async def get_session() -> AsyncSession:
    """
    Асинхронная функция зависимости для FastAPI, предоставляющая сессию SQLAlchemy.
    Создаёт новую асинхронную сессию SQLAlchemy и управляет её жизненным циклом.
    Сессия автоматически закрывается после завершения запроса.
    """
    async with session() as ss:
        try:
            yield ss
        finally:
            await ss.close() # Закрывает сессию при ошибке

