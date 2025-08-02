
from app.repositories.news_repository import NewsRepository
from fastapi import HTTPException
from app.repositories.admin_repository import AdminRepository
from app.schemas.news import NewsIn, NewsUpdateIn, NewsOut
from app.models.news import News
from app.repositories.repository_factory import RepositoryFactory
from app.utils.role_enum import RoleEnum

class NewsService:
    
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    def create_news(self, news_in: NewsIn, university_id: int, user_id: int):
        admin_repo = AdminRepository(self.news_repository.db)
        group_id = admin_repo.get_group_id_by_user_id(user_id)
        news = News(
            title=news_in.title,
            content=news_in.content,
            group_id=group_id,
            university_id=university_id,
            image_url=news_in.image_url
        )
        return self.news_repository.create(news)
    

    def get_news_by_university(self, university_id: int, limit: int = 10, offset: int = 0):
        news =  self.news_repository.getPaginatedWithConditions(
            conditions=[News.university_id == university_id],
            limit=limit,
            offset=offset,
            order_by=News.created_at.desc()  # Assuming you want the latest news first
        )
        if not news:
            raise HTTPException(status_code=404, detail="No news found for this university")
        return news


    def get_news_by_group(self, group_id: int, university_id: int, limit: int = 10, offset: int = 0):
        return self.news_repository.getPaginatedWithConditions(
            conditions=[News.group_id == group_id, university_id == News.university_id],
            limit=limit,
            offset=offset,
            order_by=News.created_at.desc()  # Assuming you want the latest news first
        )
    


    def get_news_by_id(self, news_id: int, university_id: int):
        newsList = self.news_repository.getPaginatedWithConditions(
            conditions=[News.id == news_id, News.university_id == university_id]
        )
        if len(newsList) == 0:
            raise HTTPException(status_code=404, detail="News not found")
        return newsList[0]


    def update_news(self, news_id: int, news_data: NewsUpdateIn, university_id: int,  user_id: int, user_role: str) -> NewsOut:
        news = self.news_repository.get_by_id(news_id)
        if not news or news.university_id != university_id:
            raise HTTPException(status_code=404, detail="News not found")

        if news.university_id != university_id:
            raise HTTPException(status_code=403, detail="You do not have permission to edit this news")
        
        if user_role != RoleEnum.SUPERIOR_ADMIN.value:
            admin_repo = RepositoryFactory(self.news_repository.db).get_admin_repository()
            if admin_repo.get_group_id_by_user_id(user_id) != news.group_id:
                raise HTTPException(status_code=403, detail="You do not have permission to edit this news")

        news = self.news_repository.update_by_id(news_id, news_data.model_dump(exclude_unset=True))
        return NewsOut(
            id=news.id,
            title=news.title,
            content=news.content,
            image_url=news.image_url,
            created_at=news.created_at
        )
    

    def delete_news(self, news_id: int, university_id: int, user_role: str, user_id: int):
        news = self.news_repository.get_by_id(news_id)
        if not news or news.university_id != university_id:
            raise HTTPException(status_code=404, detail="News not found")

        if user_role != RoleEnum.SUPERIOR_ADMIN.value:
            admin_repo = RepositoryFactory(self.news_repository.db).get_admin_repository()
            if admin_repo.get_group_id_by_user_id(user_id) != news.group_id:
                raise HTTPException(status_code=403, detail="You do not have permission to delete this news")

        self.news_repository.delete_by_id(news_id)
        return {"detail": "News deleted successfully"}
