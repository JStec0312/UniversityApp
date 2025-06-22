from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from typing import List

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(self.model).filter(self.model.email == email).first()
    
    def get_by_username(self, username: str) -> List[User] | None:
        return self.db.query(self.model).filter(self.model.display_name == username).all()
    
    def verify_user(self,  id: int) -> User | None:
        user = self.get_by_id(id)
        if user:
            user.verified = True
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    

    