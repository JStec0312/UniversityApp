from sqlalchemy.orm import Session
from app.models.event_rsvp import EventRSVP
from app.repositories.base_repository import BaseRepository
from datetime import date

class EventRSVPRepository(BaseRepository[EventRSVP]):
    def get_by_event_id(self, db: Session, event_id: int) -> list[EventRSVP]:
        return db.query(EventRSVP).filter(EventRSVP.event_id == event_id).all()
    
    def get_by_user_id(self, db: Session, user_id: int) -> list[EventRSVP]:
        return db.query(EventRSVP).filter(EventRSVP.user_id == user_id).all()
    
    def count_by_event_id(self, db: Session, event_id: int) -> int:
        return db.query(EventRSVP).filter(EventRSVP.event_id == event_id).count()
    
    

