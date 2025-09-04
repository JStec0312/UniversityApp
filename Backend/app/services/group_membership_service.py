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
from app.core.service_errors import (
    InvitationPermissionError,
    UserAlreadyInGroupError,
    UserNotFoundError,
    GroupNotFoundError,
    UserAlreadyInvitedError,
    InvitationAccessError,
    InvitationNotFoundError,
    InvitationNotActiveError,
    AdminPermissionError,
    UserNotMemberError,
    UserIsAlreadyAdminError,
    PermissionError
)
from app.utils.enums.invitation_status_enum import InvitationStatus
from app.utils.uow import uow



class GroupMembershipService:
    def __init__(
        self,
        group_member_repository: GroupMemberRepository | None = None,
        group_invitation_repository: GroupInvitationRepository | None = None,
        user_repository: UserRepository | None = None,
        admin_repository: AdminRepository | None = None,
        group_repository: GroupRepository | None = None,
    ):
        self.group_member_repository = group_member_repository
        self.group_invitation_repository = group_invitation_repository
        self.user_repository = user_repository
        self.admin_repository = admin_repository
        self.group_repository = group_repository
        # jedna, współdzielona sesja (UoW) – bierzemy z któregoś repo
        repos = [r for r in [group_member_repository, group_invitation_repository, user_repository, admin_repository, group_repository] if r]
        self.session = repos[0].session if repos else None

    # ----------------- INVITATIONS -----------------

    def invite_user_to_group(self, invited_user_id: int, inviter_user_id: int, group_id: int) -> GroupInvitation:
        if not self.group_repository.exists_with_conditions((Group.id == group_id,)):
            raise GroupNotFoundError()

        # czy zapraszający ma prawo (admin tej grupy)?
        if not self.admin_repository.exists_with_conditions((Admin.user_id == inviter_user_id, Admin.group_id == group_id)):
            raise InvitationPermissionError()

        # czy zapraszany użytkownik istnieje?
        if not self.user_repository.get_by_id(invited_user_id):
            raise UserNotFoundError()

        # czy już jest członkiem?
        if self.group_member_repository.exists_with_conditions((GroupMember.user_id == invited_user_id, GroupMember.group_id == group_id)):
            raise UserAlreadyInGroupError()

        # czy już ma aktywne zaproszenie?
        if self.group_invitation_repository.exists_with_conditions(
            (
                GroupInvitation.invited_user_id == invited_user_id,
                GroupInvitation.group_id == group_id,
                GroupInvitation.status == InvitationStatus.PENDING,
            )
        ):
            raise UserAlreadyInvitedError()

        inv = GroupInvitation(group_id=group_id, invited_user_id=invited_user_id, inviter_user_id=inviter_user_id)

        try:
            with uow(self.session):
                self.group_invitation_repository.create(inv)
            return inv
        except IntegrityError as e:
            code = getattr(getattr(e, "orig", None), "pgcode", None)
            if code == "23505":
                raise UserAlreadyInvitedError()
            if code == "23503":
                raise UserNotFoundError()
            raise

    def accept_group_invitation(self, invitation_id: int, user_id: int) -> GroupMember:
        with uow(self.session):
            inv = self.group_invitation_repository.get_by_id(invitation_id, for_update=True)
            if not inv:
                raise InvitationNotFoundError()
            if inv.status != InvitationStatus.PENDING:
                raise InvitationNotActiveError()
            if inv.invited_user_id != user_id:
                raise InvitationAccessError()

            if self.group_member_repository.exists_with_conditions((GroupMember.user_id == user_id, GroupMember.group_id == inv.group_id)):
                raise UserAlreadyInGroupError()

            try:
                member = self.group_member_repository.create(GroupMember(user_id=user_id, group_id=inv.group_id))
                self.group_invitation_repository.update_by_id(inv.id, {"status": InvitationStatus.ACCEPTED})
                return member
            except IntegrityError as e:
                code = getattr(getattr(e, "orig", None), "pgcode", None)
                if code == "23505":
                    raise UserAlreadyInGroupError()
                if code == "23503":
                    raise UserNotFoundError()
                raise

    # ----------------- MEMBERS -----------------

    def get_group_members(self, group_id: int, university_id: int, limit: int, offset: int) -> list[GroupMember]:
        return self.group_member_repository.get_group_members_with_display_name(
            group_id=group_id, university_id=university_id, limit=limit, offset=offset
        )

    # ----------------- ADMINS -----------------

    def add_group_admin(
        self,
        group_id: int,
        invited_user_id: int,
        inviter_user_id: int,
        inviter_is_superior: bool = False,  # zgodnie z refaktorem routera
    ) -> Admin:
        with uow(self.session):
            # uprawnienia: superior może zawsze; wpp admin tej grupy
            inviter_is_admin = self.admin_repository.exists_with_conditions(
                (Admin.user_id == inviter_user_id, Admin.group_id == group_id)
            )
            if not (inviter_is_superior or inviter_is_admin):
                raise AdminPermissionError()

            # zapraszany musi być członkiem tej grupy
            if not self.group_member_repository.exists_with_conditions(
                (GroupMember.user_id == invited_user_id, GroupMember.group_id == group_id)
            ):
                raise UserNotMemberError()

            # czy już admin?
            if self.admin_repository.exists_with_conditions(
                (Admin.user_id == invited_user_id, Admin.group_id == group_id)
            ):
                raise UserIsAlreadyAdminError()

            try:
                admin = self.admin_repository.create(Admin(user_id=invited_user_id, group_id=group_id))
                return admin
            except IntegrityError:
                raise UserIsAlreadyAdminError()

    def get_group_admins(self, group_id: int, university_id: int) -> list[Admin]:
        return self.group_member_repository.get_group_admins_with_display_name(
            group_id=group_id,
            university_id=university_id,
            limit=100,
            offset=0,
        )
    

    def  get_group_invitations(self, group_id: int, user_id: int) -> list[GroupInvitation]:
        # czy user jest adminem tej grupy?
        if not self.admin_repository.exists_with_conditions((Admin.user_id == user_id, Admin.group_id == group_id)):
            raise PermissionError("User does not have permission to see invitations for this group.")
        
        return self.group_invitation_repository.get_paginated_with_conditions((GroupInvitation.group_id == group_id,), limit=None, offset=None)
    
    def cancel_invitation(self, invitation_id: int, user_id: int) -> None:
        # czy user jest adminem tej grupy?
        inv = self.group_invitation_repository.get_by_id(invitation_id)
        if not inv:
            raise InvitationNotFoundError()
        
        if not self.admin_repository.exists_with_conditions((Admin.user_id == user_id, Admin.group_id == inv.group_id)):
            raise AdminPermissionError("User does not have permission to cancel this invitation.")
        
        with uow(self.session):
            self.group_invitation_repository.delete_by_id(invitation_id)
            return None
    
