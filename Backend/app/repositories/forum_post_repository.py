from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.models.forum_post import ForumPost
from app.repositories.base_repository import BaseRepository

class ForumPostRepository(BaseRepository[ForumPost]):
    def __init__(self, session: Session):
        super().__init__(session, ForumPost)

    def get_by_user_id(self, user_id: int) -> list[ForumPost]:
        return (
            self.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .all()
        )

    def get_latest_posts(self, limit: int = 20) -> list[ForumPost]:
        return (
            self.session.query(self.model)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )

    def search_posts(self, query: str, limit: int = 20) -> list[ForumPost]:
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

    def get_posts_by_date(self, when: datetime) -> list[ForumPost]:
        target_date = when.date()
        return (
            self.session.query(self.model)
            .filter(func.date(self.model.created_at) == target_date)
            .order_by(self.model.created_at.desc())
            .all()
        )
