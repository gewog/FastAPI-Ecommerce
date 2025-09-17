"""
Модуль содержит SQLAlchemy-модель для работы с отзывами о продуктах.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    DateTime,
    text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import Base


class Review(Base):
    """
    Модель отзывов о продуктах для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор отзыва. Первичный ключ.
        user_id (int): Идентификатор пользователя, оставившего отзыв. Внешний ключ, ссылающийся на таблицу `users`.
        product_id (int): Идентификатор продукта, к которому относится отзыв. Внешний ключ, ссылающийся на таблицу `products`.
        rating (float): Оценка продукта в отзыве.
        comment (str): Текст комментария к продукту. Максимальная длина 255 символов.
        comment_date (datetime): Дата и время создания отзыва. По умолчанию устанавливается текущее время на сервере.
        is_active (bool): Флаг активности отзыва. По умолчанию `True`.
        product (Product): Продукт, к которому относится отзыв. Связь "многие к одному" с таблицей `Product`.
        user (User): Пользователь, оставивший отзыв. Связь "многие к одному" с таблицей `User`.

    Отношения:
        Отзыв принадлежит одному пользователю (`user_id`) и одному продукту (`product_id`).
    """

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[float] = mapped_column(Float)
    comment: Mapped[str] = mapped_column(String(255), nullable=False)
    comment_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    product: Mapped["Product"] = relationship(back_populates="review")
    user: Mapped["User"] = relationship(back_populates="review")
