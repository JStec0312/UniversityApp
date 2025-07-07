from app.repositories.major_repository import MajorRepository
from app.schemas.major import MajorOut
class MajorService:
    
    def __init__(self, major_repository: MajorRepository):
        self.major_repository = major_repository

    def get_majors_by_faculty_id(self, faculty_id: int):
        majors = self.major_repository.get_by_faculty_id(faculty_id)
        return [
            MajorOut(id=m.id, name=m.name, faculty_id=m.faculty_id)
            for m in majors
        ]
    