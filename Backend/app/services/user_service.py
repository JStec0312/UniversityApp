from fastapi import HTTPException, Response
from app.models.user import User
from app.models.student import Student
from app.schemas.user import UserCreate
from app.schemas.student import StudentVerificationIn
from app.repositories.user_repository import UserRepository
from passlib.hash import bcrypt
from app.utils.generate_verification_token import generate_verification_token
from app.utils.send_verification_mail import send_verification_email
from jose import jwt,JWTError
from app.schemas.admin import AdminVerificationIn

import os
SECRET_KEY = os.getenv("JWT_SECRET")
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    def create_user(self, user_data: UserCreate) -> User:
        if self.user_repository.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = bcrypt.hash(user_data.password)
        try:
            user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                display_name=user_data.display_name,
                university_id=user_data.university_id,

            )
            new_user =  self.user_repository.create(user)
            token = generate_verification_token(new_user.id)

            send_verification_email(
                to_email=new_user.email,
                to_user=new_user.display_name,
                verification_token=token,
                university_id=new_user.university_id
            )
            
            return new_user
        
        except Exception as e:
            print("Error creating user:", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_by_id(self, user_id: int) -> User:
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))  
        
    
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
        

    def get_verification_token(self, user_id: int) -> str:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.verified:
            raise HTTPException(status_code=400, detail="User already verified")
        
        try:
            send_verification_email(
                to_email=user.email,
                to_user=user.display_name,
                verification_token=generate_verification_token(user.id)
            )
        except Exception as e:
            print("Error sending verification email:", str(e))
            raise HTTPException(status_code=500, detail=str(e))
        


    def get_user_email(self, user_id:int) -> str:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.email  