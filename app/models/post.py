from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.group import Group
    from app.models.users import User
    from app.models.comment import Comment


class Post(Base):
    """Модель поста."""

    text: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    image_path: Mapped[Optional[str]] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('group.id'))

    user: Mapped['User'] = relationship(back_populates='posts')
    group: Mapped['Group'] = relationship(back_populates='posts')
    comments: Mapped['Comment'] = relationship(back_populates='post')

    def __repr__(self):
        return self.text[:25]
