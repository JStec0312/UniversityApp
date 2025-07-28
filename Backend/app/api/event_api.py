from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import logging
from app.core.db import get_db
from app.schemas.event import EventOutNotDetailed
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.utils.require_roles import require_roles
from app.utils.role_enum import RoleEnum

router = APIRouter()
logger = logging.getLogger("app")  # własny logger; ustaw poziom na DEBUG w configu

@router.get("/upcoming", response_model=list[EventOutNotDetailed])
def get_upcoming_events(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles([
        RoleEnum.ADMIN.value,
        RoleEnum.SUPERIOR_ADMIN.value,
        RoleEnum.STUDENT.value,
    ])),
):
    token = request.cookies.get("access_token")  # <-- teraz jest
    logger.debug("cookie present=%s, len=%s", bool(token), len(token) if token else 0)
    logger.debug("user=%r", user)  # do podglądu claimsów

    event_repo = RepositoryFactory(db).get_event_repository()
    event_service = ServiceFactory.get_event_service(event_repo)
    return event_service.get_upcoming_events(university_id=user["university_id"])
