"""
Repository Factory module for creating repository instances.

Uwaga: repozytoria nie robią commitów; transakcjami zarządza warstwa serwisów.
"""

from typing import TYPE_CHECKING
from sqlalchemy.orm import Session

from app.repositories.discount_repository import DiscountRepository
from app.repositories.event_rsvp_repository import EventRSVPRepository
from app.repositories.university_repository import UniversityRepository
from app.repositories.faculty_repository import FacultyRepository
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.major_repository import MajorRepository
from app.repositories.admin_repository import AdminRepository
from app.repositories.group_member_repository import GroupMemberRepository
from app.repositories.group_invitation_repository import GroupInvitationRepository

if TYPE_CHECKING:
    # tylko do typowania; unika cykli przy imporcie runtime
    from app.repositories.group_repository import GroupRepository
    from app.repositories.news_repository import NewsRepository


class RepositoryFactory:
    """
    Factory class for creating repository instances.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_discount_repository(self) -> DiscountRepository:
        return DiscountRepository(self.session)

    def get_event_rsvp_repository(self) -> EventRSVPRepository:
        return EventRSVPRepository(self.session)

    def get_university_repository(self) -> UniversityRepository:
        return UniversityRepository(self.session)

    def get_faculty_repository(self) -> FacultyRepository:
        return FacultyRepository(self.session)

    def get_event_repository(self) -> EventRepository:
        return EventRepository(self.session)

    def get_user_repository(self) -> UserRepository:
        return UserRepository(self.session)

    def get_student_repository(self) -> StudentRepository:
        return StudentRepository(self.session)

    def get_admin_repository(self) -> AdminRepository:
        return AdminRepository(self.session)

    def get_major_repository(self) -> MajorRepository:
        return MajorRepository(self.session)

    def get_group_repository(self) -> "GroupRepository":
        from app.repositories.group_repository import GroupRepository
        return GroupRepository(self.session)

    def get_news_repository(self) -> "NewsRepository":
        from app.repositories.news_repository import NewsRepository
        return NewsRepository(self.session)

    def get_group_member_repository(self) -> GroupMemberRepository:
        return GroupMemberRepository(self.session)

    def get_group_invitation_repository(self) -> GroupInvitationRepository:
        return GroupInvitationRepository(self.session)
