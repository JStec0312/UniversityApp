
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Student(BaseModel):
    """
    Student model representing university students.
    
    This model extends the User entity with student-specific attributes like
    faculty and major. Each student is associated with exactly one user.
    """
    def __init__(self, user_id: int, faculty_id: int = None, major_id: int = None):
        """
        Initialize a new Student instance.
        
        Args:
            user_id (int): ID of the user this student profile belongs to
            faculty_id (int, optional): ID of the faculty this student belongs to
            major_id (int, optional): ID of the major this student is enrolled in
        """
        self.user_id = user_id
        self.faculty_id = faculty_id
        self.major_id = major_id
    
    __tablename__ = "students"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # One-to-one with User
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True)  # Faculty the student belongs to
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)  # Major the student is enrolled in
    
    # Relationships
    user = relationship("User", back_populates="student")  # Link to the user entity
    faculty = relationship("Faculty", back_populates="students")  # Link to the faculty
    major = relationship("Major", back_populates="students")  # Link to the major