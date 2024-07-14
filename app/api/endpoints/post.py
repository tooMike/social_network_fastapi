from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_exists_by_id
from app.core.db import get_async_session
from app.core.users import current_user
from app.crud.post import post_crud
from app.models.users import User
from app.schemas.post import PostCreate, PostDB, PostUpdate

router = APIRouter()


@router.post('/', response_model=PostDB)
async def create_post(
        post: PostCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    post = await post_crud.create(obj_in=post, user=user, session=session)
    return post


@router.get('/', response_model=List[PostDB])
async def get_posts(
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка постов."""
    posts = await post_crud.get_list(session=session)
    return posts


@router.get('/{post_id}', response_model=PostDB)
async def get_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Получение конкретного поста."""
    await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        session=session
    )
    post = await post_crud.get(obj_id=post_id, session=session)
    return post


@router.patch('/{post_id}', response_model=PostDB)
async def patch_post(
        post_id: int,
        obj_in: PostUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление данные поста."""
    post = await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        session=session,
        user=user
    )
    post = await post_crud.update(obj_in=obj_in, db_obj=post, session=session)
    return post


@router.delete('/{post.id}', response_model=PostDB)
async def delete_post(
        post_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление поста."""
    post = await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        user=user,
        session=session,
    )
    post = await post_crud.delete(db_obj=post, session=session)
    return post
