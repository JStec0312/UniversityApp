from typing import List
from sqlalchemy.orm import Session
from app.models.university import University
from app.repositories.base_repository import BaseRepository

class UniversityRepository(BaseRepository[University]):
    def __init__(self, session: Session):
        super().__init__(session, University)

    def get_all_universities(self) -> List[University]:
        """
        Retrieve all universities from the database.
        """
        return self.session.query(self.model).all()
