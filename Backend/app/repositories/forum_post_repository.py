from sqlalchemy.orm import Session
from app.models.forum_post import ForumPost
from app.repositories.base_repository import BaseRepository
from datetime import datetime

class ForumPostRepository(BaseRepository[ForumPost]):
    def get_by_user_id(self, db: Session, user_id: int) -> list[ForumPost]:
        return db.query(ForumPost).filter(ForumPost.user_id == user_id).all()
    
    def get_latest_posts(self, db: Session, limit: int = 20) -> list[ForumPost]:
        return db.query(ForumPost).order_by(ForumPost.created_at.desc()).limit(limit).all()
    
    def search_posts(self, db: Session, query: str, limit: int = 20) -> list[ForumPost]:
        search = f"%{query}%"
        return db.query(ForumPost).filter(
            ForumPost.title.ilike(search) | ForumPost.content.ilike(search)
        ).order_by(ForumPost.created_at.desc()).limit(limit).all()

    def get_posts_by_date(self, db: Session, date: datetime) -> list[ForumPost]:
        return db.query(ForumPost).filter(
            ForumPost.created_at.date() == date.date()
        ).order_by(ForumPost.created_at.desc()).all()
    
    