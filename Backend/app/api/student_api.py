from fastapi import APIRouter, Depends, HTTPException, Response
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.exceptions.service_errors import (
    FacultyDoesNotBelongToUniversityException,
    InvalidVerificationTokenException,
    UserAlreadyVerifiedException,
    MajorDoesNotBelongToFacultyException,
    UserNotFoundException,
    InvalidInputException,
    InvalidCredentialsException,
    UserNotVerifiedException
)
from app.utils.security.require_roles import require_roles
from app.utils.role_enum import RoleEnum
from app.services.service_factory import ServiceFactory
from app.schemas.student import StudentOut, StudentVerificationIn, StudentAuthOut, StudentAuthIn, StudentMeOut
from app.schemas.user import UserOut
router = APIRouter()


@router.post("/verify", response_model = UserOut)
def verify_student(body: StudentVerificationIn, db: Session = Depends(get_db)):
    rf = RepositoryFactory(db)
    svc = ServiceFactory.get_student_service(
        rf.get_student_repository(),
        rf.get_faculty_repository(),
        rf.get_major_repository()
    )
    try:
        user = svc.verify_student(body.token, body.faculty_id, body.major_id)
        return user
    except InvalidVerificationTokenException:
        raise HTTPException(401, "Invalid verification token")
    except UserNotFoundException:
        raise HTTPException(404, "User not found")
    except UserAlreadyVerifiedException:
        raise HTTPException(409, "User already verified")
    except FacultyDoesNotBelongToUniversityException as e:
        raise HTTPException(400, str(e))
    except MajorDoesNotBelongToFacultyException as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, "Internal server error")