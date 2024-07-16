from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    """Базовая модель поста."""

    text: str | None = Field(None, min_length=3)
    group_id: int | None = None


class PostCreate(PostBase):
    """Модель для создания поста."""

    text: str = Field(..., min_length=3)
    group_id: int


class PostUpdate(PostBase):
    """Модель для изменения поста."""

    text: str = Field(..., min_length=3)


class PostDelete(BaseModel):
    """Модель для удаления публикации."""

    id: int


class PostDBBase(PostCreate):
    """Модель для получения поста."""

    id: int
    pub_date: datetime
    image: str

    model_config = ConfigDict(from_attributes=True)


class PostDB(PostDBBase):
    """Модель для получения поста c автором."""

    author: str
