from datetime import datetime

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    """Базовая модель для комментария."""

    text: str = Field(..., min_length=5)


class CommentCreate(CommentBase):
    """Модель для создания комментария."""


class CommentDB(CommentBase):
    """Модель для отображения комментария."""

    id: int
    author: str
    created: datetime
    post: int
