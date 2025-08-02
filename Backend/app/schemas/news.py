from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class NewsIn(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class NewsOut(NewsIn):
    id: int
    created_at: datetime

class NewsUpdateIn(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None


