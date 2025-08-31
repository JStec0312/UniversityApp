from sqlalchemy.exc import IntegrityError

from app.models.group_member import GroupMember
from app.models.user import User
from app.models.group_invitation import GroupInvitation
from app.models.admin import Admin
from app.models.group import Group
from app.repositories.group_member_repository import GroupMemberRepository
from app.repositories.group_invitation_repository import GroupInvitationRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.user_repository import UserRepository
from app.repositories.admin_repository import AdminRepository
from app.core.service_errors import NoPermissionForInvitationException, UserAlreadyInGroupException, UserNotFoundException, GroupNotFoundException, UserAlreadyInvitedError, NotPermittedForThisInvitationException, InvitationNotFoundException, InvitationNotActiveException
from app.utils.enums.invitation_status_enum import InvitationStatus

class GroupMembershipService:
    def __init__(self, group_member_repository: GroupMemberRepository = None, group_invitation_repository: GroupInvitationRepository = None, user_repository: UserRepository = None, admin_repository: AdminRepository = None, group_repository: GroupRepository = None):
        self.group_member_repository = group_member_repository
        self.group_invitation_repository = group_invitation_repository
        self.user_repository = user_repository
        self.admin_repository = admin_repository
        self.group_repository = group_repository


    def invite_user_to_group(self, invited_user_id:int, inviter_user_id: int, group_id:int) -> GroupInvitation:
        #check if group exists
        if not self.group_repository.get_first_with_conditions(conditions = (Group.id == group_id,)):
            raise GroupNotFoundException()

        #check if admin has a permission to invite
        if not self.admin_repository.get_first_with_conditions(conditions = (Admin.user_id == inviter_user_id, Admin.group_id == group_id)):
            raise NoPermissionForInvitationException()

        #check if the user exists
        if not self.user_repository.get_by_id(invited_user_id):
            raise UserNotFoundException()
        #check if user is already a member
        if self.user_repository.get_first_with_conditions(conditions = (GroupMember.user_id == invited_user_id, GroupMember.group_id == group_id)):
            raise UserAlreadyInGroupException()
        #check if the user is already invited
        if self.group_invitation_repository.get_first_with_conditions(conditions = (GroupInvitation.invited_user_id == invited_user_id, GroupInvitation.group_id == group_id, GroupInvitation.status==InvitationStatus.PENDING)):
            raise UserAlreadyInvitedError()

        inv = GroupInvitation(group_id=group_id, invited_user_id=invited_user_id, inviter_user_id=inviter_user_id)

        try:
            self.group_invitation_repository.create(inv)
        
        except IntegrityError as e:
            code = getattr(getattr(e, 'orig', None), 'pgcode', None)
            if code == '23505':
                raise UserAlreadyInvitedError()
            if code == '23503':
                raise UserNotFoundException()
            raise
        return inv
    
    def accept_group_invitation(self, invitation_id:int, user_id:int) -> GroupMember:
        inv = self.group_invitation_repository.get_by_id(invitation_id)
        if not inv:
            raise InvitationNotFoundException()
        if inv.status != InvitationStatus.PENDING:
            raise InvitationNotActiveException()
        if inv.invited_user_id != user_id:
            raise NotPermittedForThisInvitationException()

        if self.group_member_repository.get_first_with_conditions(conditions = (GroupMember.user_id == user_id, GroupMember.group_id == inv.group_id)):
            raise UserAlreadyInGroupException()

        try:
            group_member =  self.group_member_repository.create(GroupMember(user_id=user_id, group_id=inv.group_id))
            self.group_invitation_repository.update_by_id(inv.id, {"status": InvitationStatus.ACCEPTED})
            return group_member
        except IntegrityError as e:
            code = getattr(getattr(e, 'orig', None), 'pgcode', None)
            if code == '23505':
                raise UserAlreadyInGroupException()
            if code == '23503':
                raise UserNotFoundException()
            raise


    def get_group_members(self, group_id:int, university_id:int, limit:int, offset:int) -> list[GroupMember]:
        return self.group_member_repository.get_group_members_with_display_name(group_id=group_id, university_id=university_id, limit=limit, offset=offset)
