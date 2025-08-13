from app.repositories.base_repository import BaseRepository
from app.models.group import Group
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

class GroupRepository(BaseRepository[Group]):
    def __init__(self, db):
        super().__init__(db, Group)

    def get_by_name(self, name: str, university_id: int) -> Group | None:
        return self.db.query(self.model).filter(
            self.model.group_name == name,
            self.model.university_id == university_id
        ).first()

    def get_by_university_id(self, university_id: int) -> list[Group]:
        return self.db.query(self.model).filter(
            self.model.university_id == university_id
        ).all()

def delete_by_id_and_university(self, group_id: int, university_id: int) -> int:
    try:
        stmt = delete(self.model).where(
            self.model.id == group_id,
            self.model.university_id == university_id,
        )
        result = self.db.execute(stmt)
        self.db.commit()
        # ile rekordow faktycznie usunieto (0 lub 1)
        return result.rowcount or 0
    except IntegrityError:
        self.db.rollback()
        raise
    except Exception:
        self.db.rollback()
        raise