from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Admin(BaseModel):
    def __init__(self, user_id:int, group_id:int):
        self.user_id = user_id
        self.group_id = group_id

    __tablename__ = "admins"
    
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    
    user = relationship("User", back_populates="admin")
    # Use string reference to avoid circular import
    group = relationship("Group", foreign_keys=[group_id], back_populates="admins")
    
    news = relationship("News", back_populates="admin")
    events = relationship("Event", back_populates="admin")
    discounts = relationship("Discount", back_populates="admin")
