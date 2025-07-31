from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import logging
from app.core.db import get_db
from app.schemas.event import EventOutNotDetailed, EventUpdateIn
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.utils.require_roles import require_roles
from app.utils.role_enum import RoleEnum

router = APIRouter()
logger = logging.getLogger("app")  # własny logger; ustaw poziom na DEBUG w configu

@router.get("/upcoming", response_model=list[EventOutNotDetailed])
def get_upcoming_events(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ])),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0) 
):
   

    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return event_service.get_upcoming_events(university_id=user["university_id"], limit=limit, offset=offset)


@router.get("/past", response_model=list[EventOutNotDetailed])
def get_past_events(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ])),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return event_service.get_past_events(university_id=user["university_id"], limit=limit, offset=offset)

@router.get("/search", response_model=list[EventOutNotDetailed])
def search_events(
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ])),
    name: str = Query(..., min_length=1, max_length=100),

):
    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return event_service.get_events_by_name(name=name, university_id=user["university_id"], limit=None, offset=0)

@router.get("/all", response_model=list[EventOutNotDetailed])
def get_all_events( 
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ])),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return event_service.get_all_events(university_id=user["university_id"], limit=limit, offset=offset)

@router.get("/{event_id}", response_model=EventOutNotDetailed)
def get_event_by_id(
    event_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ]))
):
    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return  event_service.get_event_by_id(event_id=event_id, university_id=user["university_id"])


@router.patch("/{event_id}", response_model=EventOutNotDetailed)
def update_event(
    event_id: int,
    event_data: EventUpdateIn,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ]))
    ):
    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return event_service.update_event(event_id=event_id, university_id=user["university_id"], event_data=event_data)