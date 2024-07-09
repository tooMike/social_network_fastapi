from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.models import User
from app.schemas.group import GroupDB, GroupUpdate


class CRUDbase:
    """Базовый класс для CRUD функций."""

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """Получение списка объектов."""
        obj = await session.execute(
            select(self.model).where(self.model.id == obj_id))
        return obj.scalars().first()

    async def get_list(
            self,
            session: AsyncSession
    ):
        """Получение списка объектов."""
        objts = await session.execute(select(self.model))
        return objts.scalars().all()

    async def get_obj_by_title(
            self,
            title: str,
            session: AsyncSession
    ):
        """Получение объекта по названию."""
        obj = await session.execute(
            select(self.model).where(self.model.title == title))
        return obj.scalars().first()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        """Создание записи в БД."""
        obj_in = obj_in.dict()
        obj_db = self.model(**obj_in)
        session.add(obj_db)
        await session.commit()
        await session.refresh(obj_db)
        return obj_db

    async def update(
            self,
            db_obj: GroupDB,
            obj_in: GroupUpdate,
            session: AsyncSession
    ):
        """Изменение объекта."""
        obj_data = jsonable_encoder(db_obj)
        obj_new_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in obj_new_data:
                setattr(db_obj, field, obj_new_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
