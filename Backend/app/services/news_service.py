
from app.repositories.news_repository import NewsRepository
from app.repositories.admin_repository import AdminRepository
from app.schemas.news import NewsIn
from app.models.news import News
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
        return self.news_repository.getPaginatedWithConditions(
            conditions=[News.university_id == university_id],
            limit=limit,
            offset=offset
        )
    
    def get_news_by_group(self, group_id: int, limit: int = 10, offset: int = 0):
        return self.news_repository.getPaginatedWithConditions(
            conditions=[News.group_id == group_id],
            limit=limit,
            offset=offset
        )
    
    