from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_exists_by_id, validate_image
from app.core.db import get_async_session
from app.core.users import current_user
from app.crud.group import group_crud
from app.crud.post import post_crud
from app.models.users import User
from app.schemas.post import PostBase, PostCreate, PostDB, PostUpdate

router = APIRouter()


@router.post('/', response_model=PostCreate)
async def create_post(
        post: PostCreate,
        image: UploadFile = File(...),
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> PostCreate:
    await check_obj_exists_by_id(
        obj_id=post.group_id,
        obj_crud=group_crud,
        session=session
    )
    image_path = await validate_image(image=image)
    post = await post_crud.create(
        obj_in=post,
        user=user,
        image=image_path,
        session=session
    )
    return post


@router.get('/', response_model=list[PostDB], response_model_exclude_none=True)
async def get_posts(
        session: AsyncSession = Depends(get_async_session)
) -> list[PostDB]:
    """Получение списка постов."""
    posts = await post_crud.get_list_with_author(session=session)
    return posts


@router.get(
    '/{post_id}',
    response_model=PostDB,
    response_model_exclude_none=True
)
async def get_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> PostDB:
    """Получение конкретного поста."""
    await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        session=session
    )
    post = await post_crud.get_with_author(obj_id=post_id, session=session)
    return post


@router.patch('/{post_id}', response_model=PostUpdate)
async def patch_post(
        post_id: int,
        obj_in: PostUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> PostUpdate:
    """Обновление данных поста."""
    post = await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        session=session,
        user=user
    )
    if obj_in.group_id is not None:
        await check_obj_exists_by_id(
            obj_id=obj_in.group_id,
            obj_crud=group_crud,
            session=session
        )
    post = await post_crud.update(obj_in=obj_in, db_obj=post, session=session)
    return post


@router.delete('/{post.id}', response_model=PostBase)
async def delete_post(
        post_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> PostBase:
    """Удаление поста."""
    post = await check_obj_exists_by_id(
        obj_id=post_id,
        obj_crud=post_crud,
        user=user,
        session=session,
    )
    post = await post_crud.delete(db_obj=post, session=session)
    return post
