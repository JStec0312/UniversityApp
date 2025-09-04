from sqlalchemy.orm import Session, selectinload

from app.models.user import User
from app.models.admin import Admin
from app.models.group_member import GroupMember
from app.repositories.base_repository import BaseRepository

class GroupMemberRepository(BaseRepository[GroupMember]):
    def __init__(self, session: Session):
        super().__init__(session, GroupMember)

    def get_group_members_with_display_name(
        self,
        group_id: int,
        university_id: int,
        limit: int,
        offset: int,
    ) -> list[GroupMember]:
        return (
            self.session.query(self.model)
            .join(self.model.user)                              # INNER JOIN na relacji
            .options(selectinload(self.model.user))             # prefetch użytkownika
            .filter(
                self.model.group_id == group_id,
                User.university_id == university_id,
            )
            .order_by(self.model.created_at)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_group_admins_with_display_name(
        self,
        group_id: int,
        university_id: int,
        limit: int,
        offset: int,
    ) -> list[GroupMember]:
        return (
            self.session.query(self.model)
            .join(self.model.user)                              # INNER JOIN na relacji
            .options(selectinload(self.model.user))             # prefetch użytkownika
            .filter(
                self.model.group_id == group_id,
                User.university_id == university_id,
                self.model.user.has(Admin.group_id == group_id)  
            )
            .order_by(self.model.created_at)
            .offset(offset)
            .limit(limit)
            .all()
        )