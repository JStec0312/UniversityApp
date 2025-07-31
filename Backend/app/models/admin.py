from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # One-to-one with User
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)  # Group this admin belongs to
    
    user = relationship("User", back_populates="admin")  # Link to the user entity
    # Use string reference to avoid circular import
    group = relationship("Group", foreign_keys=[group_id], back_populates="admins")  # Link to the group
    
    discounts = relationship("Discount", back_populates="admin")  # Discounts created by this admin
