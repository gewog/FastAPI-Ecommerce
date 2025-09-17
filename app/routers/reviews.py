"""
API для взаимодействия с отзывами о товарах.
Предоставляет методы для добавления, получения и удаления отзывов, а также обновления рейтинга товаров.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import select, insert, update, func, cast, Numeric
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas import UsersReview  # Класс-модель создания отзыва

from app.models.review import Review  # Импортирую SQLAlchemy модель
from app.models.products import Product
from app.backend.db_depends import get_session  # Импортирую функцию зависимость

from app.routers.auth import get_current_username  # Получение пользователя


session = Annotated[
    AsyncSession, Depends(get_session)
]  # Аннотация типа для зависимости сессии


router = APIRouter(prefix="/review", tags=["review 💘💖💔"])


async def update_rating(session: AsyncSession, product_id: int) -> None:
    """
    Обновляет рейтинг продукта на основе среднего значения оценок из отзывов.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.
        product_id (int): Идентификатор продукта, для которого нужно обновить рейтинг.

    Возвращает:
        None
    """
    # 1. Вычисляем средний рейтинг
    stmt = (
        select(func.avg(cast(Review.rating, Numeric)).label("average_rating"))
        .where(Review.product_id == product_id)
        .where(Review.is_active == True)
    )
    result = await session.execute(stmt)
    average_rating = result.scalars().first()

    # 2. Обновляем рейтинг продукта (если средний рейтинг не None)
    if average_rating is not None:
        update_stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(
                rating=average_rating
            )  # Исправлено: обновляем поле `rating`, а не `id`!
        )
        await session.execute(update_stmt)
        await session.commit()


@router.get(
    "/all_reviews", summary="Метод получения всех отзывов и рейтингов о товарах"
)
async def all_reviews(session: session):
    """
    Возвращает все активные отзывы о товарах.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.

    Возвращает:
        dict: Словарь, где ключи - идентификаторы отзывов, а значения - информация о продукте, рейтинге, комментарии и дате.

    Исключения:
        HTTPException: Возникает, если отзывов нет.
    """
    comments = {}
    query = select(Review).where(Review.is_active == True)
    result = await session.execute(query)
    scal_res = result.scalars().all()

    if scal_res:
        for el in scal_res:
            scal_res = result.scalars().all()
            prod_name = await session.execute(
                select(Product).where(Product.id == el.product_id)
            )
            product = prod_name.scalars().one()
            comments[el.id] = {
                "product": product.name,
                "rating": el.rating,
                "comment": el.comment,
                "comment data": el.comment_date,
            }
        return comments
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no reviews."
        )


@router.post(
    "/add_review", summary="Метод добавления отзыва и рейтинга об определенном товаре"
)
async def add_review(
    session: session,
    review: UsersReview,
    user: Annotated[get_current_username, Depends(get_current_username)],
) -> dict:
    """
    Добавляет новый отзыв о товаре.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.
        review (UsersReview): Данные отзыва для добавления.
        user (dict): Текущий аутентифицированный пользователь.

    Возвращает:
        dict: Словарь с кодом статуса и результатом транзакции.

    Исключения:
        HTTPException: Возникает, если пользователь не является покупателем или продукт не найден.
    """
    if not user.is_customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method.",
        )
    potential_product = select(Product).where(Product.id == review.product_id)
    query = await session.execute(potential_product)
    result = query.scalars().one_or_none()
    if result:
        insert_query = await session.execute(
            insert(Review).values(
                [
                    {
                        "user_id": review.user_id,
                        "product_id": review.product_id,
                        "rating": review.rating,
                        "comment": review.comment,
                    },
                ]
            )
        )
        await session.commit()
        await update_rating(session, review.product_id)
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no product"
        )


@router.patch(
    "/delete_reviews", summary="Метод удаления отзыва и рейтинга об определенном товаре"
)
async def delete_reviews(
    session: session,
    user: Annotated[get_current_username, Depends(get_current_username)],
    review_id: int,
):
    """
    Деактивирует отзыв (устанавливает is_active = False).

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.
        user (dict): Текущий аутентифицированный пользователь.
        review_id (int): Идентификатор отзыва, который нужно удалить.

    Возвращает:
        dict: Словарь с кодом статуса и результатом транзакции.

    Исключения:
        HTTPException: Возникает, если пользователь не является администратором или отзыв не найден.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method.",
        )
    check_query = await session.execute(select(Review).filter_by(id=review_id))
    answer_query = check_query.scalars().one_or_none()
    if not answer_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no review"
        )
    query = (
        update(Review)
        .values(
            {"is_active": False},
        )
        .filter_by(id=review_id)
    )
    await session.execute(query)
    await session.commit()

    query_for_recount = await session.execute(
        select(Review).where(Review.id == review_id)
    )
    review_for_recount = query_for_recount.scalars().one()
    await update_rating(session, review_for_recount.product_id)
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Review delete is successful",
    }


@router.get(
    "/products_reviews/{slug}",
    summary="Метод получения отзывов и его рейтингов об определенном товаре",
)
async def products_reviews(session: session, slug: str):
    """
    Возвращает отзывы и рейтинги для определенного товара по его слагу.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.
        slug (str): Уникальный слаг продукта.

    Возвращает:
        dict: Словарь с названием продукта и списком отзывов.

    Исключения:
        HTTPException: Возникает, если продукт не найден.
    """
    product_revies = {}
    query = select(Product).where(Product.slug == slug, Product.is_active == True)
    result = await session.execute(query)
    product = result.scalars().one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product with this slug",
        )
    product_revies[product.name] = []
    review_query = await session.execute(
        select(Review).where(Review.product_id == product.id, Review.is_active == True)
    )
    reviews = review_query.scalars().all()
    for review in reviews:
        product_revies[product.name].append(
            {"Rating": review.rating, "Comment": review.comment}
        )
    return product_revies
