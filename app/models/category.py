"""
Модель SQLAlchemy категорий
"""
from sqlalchemy import (Integer, ForeignKey, String, Boolean)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship)

class Base(DeclarativeBase):
    """Устанавливаем базовый класс"""
    pass

from sqlalchemy.schema import CreateTable
class Category(Base):
    """SQLAlchemy модель катеорий продуктов"""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    parent_id:Mapped[int] = mapped_column(Integer, # Из класса категории сделать подкласс категории
                                          ForeignKey("categories.id", ondelete="CASCADE", onupdate="CASCADE"),
                                          nullable=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    product: Mapped[list["Product"]] = relationship(
        back_populates="category") # Отношение 1 к многим с таблицей Product

print(CreateTable(Category.__table__))