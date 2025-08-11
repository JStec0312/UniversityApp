from app.models.user import User
from app.exceptions.service_errors import EmailAlreadyExistsException, ServerErrorException, UserAlreadyVerifiedException, UserNotFoundException
from app.schemas.user import UserCreate
from app.schemas.student import StudentVerificationIn
from app.repositories.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError, NoResultFound
from passlib.hash import bcrypt
from app.utils.generate_verification_token import generate_verification_token
from app.utils.send_verification_mail import send_verification_email
from jose import jwt,JWTError
from app.schemas.admin import AdminVerificationIn
from app.schemas.user import UserOut
from fastapi import HTTPException
import os
SECRET_KEY = os.getenv("JWT_SECRET")
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository


    def create_user(self, user_data: UserCreate) -> User:
        
        hashed_password = bcrypt.hash(user_data.password)
        user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                display_name=user_data.display_name,
                university_id=user_data.university_id,

            )
        
        try:
            new_user =  self.user_repository.create(user)
            return new_user

        except IntegrityError:
            raise EmailAlreadyExistsException("Email already exists")
        except Exception as e:
            raise ServerErrorException("Error creating user")


    def prepare_verification_token(self, user_id: int) -> tuple[str, str, str, str]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        if user.verified:
            raise UserAlreadyVerifiedException("User already verified")
        
        token = generate_verification_token(user_id)
        return token, user.email, user.display_name, user.university_id

    def issue_verification_token(self, user_id: int) -> str:
        return  generate_verification_token(user_id)


    
    def get_user_email(self, user_id:int) -> str:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        return user.email
    

    def get_user_by_id(self, user_id: int, university_id: int) -> UserOut:
        users = self.user_repository.get_paginated_with_conditions(
            conditions=(User.id == user_id, User.university_id == university_id),
            limit=1,
            offset=0,
            order_by=None
        )
        user = users[0] 
        if not user:
            raise UserNotFoundException("User not found")
        return user
    

    def search_users(self, name: str, university_id: int, limit: int = 20, offset: int = 0) -> list[User]:        
        def _escape_like(term: str) -> str:
            return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

        users = self.user_repository.get_paginated_with_conditions(
            conditions=(
                User.university_id == university_id,
                User.verified.is_(True),
                User.display_name.ilike(pattern, escape="\\"),
            ),
            order_by=(User.display_name.asc(), User.id.asc()),
            limit=limit,
            offset=offset,
        )
        return users
    



    def verify_student(self, token: str, verification_info: StudentVerificationIn) -> User:
        try: 
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"] )
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = self.user_repository.get_by_id(user_id)

        expected_university_id = self.user_repository.get_university_id_by_user_id(user_id)
        from app.repositories.faculty_repository import FacultyRepository
        facultyRepo = FacultyRepository(self.user_repository.db)        

        if facultyRepo.get_by_id(verification_info.faculty_id).university_id != expected_university_id:
            raise HTTPException(status_code=400, detail="Faculty does not belong to user's university")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.verified:
            raise HTTPException(status_code=400, detail="User already verified")
        
        try:
            self.user_repository.create_student(
                user_id=user.id,
                faculty_id=verification_info.faculty_id,
                major_id=verification_info.major_id
            )

            self.user_repository.verify_user(user_id)   
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    def verify_admin(self, token: str, verification_info: AdminVerificationIn) -> User:
        try: 
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"] )
            user_id = int(payload.get("sub"))  # Convert to int
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        # First check if user exists
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.verified:
            raise HTTPException(status_code=400, detail="User already verified")
        
        expected_university_id = self.user_repository.get_university_id_by_user_id(user_id)
        from app.repositories.group_repository import GroupRepository
        groupRepo = GroupRepository(self.user_repository.db)
        group = groupRepo.get_by_id(verification_info.group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        if group.university_id != expected_university_id:
            raise HTTPException(status_code=400, detail="Group does not belong to user's university")

        try:
            self.user_repository.create_admin(
                user_id=user_id,  # Already converted to int
                group_id=verification_info.group_id,
                group_password=verification_info.group_password
            )
            self.user_repository.verify_user(user_id)    # Already converted to int
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        





        