import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import category_router, product_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запущено")
    yield
    print("Приложение остановлено")

app = FastAPI(lifespan=lifespan, title="FastAPI-Ecommerce", debug=True, )

@app.get("/", tags=["TEST 👻"], summary="Тестовая апишка", description="Для теста")
async def main() -> dict:
    """Тестовая API"""
    return {"STATUS": "OK"}

# Подключаем роуты из category.py и products.py
app.include_router(category_router)
app.include_router(product_router)



# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
