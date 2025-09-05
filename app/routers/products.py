"""
API для взаимодействия с продуктами.
Предоставляет CRUD-операции для управления продуктами.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, insert, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from slugify import slugify

from app.schemas import CreateProduct

from app.models.category import Category
from app.models.products import Product  # Импортирую SQLAlchemy модель
from app.backend.db_depends import get_session  # Импортирую функцию зависимость


session = Annotated[AsyncSession, Depends(get_session)]  # Аннотация типа для зависимости сессии



router = APIRouter(prefix="/products", tags=["products 🥭🍎🍐"])

@router.get("/", summary="Получить все продукты") # Done
async def all_products(session: session):
    """получения всех товаров с условием"""
    products = select(Product).where(
        and_(Product.is_active == True,
             Product.stock > 0)
    )
    query = await session.execute(products)
    products_all = query.scalars().all()
    if not products_all:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )
    return products_all


@router.post("/create", summary="Создать продукт") # Done
async def create_product(session: session, product: CreateProduct) -> dict:
    """API создания товара"""
    category_query = select(Category).where(Category.id == product.category)
    category_result = await session.execute(category_query)
    category = category_result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {product.category} не найдена"
        )
    product_create = insert(Product).values(
        {
            "name": product.name,
            "slug": slugify(product.name),
            "description": product.description,
            "price": product.price,
            "image_url": product.image_url,
            "stock": product.stock,
            "rating": 0.0,
            "category_id": product.category

        },
    )
    await session.execute(product_create)
    await session.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}



@router.get("/{category_slug}", summary="Получить продукты определенной категории")
async def product_by_category(category_slug: str):
    """API получения товаров определенной категории"""
    ...


@router.get("/detail/{product_slug}", summary="Получить детальную информацию о товаре")
async def product_detail(session: session, product_slug: str):
    """API получения детальной информации о товаре"""
    detail = select(Product).filter_by(slug=product_slug)
    query = await session.execute(detail)
    result = query.scalars().one_or_none()
    if result:
        return {"Детальная информация": result.description}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )



@router.put("/detail/{product_slug}", summary="Изменить информацию о товаре")
async def update_product(session: session, product_slug: str, product: CreateProduct):
    """API изменения товара"""
    check_query = select(Product).filter_by(slug=product_slug)
    query = await session.execute(check_query)
    result = query.scalars().one_or_none()
    if result:
        new_product = update(Product).values(
            {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "image_url": product.image_url,
                "stock": product.stock,
                "rating": 0.0,
                "category_id": product.category
            },
        ).filter_by(slug=product_slug)
        await session.execute(new_product)
        await session.commit()
        return {"Детальная информация": result.description}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found"
        )


@router.delete("/delete", summary="Удалить товар")
async def delete_product(product_id: int):
    """API удаления товара"""
    pass