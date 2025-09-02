from typing import List
from app.schemas.university import UniversityOut
from app.repositories.university_repository import UniversityRepository

class UniversityService:
    def __init__(self, university_repo: UniversityRepository):
        self.university_repo = university_repo

    def get_all_universities(self) -> List[UniversityOut]:
        return [
            UniversityOut(id=u.id, name=u.name)
            for u in self.university_repo.get_all_universities()
        ]
