import re

from pydantic import BaseModel, Field, field_validator


class Group(BaseModel):
    """Модель групп"""
    title: str = Field(max_length=200, min_length=3)
    slug: str = Field(max_length=50, min_length=3)
    description: str = Field(max_length=350, min_length=3)

    @field_validator("slug")
    @classmethod
    def slug_validator(cls, slug: str) -> str:
        pattern = re.compile("^[a-zA-Z0-9-_]+$")
        if not pattern.match(slug):
            raise ValueError(
                "Недопустимые символы в slug. Разрешены только \
                буквы, цифры, дефисы и подчеркивания.")

        return slug
