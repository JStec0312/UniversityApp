from typing import List
from sqlalchemy.exc import IntegrityError
from app.core.service_errors import NotFoundError, ForbiddenError

from app.repositories.news_repository import NewsRepository
from app.repositories.admin_repository import AdminRepository
from app.schemas.news import NewsIn, NewsUpdateIn, NewsOut
from app.models.news import News
from app.utils.enums.role_enum import RoleEnum
from app.utils.uow import uow

class NewsService:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository
        self.session = news_repository.session  # jedna sesja/UoW

    # --- CREATE ---
    def create_news(self, news_in: NewsIn, university_id: int, user_id: int) -> News:
        admin_repo = AdminRepository(self.session)
        group_id = admin_repo.get_group_id_by_user_id(user_id)

        news = News(
            title=news_in.title,
            content=news_in.content,
            group_id=group_id,
            university_id=university_id,
            image_url=news_in.image_url,
        )
        # transakcja kontrolowana przez serwis
        with uow(self.session):
            created = self.news_repository.create(news)
            return created

    # --- READ ---
    def get_news_by_university(self, university_id: int, limit: int = 10, offset: int = 0) -> List[News]:
        items = self.news_repository.get_paginated_with_conditions(
            conditions=[News.university_id == university_id],
            limit=limit,
            offset=offset,
            order_by=(News.created_at.desc(),),  # krotka
        )
        if not items:
            raise NotFoundError(message="No news found for this university", code="NEWS_NOT_FOUND")
        return items

    def get_news_by_group(self, group_id: int, university_id: int, limit: int = 10, offset: int = 0) -> List[News]:
        return self.news_repository.get_paginated_with_conditions(
            conditions=[News.group_id == group_id, News.university_id == university_id],  # naprawiony warunek
            limit=limit,
            offset=offset,
            order_by=(News.created_at.desc(),),
        )

    def get_news_by_id(self, news_id: int, university_id: int) -> News:
        news = self.news_repository.get_first_with_conditions(
            conditions=[News.id == news_id, News.university_id == university_id]
        )
        if news is None:
            raise NotFoundError(message="News not found", code="NEWS_NOT_FOUND")
        return news

    # --- UPDATE ---
    def update_news(
        self,
        news_id: int,
        news_data: NewsUpdateIn,
        university_id: int,
        user_role: str,
        user_id: int,
    ) -> NewsOut:
        admin_repo = AdminRepository(self.session)

        with uow(self.session):
            news = self.news_repository.get_by_id(news_id, for_update=True)
            if not news or news.university_id != university_id:
                raise NotFoundError(message="News not found", code="NEWS_NOT_FOUND")

            if user_role != RoleEnum.SUPERIOR_ADMIN.value:
                if admin_repo.get_group_id_by_user_id(user_id) != news.group_id:
                    raise ForbiddenError(message="You do not have permission to edit this news", code="NEWS_EDIT_FORBIDDEN")

            updated = self.news_repository.update_by_id(news_id, news_data.model_dump(exclude_unset=True))

            return NewsOut(
                id=updated.id,
                title=updated.title,
                content=updated.content,
                image_url=updated.image_url,
                created_at=updated.created_at,
            )

    # --- DELETE ---
    def delete_news(self, news_id: int, university_id: int, user_role: str, user_id: int) -> dict:
        admin_repo = AdminRepository(self.session)

        with uow(self.session):
            news = self.news_repository.get_by_id(news_id, for_update=True)
            if not news or news.university_id != university_id:
                raise NotFoundError(message="News not found", code="NEWS_NOT_FOUND")

            if user_role != RoleEnum.SUPERIOR_ADMIN.value:
                if admin_repo.get_group_id_by_user_id(user_id) != news.group_id:
                    raise ForbiddenError(message="You do not have permission to delete this news", code="NEWS_DELETE_FORBIDDEN")

            self.news_repository.delete_by_id(news_id)
            # brak commit tutaj – transakcja zamknie się na wyjściu z with

        return {"detail": "News deleted successfully"}
