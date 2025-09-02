from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import HTTPException

from app.repositories.admin_repository import AdminRepository
from app.repositories.event_repository import EventRepository
from app.schemas.event import AddEventIn
from app.models.event import Event
from app.utils.uow import uow

class AdminService:
    def __init__(self, admin_repo: AdminRepository, group_repo=None, user_repo=None):
        self.admin_repo = admin_repo
        self.group_repo = group_repo
        self.user_repo = user_repo
        self.session = admin_repo.session  # jedna wspólna sesja/UoW

    def create_event(self, event_data: AddEventIn, user_id: int, university_id: int):
        # 1) uprawnienia/kontekst
        group_id = self.admin_repo.get_group_id_by_user_id(user_id)
        if not group_id:
            raise HTTPException(status_code=404, detail="Group not found for user")

        # 2) walidacja czasu
        start = event_data.start_date
        end = event_data.end_date
        now = datetime.now(ZoneInfo("Europe/Warsaw"))

        if start >= end:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        if start < now:
            raise HTTPException(status_code=400, detail="Start date cannot be in the past")

        # 3) zapis w jednej transakcji
        event_repo = EventRepository(self.session)
        new_event = Event(
            title=event_data.title,
            description=event_data.description,
            start_date=start,
            end_date=end,
            location=event_data.location,
            image_url=event_data.image_url,
            group_id=group_id,
            university_id=university_id,
        )

        with uow(self.session):
            event_repo.create(new_event)  # repo robi flush(), nie commit

        return {
            "status": "success",
            "message": "Event created successfully",
            "event_id": new_event.id,
        }
