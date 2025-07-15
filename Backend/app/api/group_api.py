
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.group import  GroupByUniOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory

router = APIRouter()

@router.get("/get-groups-by-university-id/{university_id}", response_model=list[GroupByUniOut])
def get_faculties_by_university_id(university_id:int,  db: Session = Depends(get_db)):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    return group_service.get_groups_by_university_id(university_id=university_id)
