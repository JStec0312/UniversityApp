from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import BaseModel
from app.utils.enums.invitation_status_enum import InvitationStatus
from sqlalchemy import Enum


class GroupInvitation(BaseModel):
    __tablename__ = "group_invitations"

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    inviter_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING)