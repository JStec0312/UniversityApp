from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Discount(BaseModel):
    """Discount model"""
    __tablename__ = "discounts"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    link = Column(String(512))
    valid_until = Column(Date, nullable=False)
    
    # Relationships
