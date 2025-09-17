"""
Модуль содержит SQLAlchemy-модель для работы с продуктами.
"""

from typing import Annotated

from sqlalchemy import Integer, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from app.models.category import Base


str_type = Annotated[str, mapped_column(String)]  # Кастомный тип данных 1
int_type = Annotated[int, mapped_column(Integer)]  # Кастомный тип данных 2


class Product(Base):
    """
    Модель продуктов для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор продукта. Первичный ключ.
        name (str): Название продукта.
        slug (str): Уникальный слаг (человекочитаемый идентификатор) продукта.
        description (str): Описание продукта.
        price (int): Цена продукта.
        image_url (str): URL изображения продукта.
        stock (int): Количество продукта на складе.
        supplier_id (int): Идентификатор поставщика. Внешний ключ, ссылающийся на таблицу `users`.
        rating (float): Рейтинг продукта.
        is_active (bool): Флаг активности продукта. По умолчанию `True`.
        category_id (int): Идентификатор категории. Внешний ключ, ссылающийся на таблицу `categories`.
        category (Category): Категория, к которой относится продукт. Связь "многие к одному" с таблицей `Category`.
        review (list[Review]): Список отзывов о продукте. Связь "один ко многим" с таблицей `Review`.

    Отношения:
        Продукт принадлежит одной категории (`category_id`) и может иметь множество отзывов (`review`).
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str_type]
    price: Mapped[int_type]
    image_url: Mapped[str_type]
    stock: Mapped[int_type]
    supplier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    rating: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    category: Mapped["Category"] = relationship(
        back_populates="product"
    )  # Отношение многие к 1 с таблицей Category

    review: Mapped[list["Review"]] = relationship(
        back_populates="product"
    )  # 1 продукт - много отзывов
