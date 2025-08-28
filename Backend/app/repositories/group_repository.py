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
        stmt = (
            delete(self.model)
            .where(self.model.id == group_id, self.model.university_id == university_id)
            .returning(self.model.id)
        )
        try:
            result = self.db.execute(stmt)
            self.db.commit()  # jeśli taki masz kontrakt; inaczej przenieś commit wyżej
            deleted_id = result.scalar_one_or_none()
            return 1 if deleted_id is not None else 0
        except IntegrityError:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise