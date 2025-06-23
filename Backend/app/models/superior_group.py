from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class SuperiorGroup(BaseModel):
    """Admin model"""
    __tablename__ = "superior_groups"
    
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    
    # Relationships
    university = relationship("University", back_populates="superior_groups")
    group = relationship("Group", back_populates="superior_groups")