"""
Модель отзыва
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import Base


class Review(Base):
    """SQLAlchemy модель отзывов"""
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    rating: Mapped[float] = mapped_column(Float)
    comment: Mapped[str] = mapped_column(String(255), nullable=False)
    comment_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    product: Mapped["Product"] = relationship(back_populates="review")
    user: Mapped["User"] = relationship(back_populates="review")