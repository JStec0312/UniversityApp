from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime

class GroupRegisterPassword(BaseModel): 
    __tablename__ = "group_register_passwords"

    id = Column(Integer, primary_key=True)
    token = Column(String(255), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    given_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    given_by_user = relationship("User", back_populates="group_register_passwords")
    group = relationship("Group", back_populates="group_register_passwords")