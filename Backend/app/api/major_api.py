

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.major import MajorOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory

router = APIRouter()

@router.get("/get-majors-by-faculty-id/{faculty_id}", response_model=list[MajorOut])
def get_faculties_by_university_id(faculty_id: int, db: Session = Depends(get_db)):
    major_repo = RepositoryFactory(db).get_major_repository()
    major_service = ServiceFactory.get_major_service(major_repo)
    return major_service.get_majors_by_faculty_id(faculty_id = faculty_id )
