from fastapi import APIRouter, Depends, Request, Query, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.news import NewsIn
from app.utils.require_roles import require_roles
from app.utils.role_enum import RoleEnum

router = APIRouter()
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_news(news_in: NewsIn, db: Session = Depends(get_db), user: dict = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    news_repo = RepositoryFactory(db).get_news_repository()
    news_service = ServiceFactory.get_news_service(news_repo)
    return news_service.create_news(news_in, university_id= user["university_id"],user_id =  user["user_id"])

