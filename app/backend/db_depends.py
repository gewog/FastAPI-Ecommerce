"""
Модуль для предоставления асинхронной сессии базы данных в FastAPI-приложении.

Этот модуль содержит зависимость `get_session`, которая используется для инъекции асинхронной сессии SQLAlchemy
в обработчики запросов. Сессия создаётся при каждом запросе и автоматически закрывается после его завершения,
обеспечивая безопасное управление соединением с базой данных в асинхронной среде.

Используется совместно с `sqlalchemy.ext.asyncio.AsyncSession` и `async_generator` для корректного жизненного цикла сессии.
Гарантирует, что каждое HTTP-запроса получает изолированную сессию, предотвращая утечки ресурсов и конфликты транзакций.

Пример использования:
    from fastapi import Depends
    from .dependencies import get_session

    async def some_endpoint(session: AsyncSession = Depends(get_session)):
        # Работа с базой данных через session
        result = await session.execute(select(User))
        return result.scalars().all()
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
            await ss.close()  # Закрывает сессию при ошибке
