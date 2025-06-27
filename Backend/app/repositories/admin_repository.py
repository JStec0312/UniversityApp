from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from datetime import date

class AdminRepository(BaseRepository[Admin]):
    def __init__(self, db: Session):
        super().__init__(db, Admin)

    def get_by_user_id(self, user_id: int) -> Admin | None:
        return self.db.query(self.model).filter(self.model.user_id == user_id).first()

    def get_by_group_id(self, group_id: int) -> list[Admin]:
        return self.db.query(self.model).filter(self.model.group_id == group_id).all()

    def get_by_email(self, email: str) -> Admin | None:
        return (
            self.db.query(Admin)
            .join(Admin.user)  
            .filter(User.email == email)
            .first()
        )