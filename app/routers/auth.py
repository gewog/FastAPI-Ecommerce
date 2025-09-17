"""
Модуль аутентификации для регистрации и авторизации пользователей.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext


from app.models.user import User
from app.schemas import CreateUser, UserResponse


from app.backend.db_depends import get_session  # Импортирую функцию зависимость

session = Annotated[
    AsyncSession, Depends(get_session)
]  # Аннотация типа для зависимости сессии


router = APIRouter(prefix="/auth", tags=["auth 🤷🤷‍♂️👶"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()  # Всплывающая форма входа


@router.post("/", summary="Создать пользователя")
async def create_user(session: session, new_user: CreateUser) -> dict | str:
    """
    Создает нового пользователя в базе данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.
        new_user (CreateUser): Данные пользователя для регистрации.

    Возвращает:
        dict | str: Словарь с кодом статуса и результатом транзакции или сообщение об ошибке.

    Исключения:
        Возвращает сообщение об ошибке в случае исключения.
    """
    query = insert(User).values(
        [
            {
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "username": new_user.username,
                "email": new_user.email,
                "hashed_password": bcrypt_context.hash(new_user.password),
            },
        ],
    )
    try:
        await session.execute(query)
        await session.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    except Exception as e:
        return f"Произошла ошибка: {e}."


async def get_current_username(
    session: session, credentials: HTTPBasicCredentials = Depends(security)
):
    """
    Аутентифицирует пользователя на основе предоставленных учетных данных.

    Аргументы:
        session (AsyncSession): Асинхронная сессия базы данных.
        credentials (HTTPBasicCredentials): Учетные данные для HTTP Basic Authentication.

    Возвращает:
        User: Объект пользователя, если аутентификация прошла успешно.

    Исключения:
        HTTPException: Возникает, если аутентификация не удалась.
    """
    user = await session.scalar(
        select(User).where(User.username == credentials.username)
    )
    if not user or not bcrypt_context.verify(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не авторизованы"
        )
    return user


@router.get("/users/me")
async def read_current_user(user: str = Depends(get_current_username)) -> dict:
    """
    Возвращает данные текущего аутентифицированного пользователя.

    Аргументы:
        user (User): Объект текущего аутентифицированного пользователя.

    Возвращает:
        dict: Словарь, содержащий данные пользователя.
    """
    return {"User": UserResponse.model_validate(user)}
