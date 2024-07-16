import base64

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDbase
from app.crud.comment import comment_crud
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


async def validate_same_slugs(
        obj_slug: str,
        crud: CRUDbase,
        session: AsyncSession
):
    """Проверка на уникальность title."""
    obj = await crud.get_obj_by_slug(obj_slug, session)
    if obj is not None:
        raise HTTPException(
            status_code=422,
            detail='Группа с таким slug уже существует!',
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
        if not (obj.user_id == user.id or user.is_superuser):
            raise HTTPException(
                status_code=403,
                detail='У вас нет прав на редактирование!'
            )
    return obj


async def check_post_has_this_comment(
        post_id: int,
        comment_id: int,
        session: AsyncSession
):
    comment = await comment_crud.get_with_author(obj_id=comment_id, session=session)
    # Проверяем
    if comment:
        if not (comment["post"] == post_id):
            raise HTTPException(
                status_code=404,
                detail='У этого поста нет такого комментария'
            )
    else:
        raise HTTPException(
            status_code=404,
            detail='Такого комментария не существует'
        )
    return comment


async def validate_image(
        image: str,
):
    try:
        # Декодирование изображения из Base64
        ext, imgstr = image.split(';base64,')
        ext = ext.split('/')[-1]
        image_bytes = base64.b64decode(imgstr)
        image_path = "static/images/" + "123." + ext
        with open(image_path, "wb") as f:
            f.write(image_bytes)
            return image_path
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not decode image: {e}"
        )
