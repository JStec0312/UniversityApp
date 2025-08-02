from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class AddEventIn(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    image_url: Optional[str] = None

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_custom_datetime(cls, value):
        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, "%Y-%m-%dT%H:%M")
                return dt.replace(tzinfo=ZoneInfo("Europe/Warsaw"))
            except ValueError:
                raise ValueError("Date must be in format YYYY-MM-DDTHH:MM (e.g. 2025-07-24T14:30)")
        return value

class EventUpdateIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None


class EventOutNotDetailed(BaseModel):
    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    image_url: Optional[str] = None
    group_name: str


