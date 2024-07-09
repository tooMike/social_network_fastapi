import re

from pydantic import BaseModel, Field, field_validator, ValidationInfo


class GroupBase(BaseModel):
    """Базовая модель групп."""
    title: str | None = Field(None, max_length=200, min_length=3)
    slug: str | None = Field(None, max_length=50, min_length=3)
    description: str | None = Field(None, max_length=350, min_length=3)

    @field_validator("slug")
    @classmethod
    def slug_validator(cls, slug: str) -> str:
        pattern = re.compile("^[a-zA-Z0-9-_]+$")
        if not pattern.match(slug):
            raise ValueError(
                "Недопустимые символы в slug. Разрешены только \
                буквы, цифры, дефисы и подчеркивания.")

        return slug


class GroupCreate(GroupBase):
    """Схема для создания групп."""
    title: str = Field(max_length=200, min_length=3)
    slug: str = Field(max_length=50, min_length=3)
    description: str = Field(max_length=350, min_length=3)


class GroupUpdate(GroupBase):
    """Схема для изменения групп."""

    @field_validator("title", "slug", "description")
    def validate(cls, field: str, info: ValidationInfo) -> str:
        """Проверяем, что полю не передано значение null."""
        if field is None:
            raise ValueError(f"Поле {info.field_name} не может быть пустым!")
        return field


class GroupDB(GroupCreate):
    """Схема для получения групп."""
    id: int
