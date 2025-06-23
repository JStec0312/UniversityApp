
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Group(BaseModel):
    __tablename__ = "groups"
    
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    group_name = Column(String(100), nullable=False)

    university = relationship("University", back_populates="groups")
    # Use string reference to avoid circular import
    admins = relationship("Admin", back_populates="group")
    superior_groups = relationship("SuperiorGroup", back_populates="group")
    
