"""
API для взаимодействия с продуктами.
Предоставляет CRUD-операции для управления продуктами.
"""

from typing import Annotated, List, Dict, Any

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, insert, update, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from slugify import slugify

from app.schemas import CreateProduct

from app.models.category import Category
from app.models.products import Product  # Импортирую SQLAlchemy модель
from app.backend.db_depends import get_session  # Импортирую функцию зависимость


session = Annotated[
    AsyncSession, Depends(get_session)
]  # Аннотация типа для зависимости сессии


router = APIRouter(prefix="/products", tags=["products 🥭🍎🍐"])


@router.get("/", summary="Получить все продукты")  # Done
async def all_products(session: session):
    """Получение всех активных продуктов с ненулевым остатком.
    Returns:
        List[Product]: Список объектов Product.
    Raises:
        HTTPException: Если продукты не найдены.
    """
    products = select(Product).where(and_(Product.is_active == True, Product.stock > 0))
    query = await session.execute(products)
    products_all = query.scalars().all()
    if not products_all:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )
    return products_all


@router.post("/create", summary="Создать продукт")  # Done
async def create_product(
    session: session, product: CreateProduct
) -> Dict[str, Any]:
    """Создание нового продукта.
    Args:
        product (CreateProduct): Схема создания продукта.
    Returns:
        Dict[str, Any]: Статус и сообщение об успехе.
    Raises:
        HTTPException: Если категория не найдена.
    """
    category_query = select(Category).where(Category.id == product.category)
    category_result = await session.execute(category_query)
    category = category_result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {product.category} не найдена",
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
            "category_id": product.category,
        },
    )
    await session.execute(product_create)
    await session.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.get("/{category_slug}", summary="Получить продукты определенной категории")
async def product_by_category(
    session: session, category_slug: str
) -> List[Dict[int, str]]:
    """API получения товаров определенной категории"""
    id_list = []
    prod_list = []
    check_category = select(Category).filter_by(slug=category_slug)
    check_query = await session.execute(check_category)
    check_result = check_query.scalars().one_or_none()
    if check_result is not None:
        id_list.append(int(check_result.id))
        print(id_list)

        check_subcategory = select(Category).where(Category.parent_id == id_list[0])
        check_subquery = await session.execute(check_subcategory)
        check_subresult = check_subquery.scalars().all()
        print(check_subresult)

        if check_subresult is not None:
            for el in check_subresult:
                id_list.append(int(el.id))
        print(id_list)
        all_products_by_id = select(Product).where(
            and_(
                Product.category_id.in_(id_list),
                Product.is_active == True,
                Product.stock > 0,
            )
        )
        res_query = await session.execute(all_products_by_id)
        res_scal = res_query.scalars().all()
        for el in res_scal:
            prod_list.append({el.id: el.name})
            print(prod_list)
        return prod_list

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )


@router.get("/detail/{product_slug}", summary="Получить детальную информацию о товаре")
async def product_detail(
    session: session, product_slug: str
) -> Dict[str, str]:
    """Получение детальной информации о продукте по его slug.
    Args:
        product_slug (str): Slug продукта.
    Returns:
        Dict[str, str]: Детальная информация о продукте.
    Raises:
        HTTPException: Если продукт не найден.
    """
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
async def update_product(
    session: session, product_slug: str, product: CreateProduct
) -> Dict[str, str]:
    """Обновление информации о продукте.
    Args:
        product_slug (str): Slug продукта.
        product (CreateProduct): Новые данные продукта.
    Returns:
        Dict[str, str]: Сообщение об успехе.
    Raises:
        HTTPException: Если продукт не найден.
    """
    check_query = select(Product).filter_by(slug=product_slug)
    query = await session.execute(check_query)
    result = query.scalars().one_or_none()
    if result:
        new_product = (
            update(Product)
            .values(
                {
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "image_url": product.image_url,
                    "stock": product.stock,
                    "rating": 0.0,
                    "category_id": product.category,
                },
            )
            .filter_by(slug=product_slug)
        )
        await session.execute(new_product)
        await session.commit()
        return {"Детальная информация": result.description}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found"
        )


@router.delete("/delete", summary="Удалить товар")
async def delete_product(
    session: session, product_slug: str
) -> Dict[str, Any]:
    """Удаление продукта по его slug.
    Args:
        product_slug (str): Slug продукта.
    Returns:
        Dict[str, Any]: Статус и сообщение об успехе.
    Raises:
        HTTPException: Если продукт не найден.
    """
    check_product = select(Product).filter_by(slug=product_slug)
    check_query = await session.execute(check_product)
    result = check_query.scalars().one_or_none()
    print(result)
    if result is not None:
        product_delete = delete(Product).filter_by(slug=product_slug)
        query = await session.execute(product_delete)
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Product delete is successful",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found"
        )
