from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.models.post import Post


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    posts: Mapped[List['Post']] = relationship('Post', back_populates='user')
