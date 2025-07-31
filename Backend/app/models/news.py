from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class News(BaseModel):
    """News model"""
    __tablename__ = "news"
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    image_url = Column(String(512), nullable=True) 
    # Relationships
    group = relationship("Group", back_populates="news")
    university = relationship("University", back_populates="news")
    