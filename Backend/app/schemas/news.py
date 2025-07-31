from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

class NewsIn(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
