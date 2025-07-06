"""
Base schema module for Pydantic models.

This module provides base Pydantic models for schema inheritance
throughout the application.
"""

from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime
from typing import Optional


class BaseSchema(PydanticBaseModel):
    """
    Base schema for consistent schema structure.
    
    This class serves as the foundation for all Pydantic schemas
    in the application. It configures the ORM mode to allow working
    with SQLAlchemy models and defines common fields.
    
    Attributes:
        id: Optional primary key ID field
        created_at: Optional timestamp of record creation
    """
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        """
        Pydantic configuration class.
        
        This configuration enables ORM mode, which allows Pydantic to work
        with SQLAlchemy ORM models directly.
        """
        orm_mode = True
