from fastapi import HTTPException
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
        self.user_repository = user_repository

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
                verification_token=token
            )
            
            return new_user
        
        except Exception as e:
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
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = self.user_repository.get_by_id(user_id)
        

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.verified:
            raise HTTPException(status_code=400, detail="User already verified")
        
        try:
            self.user_repository.create_admin(
                user_id= user_id,
                group_id=verification_info.group_id,
            )
            self.user_repository.verify_user(user_id)    
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
            raise HTTPException(status_code=500, detail=str(e))