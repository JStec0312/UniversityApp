"""
Base model module for SQLAlchemy model inheritance.

This module provides the BaseModel class which serves as the foundation
for all database models in the application, providing common fields and behaviors.
"""

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class BaseModel(Base):
    """
    Base abstract model for all database entities.
    
    This class defines common fields and behaviors that should be present
    in all database models, including:
    
    - Primary key ID field
    - Creation timestamp
    - Automatic table name generation
    
    All model classes should inherit from this class to ensure consistency
    across the database schema.
    
    Attributes:
        id: Primary key auto-increment integer column
        created_at: Timestamp of record creation with timezone support
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Automatically generate table name based on class name.
        
        This method automatically converts the class name to lowercase
        to create the table name, following the convention of lowercase
        table names in SQL.
        
        Returns:
            str: The lowercase class name as the table name
        """
        return cls.__name__.lower()
