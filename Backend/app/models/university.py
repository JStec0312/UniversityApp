# models/university.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class University(BaseModel):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    
    faculties = relationship("Faculty", back_populates="university")
    users = relationship("User", back_populates="university")
    groups = relationship("Group", back_populates="university")
    superior_groups = relationship("SuperiorGroup", back_populates="university")  # ✅ dodaj to
    events = relationship("Event", back_populates="university")
