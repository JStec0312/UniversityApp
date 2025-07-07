from app.repositories.faculty_repository import FacultyRepository
from app.schemas.faculty import FacultyOut
class FacultyService:
    def __init__(self, faculty_repository: FacultyRepository):
        self.faculty_repository = faculty_repository

    def get_faculties_by_university_id(self, university_id: int):
        faculties =  self.get_faculties_by_university_id
        return [
            FacultyOut(id=f.id, name=f.name, university_id=f.university_id)
            for f in self.faculty_repository.get_by_university_id(university_id)
        ]
    