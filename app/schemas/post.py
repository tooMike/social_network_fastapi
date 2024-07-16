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
            parts = value.split(',', 1)
            if len(parts) != 2:
                raise ValueError(
                    'Невалидный формат изображения'
                )

            header, encoded = parts
            if not header.startswith('data:image'):
                raise ValueError(
                    'Невалидный формат изображения. Начало должно быть – '
                    'data:image'
                )

            # Проверка допустимого типа MIME
            allowed_types = ['jpeg', 'png', 'gif']
            if not any(f'image/{mime}' in header for mime in allowed_types):
                raise ValueError(
                    f'Невалидный формат изображения: разрешенные форматы: '
                    f'{allowed_types}'
                )

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
