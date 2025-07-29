from app.repositories.event_repository import EventRepository
from app.repositories.repository_factory import RepositoryFactory
from fastapi import HTTPException
class EventService:
    def __init__(self, event_repo):
        self.event_repo: EventRepository = event_repo

    def get_upcoming_events(self, university_id: int):

        events =  self.event_repo.get_upcoming_events(university_id=university_id)
        from app.schemas.event import EventOutNotDetailed
        return [
            EventOutNotDetailed(
                id=event.id,
                title=event.title,
                description=event.description,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                image_url=event.image_url,
                group_name=event.group_name if event.group else None
            ) for event in events
        ]