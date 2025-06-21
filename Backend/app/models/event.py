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
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    
    # Relationships
    admin = relationship("Admin", back_populates="events")
    rsvps = relationship("EventRSVP", back_populates="event")