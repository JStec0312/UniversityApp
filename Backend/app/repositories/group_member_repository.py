from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.models.group_member import GroupMember
from sqlalchemy.orm import selectinload


class GroupMemberRepository(BaseRepository[GroupMember]):
    def __init__(self, db):
        super().__init__(db, GroupMember)

    def get_group_members_with_display_name(self, group_id:int, university_id:int, limit:int, offset:int):
        return (
            self.db.query(GroupMember)
            .join(GroupMember.user)  # INNER JOIN – wymusi istnienie usera
            .options(selectinload(GroupMember.user))  # gdyby lazy nie było joined
            .filter(
                GroupMember.group_id == group_id,
                User.university_id == university_id
            )
            .order_by(GroupMember.created_at)
            .limit(limit).offset(offset)
            .all()
        )