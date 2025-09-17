"""
Pydantic модели для категорий, продуктов, отзывов
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CreateCategory(BaseModel):
    """Класс-модель создания категории"""

    name: str
    parent_id: int | None


class CreateProduct(BaseModel):
    """Класс-модель создания продукта"""

    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateUser(BaseModel):
    """Класс-модель создания пользователя"""

    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """Модель ответа для пользователя"""

    id: int
    first_name: str
    last_name: str
    username: str
    email: str

    class Config:
        from_attributes = True  # Позволяет создавать объект из ORM-объекта


class UsersReview(BaseModel):
    """Класс-модель создания отзыва"""

    id: int
    rating: float = Field(ge=0, le=10)
    comment: str
    user_id: int
    product_id: int
    is_active: bool = True
    comment_date: Optional[datetime] = None
