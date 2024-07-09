from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase


async def validate_same_names(
        obj_title: str,
        crud: CRUDbase,
        session: AsyncSession
):
    """Проверка на уникальность title."""
    obj = await crud.get_obj_by_title(obj_title, session)
    if obj is not None:
        raise HTTPException(
            status_code=422,
            detail='Группа с таким именем уже существует!',
        )


async def check_obj_exists_by_id(
        obj_id: int,
        obj_crud,
        session: AsyncSession
):
    """Проверка существования объекта в БД с указанным id."""
    obj = await obj_crud.get(obj_id, session)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail='Объект с указанным id не найден!'
        )
    return obj
