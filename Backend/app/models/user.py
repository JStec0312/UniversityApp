from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.models.base import BaseModel

class User(BaseModel):
    """
    User model representing application users.
    
    This is the core user entity for all system users. Users can be students,
    administrators, or regular users. Each user has authentication information
    and can be associated with a university.
    """
    def __init__(self, email: str, hashed_password: str, display_name: str = None, verified: bool = False, university_id: int = None):
        """
        Initialize a new User instance.
        
        Args:
            email (str): User's email address, used for login and communication
            hashed_password (str): Hashed password for authentication
            display_name (str, optional): User's display name
            verified (bool, optional): Whether the user's account is verified
            university_id (int, optional): ID of the university this user belongs to
        """
        self.email = email
        self.hashed_password = hashed_password
        self.display_name = display_name
        self.verified = verified
        self.university_id = university_id

    __tablename__ = "users"
    
    email = Column(String(255), unique=False, index=True, nullable=False) # Unique constraint is marked as UNIQUE for tests
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    avatar_image_url = Column(String(255), nullable=True, default=None)  # URL to the user's avatar image
    

    
    # Relationships
    university = relationship("University", back_populates="users")  # University this user belongs to
    student = relationship("Student", back_populates="user", uselist=False)  # Student profile if user is a student
    admin = relationship("Admin", back_populates="user", uselist=False)  # Admin profile if user is an admin
    forum_posts = relationship("ForumPost", back_populates="user")  # Forum posts created by this user
    event_rsvps = relationship("EventRSVP", back_populates="user")  # Event RSVPs for this user
    superior_admin = relationship("SuperiorAdmin", back_populates="user")  


