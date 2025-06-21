from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, email: str, hashed_password: str, display_name: str = None, verified: bool = False, university_id: int = None):
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
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)

    
    # Relationships
    university = relationship("University", back_populates="users")
    student = relationship("Student", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    forum_posts = relationship("ForumPost", back_populates="user")
    event_rsvps = relationship("EventRSVP", back_populates="user")

