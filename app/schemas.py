"""
Pydantic модели для категорий и продуктов
"""

from pydantic import BaseModel


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
