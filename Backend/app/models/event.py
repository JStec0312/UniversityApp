from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Event(BaseModel):
    """Event model"""
    __tablename__ = "events"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=False)
    image_url = Column(String(512))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)  
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Relationships
    group = relationship("Group", back_populates="events")
    rsvps = relationship("EventRSVP", back_populates="event")
    university = relationship("University", back_populates="events")
    @property
    def group_name(self):
        return self.group.group_name if self.group else None