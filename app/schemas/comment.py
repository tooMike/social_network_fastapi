from pydantic import BaseModel, Field

from datetime import datetime


class CommentBase(BaseModel):
    """Базовая модель для комментария."""

    text: str = Field(..., min_length=5)



class CommentDB(CommentBase):
    """Модель для отображения комментария."""

    post_id: int
    created_at: datetime
