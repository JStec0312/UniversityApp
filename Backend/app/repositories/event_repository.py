from datetime import date
from sqlalchemy.orm import Session

from app.models.event import Event
from app.repositories.base_repository import BaseRepository

class EventRepository(BaseRepository[Event]):
    def __init__(self, session: Session):
        super().__init__(session, Event)

    def get_by_admin_id(self, admin_id: int) -> list[Event]:
        return (
            self.session.query(self.model)
            .filter(self.model.admin_id == admin_id)
            .all()
        )

    def get_upcoming_events(self, university_id: int, limit: int = 20) -> list[Event]:
        today = date.today()
        return (
            self.session.query(self.model)
            .join(self.model.group)
            .filter(
                self.model.start_date >= today,
                self.model.university_id == university_id,
            )
            .order_by(self.model.start_date)
            .limit(limit)
            .all()
        )

    def get_past_events(self, limit: int = 10) -> list[Event]:
        today = date.today()
        return (
            self.session.query(self.model)
            .filter(self.model.end_date < today)
            .order_by(self.model.end_date.desc())
            .limit(limit)
            .all()
        )
