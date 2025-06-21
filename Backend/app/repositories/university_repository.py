from sqlalchemy.orm import Session
from app.models.university import University
from app.repositories.base_repository import BaseRepository
class UniversityRepository(BaseRepository[University]):
    def __init__(self, db: Session):
        super().__init__(db, University)
