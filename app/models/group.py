from sqlalchemy import Column, String, Text

from app.core.db import Base


class Group(Base):
    """Модель групп."""
    title = Column(String(200), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

