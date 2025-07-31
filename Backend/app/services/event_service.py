from app.repositories.event_repository import EventRepository
from app.repositories.repository_factory import RepositoryFactory
from app.models.event import Event
from app.schemas.event import EventOutNotDetailed, EventUpdateIn
from app.utils.timebox import Clock


from fastapi import HTTPException
class EventService:
    def __init__(self, event_repo):
        self.event_repo: EventRepository = event_repo

    def get_upcoming_events(self, university_id: int, limit: int = 20, offset: int = 0):

        conditions = (
            Event.university_id == university_id,
            Event.start_date >= Clock.now()
        )

        events =  self.event_repo.getPaginatedWithConditions(conditions=conditions, skip=offset, limit=limit)
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
    
    def get_past_events(self, university_id: int, limit: int = 20, offset: int = 0):
        conditions = (
            Event.university_id == university_id,
            Event.end_date < Clock.now()
        )

        events = self.event_repo.getPaginatedWithConditions(conditions=conditions, skip=offset, limit=limit)
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
    
    def get_events_by_name(self, name: str, university_id: int, limit: int = 20, offset: int = 0):
        conditions = (
            Event.university_id == university_id,
            Event.title.ilike(f"%{name}%")
        )

        events = self.event_repo.getPaginatedWithConditions(conditions=conditions, skip=offset, limit=limit)
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
    
    def get_all_events(self, university_id: int, limit: int = 20, offset: int = 0):
        conditions = (Event.university_id == university_id,)

        events = self.event_repo.getPaginatedWithConditions(conditions=conditions, skip=offset, limit=limit)
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
    
    def get_event_by_id(self, event_id: int, university_id: int):
        events = self.event_repo.getPaginatedWithConditions(
            conditions=(Event.id == event_id, Event.university_id == university_id),
            skip=0,
            limit=1
        )
        event = events[0] if events else None

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        return EventOutNotDetailed(
            id=event.id,
            title=event.title,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            image_url=event.image_url,
            group_name=event.group_name if event.group else None
        )
    
    def update_event(self, event_data: EventUpdateIn):
        event = self.event_repo.get_by_id(event_data.id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        for field, value in event_data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        self.event_repo.update_by_id(event.id, event)
        return EventOutNotDetailed(
            id=event.id,
            title=event.title,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            image_url=event.image_url,
            group_name=event.group_name if event.group else None
        )