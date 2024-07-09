from typing import List
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.group import Group as GroupModel
from app.schemas.group import Group as GroupSchema


async def create_group(
        new_group: GroupSchema
):
    """Создание новой группы."""
    new_group = new_group.dict()
    db_group = GroupModel(**new_group)
    async with AsyncSessionLocal() as session:
        session.add(db_group)
        await session.commit()
        await session.refresh(db_group)
    return db_group


async def read_all_groups():
    async with AsyncSessionLocal() as session:
        groups = await session.execute(select(GroupModel.title))
    return groups.scalars().all()
