from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func

from app.core.db import Base
# from app.models.group import Group
# from app.models.users import User


class Post(Base):
    """Модель поста."""

    text: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    image_path: Mapped[Optional[str]] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('group.id'))

    user: Mapped['User'] = relationship('User', back_populates='posts')
    group: Mapped['Group'] = relationship('Group', back_populates='posts')

    def __repr__(self):
        return self.text[:25]
