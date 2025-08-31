from fastapi import APIRouter, Depends, Request, Query, status, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.news import NewsIn, NewsOut
from app.utils.security.require_roles import require_roles
from app.utils.enums.role_enum import RoleEnum

router = APIRouter()
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_news(news_in: NewsIn, db: Session = Depends(get_db), user: dict = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    news_repo = RepositoryFactory(db).get_news_repository()
    news_service = ServiceFactory.get_news_service(news_repo)
    return news_service.create_news(news_in, university_id= user["university_id"],user_id =  user["user_id"])

@router.get("/all", response_model=list[NewsOut])
def get_news(
    db: Session = Depends(get_db), 
    user: dict = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value, RoleEnum.STUDENT.value])),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
    ):
    news_repo = RepositoryFactory(db).get_news_repository()
    news_service = ServiceFactory.get_news_service(news_repo)
    return news_service.get_news_by_university(university_id=user["university_id"], limit=limit, offset=offset)

@router.get("/{news_id}", response_model=NewsOut)
def get_news_by_id(news_id: int, db: Session = Depends(get_db), user: dict = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value, RoleEnum.STUDENT.value]))):
    news_repo = RepositoryFactory(db).get_news_repository()
    news_service = ServiceFactory.get_news_service(news_repo)
    return news_service.get_news_by_id(news_id, university_id=user["university_id"])


@router.patch("/{news_id}", response_model=NewsOut)
def update_news(news_id: int, news_data: NewsIn, db: Session = Depends(get_db), user: dict = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    news_repo = RepositoryFactory(db).get_news_repository()
    news_service = ServiceFactory.get_news_service(news_repo)
    return news_service.update_news(news_id=news_id, news_data=news_data, university_id=user["university_id"], user_role=user["role"], user_id=user["user_id"])

@router.delete("/{news_id}")
def delete_news(response: Response, news_id: int, db: Session = Depends(get_db), user: dict = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    news_repo = RepositoryFactory(db).get_news_repository()
    news_service = ServiceFactory.get_news_service(news_repo)
    news_service.delete_news(news_id=news_id, university_id=user["university_id"], user_role=user["role"], user_id=user["user_id"])
    response.status_code = status.HTTP_204_NO_CONTENT
    return {"detail": "News deleted successfully"}
