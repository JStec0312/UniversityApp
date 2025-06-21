from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Admin(BaseModel):
    """Admin model"""
    __tablename__ = "admins"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    group_type = Column(String(255))  # e.g., "Samorząd", "Koło Naukowe", etc.
    
    # Relationships
    user = relationship("User", back_populates="admin")
    news = relationship("News", back_populates="admin")
    events = relationship("Event", back_populates="admin")
    discounts = relationship("Discount", back_populates="admin")