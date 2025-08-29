import asyncio

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from settings import setting  # Экземпляр класса Settings


engine = create_async_engine(setting.get_path, echo=True)
session = async_sessionmaker(bind=engine)


async def get_version():
    """Тестовое получение версии постгерс"""
    async with session() as ss:
        res = await ss.execute(text("select version();"))
        print(res.fetchall())


if __name__ == "__main__":
    asyncio.run(get_version())
