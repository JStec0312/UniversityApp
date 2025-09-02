from sqlalchemy.orm import Session
from app.models.event_rsvp import EventRSVP
from app.repositories.base_repository import BaseRepository

class EventRSVPRepository(BaseRepository[EventRSVP]):
    def __init__(self, session: Session):
        super().__init__(session, EventRSVP)

    def get_by_event_id(self, event_id: int) -> list[EventRSVP]:
        return (
            self.session.query(self.model)
            .filter(self.model.event_id == event_id)
            .all()
        )

    def get_by_user_id(self, user_id: int) -> list[EventRSVP]:
        return (
            self.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .all()
        )

    def count_by_event_id(self, event_id: int) -> int:
        return (
            self.session.query(self.model)
            .filter(self.model.event_id == event_id)
            .count()
        )
