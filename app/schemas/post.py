from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PostBase(BaseModel):
    """Базовая модель поста."""

    text: str = Field(..., min_length=3)


class PostUpdate(PostBase):
    """Модель для изменения поста."""

    text: str = Field(..., min_length=3)
    group_id: int | None = None
    image: str | None = None

    @field_validator('image')
    @classmethod
    def validate_image(cls, value: str) -> str:
        if value:
            header, _ = value.split(',', 1)
            if not header.startswith('data:image'):
                raise ValueError('Invalid image format')
        return value


class PostCreate(PostUpdate):
    """Модель для создания поста."""

    group_id: int
    image: str


class PostDelete(BaseModel):
    """Модель для удаления публикации."""

    id: int


class PostDBBase(PostBase):
    """Модель для получения поста."""

    id: int
    group_id: int
    pub_date: datetime
    image: str

    model_config = ConfigDict(from_attributes=True)


class PostDB(PostDBBase):
    """Модель для получения поста c автором."""

    author: str
