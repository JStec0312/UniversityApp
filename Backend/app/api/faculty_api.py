

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.faculty import FacultyOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory

router = APIRouter()

@router.get("/get-faculties-by-uni-id/{university_id}", response_model=list[FacultyOut])
def get_faculties_by_university_id(university_id: int, db: Session = Depends(get_db)):
    faculty_repo = RepositoryFactory(db).get_faculty_repository()
    faculty_service = ServiceFactory.get_faculty_service(faculty_repo)
    return faculty_service.get_faculties_by_university_id(university_id)
