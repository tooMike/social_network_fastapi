from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase
from app.models.users import User


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
        session: AsyncSession,
        user: User | None = None,
):
    """Проверка существования объекта в БД с указанным id."""
    obj = await obj_crud.get(obj_id, session)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail='Объект с указанным id не найден!'
        )
    # Проверяем, имеет ли пользователь право редактировать объект
    if user:
        if not (obj.user_id ==  user.id or user.is_superuser):
            raise HTTPException(
                status_code=403,
                detail='У вас нет прав на редактирование!'
            )
    return obj
