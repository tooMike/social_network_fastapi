from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import validate_same_names
from app.core.db import get_async_session
from app.crud.group import group_crud
from app.schemas.group import GroupCreate, GroupDB

router = APIRouter()


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

@router.post("/", response_model=GroupDB)
async def create_group(
        obj: GroupCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await validate_same_names(
        obj_title=obj.title,
        crud=group_crud,
        session=session
    )
    group = await group_crud.create(
        obj_in=obj,
        session=session
    )
    return group
