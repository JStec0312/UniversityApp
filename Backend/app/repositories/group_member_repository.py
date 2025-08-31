from app.repositories.base_repository import BaseRepository
from app.models.group_member import GroupMember

class GroupMemberRepository(BaseRepository[GroupMember]):
    def __init__(self, db):
        super().__init__(db, GroupMember)
