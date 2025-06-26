from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.user_service import UserService
from app.schemas.student import StudentVerificationIn
from app.schemas.user import UserOut
router = APIRouter()

@router.post("/verify/student/{token}", response_model=UserOut)
def verify_user(token: str, verification_info: StudentVerificationIn,  db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = UserService(user_repo)
    return user_service.verify_student(token, verification_info)

