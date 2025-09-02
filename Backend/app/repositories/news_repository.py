from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.news import News
from app.repositories.base_repository import BaseRepository

class NewsRepository(BaseRepository[News]):
    def __init__(self, session: Session):
        super().__init__(session, News)

    def get_by_admin_id(self, admin_id: int) -> list[News]:
        return (
            self.session.query(self.model)
            .filter(self.model.admin_id == admin_id)
            .all()
        )

    def get_latest(self, limit: int = 10) -> list[News]:
        return (
            self.session.query(self.model)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def search(self, query: str, limit: int = 20) -> list[News]:
        pattern = f"%{query}%"
        return (
            self.session.query(self.model)
            .filter(
                or_(
                    self.model.title.ilike(pattern),
                    self.model.content.ilike(pattern),
                )
            )
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )
