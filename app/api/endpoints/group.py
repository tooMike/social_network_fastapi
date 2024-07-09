from fastapi import APIRouter

from app.crud.group import create_group, read_all_groups
from app.schemas.group import Group

router = APIRouter()

@router.post("/")
async def create_new_group(
        new_group: Group
):
    """Создание новой группы."""

    new_group = await create_group(new_group)
    return new_group

@router.get("/")
async def gel_all_groups():
    """Получение списка всех групп."""

    groups_list = await read_all_groups()
    return groups_list
