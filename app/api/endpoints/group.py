from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import validate_same_names, \
    check_obj_exists_by_id
from app.core.db import get_async_session
from app.crud.group import group_crud
from app.schemas.group import GroupCreate, GroupDB, GroupUpdate

router = APIRouter()


@router.post("/", response_model=GroupDB)
async def create_new_group(
        new_group: GroupCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание новой группы."""
    await validate_same_names(obj_title=new_group.title, crud=group_crud,
                              session=session)
    new_group = await group_crud.create(new_group, session)
    return new_group


@router.get("/", response_model=list[GroupDB])
async def gel_all_groups(
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка всех групп."""

    groups_list = await group_crud.get_list(session)
    return groups_list


@router.get("/{group_id}", response_model=GroupDB)
async def get_group(
        group_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Получение информации о конкретной группе."""
    group = await group_crud.get(group_id, session)
    return group


@router.patch("/{group_id}", response_model=GroupDB)
async def patch_group(
        group_id: int,
        new_data: GroupUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление информации о группе."""
    group_db = await check_obj_exists_by_id(group_id, group_crud, session)
    if new_data.title is not None:
        await validate_same_names(new_data.title, group_crud, session)
    group = await group_crud.update(group_db, new_data, session)
    return group
