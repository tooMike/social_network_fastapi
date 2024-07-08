from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column
from sqlalchemy import Column, Integer

from app.core.config import settings


class PreBase:
    """Создаем базовых класс для всех моделей."""

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine: AsyncEngine = create_async_engine(settings.database_url)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session