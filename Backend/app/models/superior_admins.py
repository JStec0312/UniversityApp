from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SuperiorAdmin(BaseModel):
    __tablename__ = "superior_admins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),  nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="superior_admin")
    group = relationship("Group", back_populates="superior_admins")