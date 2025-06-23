from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.utils.role_enum import RoleEnum
from app.repositories.admin_repository import AdminRepository
from app.repositories.student_repository import StudentRepository
from app.models.student import Student
from app.models.admin import Admin
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
        id = user.id
        if user:
            user.verified = True
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    def create_student(self, user_id:int,  faculty_id:int = None, major_id:int = None) -> User:
        existing_student = self.get_by_id(user_id)
        if existing_student:
            student_repo = StudentRepository(self.db)
            student = Student(
                user_id=user_id,
                faculty_id=faculty_id,
                major_id=major_id
            )
            student_repo.create(student)
            return None
    

    def create_admin(self, user_id: int,  group_id: int, faculty_id: int = None, major_id: int = None) -> User:
        existing_admin = self.get_by_id(user_id)
        if  existing_admin:
            admin = Admin(
                user_id=user_id,
                group_id=group_id,
                faculty_id=faculty_id,
                major_id=major_id
            )
            admin_repo = AdminRepository(self.db)
            admin_repo.create(admin)
            return None
    