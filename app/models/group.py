from typing import List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.post import Post


class Group(Base):
    """Модель групп."""
    title: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False
    )
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    posts: Mapped[List['Post']] = relationship('Post', back_populates='group')

    def __repr__(self):
        return self.title
