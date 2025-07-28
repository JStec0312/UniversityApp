from app.repositories.event_repository import EventRepository
from app.repositories.repository_factory import RepositoryFactory
from fastapi import HTTPException
class EventService:
    def __init__(self, event_repo):
        self.event_repo: EventRepository = event_repo

    def get_upcoming_events(self, university_id: int):

        return self.event_repo.get_upcoming_events(university_id=university_id)