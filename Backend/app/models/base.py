from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class BaseModel(Base):
    """Base model for all database models"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
