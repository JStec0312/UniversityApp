from app.models.user import User
import re
from app.core.service_errors import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    ServerErrorException,
    UserAlreadyVerifiedException,
    UserNotFoundException,
    UserNotVerifiedException,
)
from app.schemas.user import UserCreate, UserAuthIn
from app.repositories.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from app.utils.security.jwt_tokens import create_verify_token
from app.utils.enums.role_enum import RoleEnum
from app.utils.uow import uow
from app.schemas.user import UserOut
import os

SECRET_KEY = os.getenv("JWT_SECRET")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository
        # jedna sesja do transakcji (UoW)
        self.session = user_repository.session

    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = bcrypt.hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            display_name=user_data.display_name,
            university_id=user_data.university_id,
        )
        try:
            # transakcja kontrolowana przez serwis
            with uow(self.session):
                new_user = self.user_repository.create(user)  # repo robi flush, bez commit
                return new_user
        except IntegrityError:
            # np. UNIQUE(email)
            raise EmailAlreadyExistsException("Email already exists")
        except Exception:
            raise ServerErrorException("Error creating user")

    def prepare_verification_token(self, user_id: int) -> tuple[str, str, str, str]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        if user.verified:
            raise UserAlreadyVerifiedException("User already verified")
        token = create_verify_token(user_id)
        return token, user.email, user.display_name, user.university_id

    def issue_verification_token(self, user_id: int) -> str:
        return create_verify_token(user_id)

    def get_user_email(self, user_id: int) -> str:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        return user.email

    def get_user_by_id(self, user_id: int, university_id: int) -> UserOut:
        user = self.user_repository.get_first_with_conditions(
            conditions=(User.id == user_id, User.university_id == university_id)
        )
        if user is None:
            raise UserNotFoundException("User not found")
        return user

    @staticmethod
    def _normalize(term: str) -> str:
        term = (term or "").strip()
        return re.sub(r"\s+", " ", term)

    @staticmethod
    def _escape_like(term: str) -> str:
        return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    def search_users(
        self,
        name: str,
        university_id: int,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[User], int]:
        term = self._normalize(name)
        safe = self._escape_like(term)

        # multiword: "jan no" -> "%jan%no%"
        parts = [p for p in safe.split(" ") if p]
        like = f"%{'%'.join(parts)}%"

        conditions = (
            User.university_id == university_id,
            User.verified.is_(True),
            User.display_name.ilike(like, escape="\\"),
        )

        items = self.user_repository.get_paginated_with_conditions(
            conditions=conditions,
            limit=limit,
            offset=offset,
            order_by=(User.display_name.asc(), User.id.asc()),  # stabilna paginacja
        )
        total = self.user_repository.count_with_conditions(conditions)
        return items, total

    def authenticate_user(self, user_in: UserAuthIn) -> tuple[User, list[str]]:
        user = self.user_repository.get_by_email(user_in.email)
        if not user:
            raise UserNotFoundException("User not found")

        if not getattr(user, "verified", False):
            raise UserNotVerifiedException("User not verified")

        if not bcrypt.verify(user_in.password, user.hashed_password):
            raise InvalidCredentialsException("Invalid credentials")

        roles: list[str] = []
        if getattr(user, "admin", None):
            roles.append(RoleEnum.ADMIN.value)
        if getattr(user, "student", None):
            roles.append(RoleEnum.STUDENT.value)
        if getattr(user, "superior_admin", None):
            roles.append(RoleEnum.SUPERIOR_ADMIN.value)

        return user, roles
