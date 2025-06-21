
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Faculty(BaseModel):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Relationships
    university = relationship("University", back_populates="faculties")
    students = relationship("Student", back_populates="faculty")
    majors = relationship("Major", back_populates="faculty")   
