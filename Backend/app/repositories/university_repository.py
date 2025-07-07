from sqlalchemy.orm import Session
from app.models.university import University
from app.repositories.base_repository import BaseRepository
class UniversityRepository(BaseRepository[University]):
    def __init__(self, db: Session):
        super().__init__(db, University)

    def get_all_universities(self):
        """
        Retrieve all universities from the database.
        
        Returns:
            List[University]: A list of all universities.
        """
        return self.db.query(self.model).all()
