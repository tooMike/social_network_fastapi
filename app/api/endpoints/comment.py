from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_obj_exists_by_id,
    check_post_has_this_comment,
)
from app.core.db import get_async_session
from app.core.users import current_user
from app.crud.comment import comment_crud
from app.crud.post import post_crud
from app.models.users import User
from app.schemas.comment import CommentCreate, CommentDB

router = APIRouter()


@router.post('/{post_id}/comment', response_model=CommentDB)
async def create_comment(
        post_id: int,
        obj_in: CommentCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Добавление комментария к посту."""
    post = await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        user=user,
        session=session
    )
    comment = await comment_crud.create(
        obj_in=obj_in,
        post=post,
        user=user,
        session=session
    )
    return comment


@router.get('/{post_id}/comments/', response_model=List[CommentDB])
async def get_all_comments(
        post_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка комментариев к посту."""
    post = await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        session=session
    )
    comments = await comment_crud.get_list_with_author(
        post=post,
        session=session
    )
    return comments


@router.get("/{post_id}/comments/{comment_id}")
async def get_comment(
        comment_id: int,
        post_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Получение конкретного комментария"""
    # Проверяем, что такой пост существует
    await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        session=session
    )
    comment = await check_post_has_this_comment(
        comment_id=comment_id,
        post_id=post_id,
        session=session
    )
    return comment
