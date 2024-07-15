from typing import List, TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.models.post import Post

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.comment import Comment


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    posts: Mapped[List['Post']] = relationship(back_populates='user')
    comments: Mapped[List['Comment']] = relationship(back_populates='user')
