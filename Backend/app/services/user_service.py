from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from passlib.hash import bcrypt


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreate) -> User:
        if self.user_repository.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = bcrypt.hash(user_data.password)

        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            display_name=user_data.display_name
        )

        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user  
