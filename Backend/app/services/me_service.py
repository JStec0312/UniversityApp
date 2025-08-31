from app.models.group_invitation import GroupInvitation

from app.repositories.user_repository import UserRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.event_repository import EventRepository
from app.repositories.admin_repository import AdminRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.group_member_repository import GroupMemberRepository
from app.repositories.group_invitation_repository import GroupInvitationRepository
class MeService:
    def __init__(
            self,
            user_repository: UserRepository = None,
            group_repository: GroupRepository = None,
            event_repository: EventRepository = None,
            admin_repository : AdminRepository = None,
            student_repository: StudentRepository = None,
            group_member_repository: GroupMemberRepository = None,
            group_invitation_repository: GroupInvitationRepository = None
    ):
        self.user_repository = user_repository
        self.group_repository = group_repository
        self.event_repository = event_repository
        self.admin_repository = admin_repository
        self.student_repository = student_repository
        self.group_member_repository = group_member_repository
        self.group_invitation_repository = group_invitation_repository

    def see_my_invitations(self, user_id: int, limit: int, offset: int):
        conditions = (GroupInvitation.invited_user_id == user_id)
        return self.group_invitation_repository.get_paginated_with_conditions(conditions=conditions, limit=limit, offset=offset)
    