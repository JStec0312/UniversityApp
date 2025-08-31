
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Group(BaseModel):
    __tablename__ = "groups"
    
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)  # University this group belongs to
    group_name = Column(String(100), nullable=False)  # Name of the group
    
    # Relationships
    university = relationship("University", back_populates="groups")  # Link to the university
    # Use string reference to avoid circular import
    admins = relationship("Admin", back_populates="group", passive_deletes=True)  # Administrators of this group
    events = relationship("Event", back_populates="group", passive_deletes=True)  # Events associated with this group
    news = relationship("News", back_populates="group", passive_deletes=True)  # News posts associated with this group
    superior_admins = relationship("SuperiorAdmin", back_populates="group", passive_deletes=True)  # Superior administrators of this group
    members = relationship("GroupMember", back_populates="group", passive_deletes=True)  # Members of this group
