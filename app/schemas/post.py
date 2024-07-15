from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime


class PostBase(BaseModel):
    """Базовая модель поста."""

    text: str | None = Field(None, min_length=3)
    group_id: int | None = None
    image: str | None = None


class PostCreate(PostBase):
    """Модель для создания поста."""

    text: str = Field(..., min_length=3)
    group_id: int


class PostUpdate(PostBase):
    """Модель для изменения поста."""

    text: str = Field(..., min_length=3)


class PostDB(PostCreate):
    """Модель для получения поста."""

    id: int
    author: str
    pub_date: datetime

    model_config = ConfigDict(from_attributes=True)
