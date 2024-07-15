from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr


class UserBase(schemas.CreateUpdateDictModel):
    """Базовая схема пользователя."""

    username: str
    email: EmailStr


class UserRead(UserBase):
    """Получение информации о пользователе."""

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Создание пользователя."""

    password: str


class UserUpdate(schemas.BaseUserUpdate):
    """Изменение информации о пользователе."""
