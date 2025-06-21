# models/major.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Major(BaseModel):
    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="majors")
    students = relationship("Student", back_populates="major")
