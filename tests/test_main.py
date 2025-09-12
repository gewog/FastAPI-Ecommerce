import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app

# Инициализируем синхронный клиент для тестирования FastAPI-приложения.
# Используется для синхронных тестов (закомментированный пример ниже).
client: TestClient = TestClient(app)

@pytest.mark.asyncio
async def test_main() -> None:
    """
    Асинхронный тест для проверки корневой ручки (endpoint) `/` FastAPI-приложения.

    Использует `httpx.AsyncClient` с `ASGITransport` для выполнения асинхронных запросов.
    Проверяет, что:
    - Статус-код ответа равен 200 (OK).
    - Тело ответа соответствует ожидаемому JSON: `{"STATUS": "OK"}`.

    Returns:
        None: Тест не возвращает значения, но выбрасывает `AssertionError` при неудаче.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        response = await async_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"STATUS": "OK"}

# def test_main_router() -> None:
#     """
#     Синхронный тест для проверки корневой ручки (endpoint) `/` FastAPI-приложения.
#
#     Использует `TestClient` для выполнения синхронных запросов.
#     Проверяет, что:
#         - Статус-код ответа равен 200 (OK).
#         - Тело ответа соответствует ожидаемому JSON: `{"STATUS": "OK"}`.
#
#     Returns:
#         None: Тест не возвращает значения, но выбрасывает `AssertionError` при неудаче.
#     """
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"STATUS": "OK"}


