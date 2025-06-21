
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Student(BaseModel):
    __tablename__ = "students"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="student")
    faculty = relationship("Faculty", back_populates="students")
    major = relationship("Major", back_populates="students")