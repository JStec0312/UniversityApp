from app.repositories.base_repository import BaseRepository
from app.models.group_invitation import GroupInvitation

class GroupInvitationRepository(BaseRepository[GroupInvitation]):
    def __init__(self, db):
        super().__init__(db, GroupInvitation)

