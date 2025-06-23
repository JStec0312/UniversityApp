from app.repositories.base_repository import BaseRepository
from app.repositories.discount_repository import DiscountRepository
from app.repositories.event_rsvp_repository import EventRSVPRepository
from app.repositories.university_repository import UniversityRepository
from app.repositories.faculty_repository import FacultyRepository
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.major_repository import MajorRepository
from app.repositories.admin_repository import AdminRepository



class RepositoryFactory:
    def __init__(self, db):
        self.db = db

    def get_discount_repository(self) -> DiscountRepository:
        return DiscountRepository(self.db)

    def get_event_rsvp_repository(self) -> EventRSVPRepository:
        return EventRSVPRepository(self.db)

    def get_university_repository(self) -> UniversityRepository:
        return UniversityRepository(self.db)

    def get_faculty_repository(self) -> FacultyRepository:
        return FacultyRepository(self.db)

    def get_event_repository(self) -> EventRepository:
        return EventRepository(self.db)

    def get_user_repository(self) -> UserRepository:
        return UserRepository(self.db)
    
    def get_student_repository(self) -> StudentRepository:
        return StudentRepository(self.db)

    def get_admin_repository(self) -> AdminRepository:
        return AdminRepository(self.db)
    
    def get_major_repository(self) -> MajorRepository:
        return MajorRepository(self.db)
    
