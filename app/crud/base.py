from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.models import Post, User
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
            session: AsyncSession,
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

    async def get_obj_by_slug(
            self,
            slug: str,
            session: AsyncSession
    ):
        """Получение объекта по slug."""
        obj = await session.execute(
            select(self.model).where(self.model.slug == slug))
        return obj.scalars().first()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: User | None = None,
            post: Post | None = None,
    ):
        """Создание записи в БД."""
        obj_in = obj_in.dict()
        if user:
            obj_in["user_id"] = user.id
        if post:
            obj_in["post_id"] = post.id
        obj_db = self.model(**obj_in)
        session.add(obj_db)
        await session.commit()
        await session.refresh(obj_db)
        return obj_db

    async def update(
            self,
            db_obj,
            obj_in,
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

    async def delete(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Удаление объекта из БД."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

