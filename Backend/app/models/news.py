from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class News(BaseModel):
    """News model"""
    __tablename__ = "news"
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    
    # Relationships
    admin = relationship("Admin", back_populates="news")