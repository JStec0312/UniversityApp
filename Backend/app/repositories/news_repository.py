from sqlalchemy.orm import Session
from app.models.news import News
from app.repositories.base_repository import BaseRepository

class NewsRepository(BaseRepository[News]):
    def __init__(self, db: Session):
        super().__init__(db, News)

    def get_by_admin_id(self, admin_id: int) -> list[News]:
        return self.db.query(self.model).filter(self.model.admin_id == admin_id).all()

    def get_latest(self, limit: int = 10) -> list[News]:
        return self.db.query(self.model).order_by(self.model.created_at.desc()).limit(limit).all()
    
    def search(self, query: str, limit: int = 20) -> list[News]:
        search = f"%{query}%"
        return self.db.query(self.model).filter(
            self.model.title.ilike(search) | self.model.content.ilike(search)
        ).order_by(self.model.created_at.desc()).limit(limit).all()
    
    