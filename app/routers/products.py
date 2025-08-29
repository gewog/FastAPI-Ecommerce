"""
API взаимодействия с товарами (продуктами)
"""
from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products 🥭🍎🍐"])

@router.get("/", summary="Получить все продукты")
async def all_products():
    """получения всех товаров"""
    pass


@router.post("/create", summary="Создать продукт")
async def create_product():
    """API создания товара"""
    pass


@router.get("/{category_slug}", summary="Получить продукты определенной категории")
async def product_by_category(category_slug: str):
    """API получения товаров определенной категории"""
    pass


@router.get("/detail/{product_slug}", summary="Получить детальную информацию о товаре")
async def product_detail(product_slug: str):
    """API получения детальной информации о товаре"""
    pass


@router.put("/detail/{product_slug}", summary="Изменить информацию о товаре")
async def update_product(product_slug: str):
    """API изменения товара"""
    pass


@router.delete("/delete", summary="Удалить товар")
async def delete_product(product_id: int):
    """API удаления товара"""
    pass