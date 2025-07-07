

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.university import UniversityOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory

router = APIRouter()

@router.get("/get-universities", response_model=list[UniversityOut] )
def get_universities( db: Session = Depends(get_db)):
    university_repo = RepositoryFactory(db).get_university_repository()
    university_service = ServiceFactory.get_university_service(university_repo)
    return university_service.get_all_universities()
