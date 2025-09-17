"""
Модуль содержит SQLAlchemy-модель для работы с категориями продуктов.
"""

from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.

    Наследуясь от этого класса, другие классы становятся SQLAlchemy-моделями,
    которые могут быть преобразованы в таблицы базы данных.
    """

    pass


from sqlalchemy.schema import CreateTable


class Category(Base):
    """
    Модель категорий продуктов (подкатегорий) для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор категории. Первичный ключ.
        parent_id (int): Идентификатор родительской категории. Внешний ключ, ссылающийся на `id` этой же таблицы.
        name (str): Название категории.
        slug (str): Уникальный слаг (человекочитаемый идентификатор) категории.
        is_active (bool): Флаг активности категории. По умолчанию `True`.
        product (list[Product]): Список продуктов, относящихся к данной категории. Связь "один ко многим" с таблицей `Product`.

    Отношения:
        Категория может содержать подкатегории (через `parent_id`) и продукты (через `product`).
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    parent_id: Mapped[int] = mapped_column(
        Integer,  # Из класса категории сделать подкласс категории
        ForeignKey("categories.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    product: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )  # Отношение 1 к многим с таблицей Product


# Раскомментируйте следующую строку для вывода SQL-запроса создания таблицы
# print(CreateTable(Category.__table__).compile(compile_kwargs={"literal_binds": True}))
