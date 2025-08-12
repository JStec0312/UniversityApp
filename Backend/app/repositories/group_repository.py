from app.repositories.base_repository import BaseRepository
from app.models.group import Group

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

