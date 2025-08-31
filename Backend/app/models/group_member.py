from app.models.base import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class GroupMember(BaseModel):
    __tablename__ = 'group_members'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)

    # Relationship
    user = relationship("User", back_populates="group_members", lazy="joined")
    group = relationship("Group", back_populates="members")

    @property
    def display_name(self):
        return self.user.display_name if self.user else None
