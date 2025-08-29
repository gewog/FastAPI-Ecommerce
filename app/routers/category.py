"""
API взаимодействия к категориями товаров
"""
from fastapi import APIRouter

router = APIRouter(prefix="/category",
                   tags=["category 🍔🍑🍅"])

@router.get("/all_categories",  summary="Получить все категории продуктов")
async def get_all_categories():
    """API просмотра всех категорий"""
    ...

@router.post("/create", summary="Создать категорию продуктов")
async def create_category():
    """API создания категории"""
    ...

@router.put("/update_category",  summary="Обновить категорию продуктов")
async def update_category():
    """API обновления категории (частичное обновление)"""
    ...

@router.delete("/delete",  summary="Удалить категорию продуктов")
async def delete_category():
    """API удаления категории"""
    ...