"""
Модель SQLAlchemy продуктов
"""
from typing import Annotated

from sqlalchemy import (Integer, ForeignKey, String, Boolean, Float)
from sqlalchemy.orm import (Mapped, mapped_column, relationship, DeclarativeBase)

from app.models.category import Base


str_type = Annotated[str, mapped_column(String)] # Кастомный тип данных 1
int_type = Annotated[int, mapped_column(Integer)] # Кастомный тип данных 2


class Product(Base):
    """SQLAlchemy модель продуктов"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str_type]
    price: Mapped[int_type]
    image_url: Mapped[str_type]
    stock: Mapped[int_type]
    supplier_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id',
                                                                  ondelete="CASCADE"), nullable=True)
    rating: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(
        back_populates="product") # Отношение многие к 1 с таблицей Category