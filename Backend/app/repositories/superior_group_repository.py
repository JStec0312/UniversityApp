from app.repositories.base_repository import BaseRepo
from app.models.superior_group import SuperiorGroup

class SuperiorGroupRepository(BaseRepo[SuperiorGroup]):
    def __init__(self, db):
        super().__init__(db, SuperiorGroup)

    def get_by_name(self, name: str, university_id: int) -> SuperiorGroup | None:
        return self.db.query(self.model).filter(
            self.model.name == name,
            self.model.university_id == university_id
        ).first()

    def get_by_university_id(self, university_id: int) -> list[SuperiorGroup]:
        return self.db.query(self.model).filter(
            self.model.university_id == university_id
        ).all()