from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Comment(Base):
    """Модель комментария."""

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        insert_default=func.now()
    )

    def __repr__(self):
        return self.text[:25]
