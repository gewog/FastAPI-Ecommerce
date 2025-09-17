"""
Модуль содержит SQLAlchemy-модель для работы с пользователями.
"""

from app.models.products import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """
    Модель пользователя для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя. Первичный ключ.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        username (str): Уникальное имя пользователя.
        email (str): Уникальный email пользователя.
        hashed_password (str): Хешированный пароль пользователя.
        is_active (bool): Флаг активности пользователя. По умолчанию `True`.
        is_admin (bool): Флаг, указывающий, является ли пользователь администратором. По умолчанию `False`.
        is_supplier (bool): Флаг, указывающий, является ли пользователь поставщиком. По умолчанию `False`.
        is_customer (bool): Флаг, указывающий, является ли пользователь покупателем. По умолчанию `True`.
        review (list[Review]): Список отзывов, оставленных пользователем. Связь "один ко многим" с таблицей `Review`.

    Отношения:
        Пользователь может оставлять множество отзывов (`review`).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_supplier = Column(Boolean, default=False)
    is_customer = Column(Boolean, default=True)
    # Новое
    review: Mapped[list["Review"]] = relationship(
        back_populates="user"
    )  # 1 продукт - много отзывов
