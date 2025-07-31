"""
Repository Factory module for creating repository instances.

This module provides the RepositoryFactory class which follows the factory pattern
to create and provide instances of various repository classes.
"""

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
from app.repositories.group_register_password_repository import GroupRegisterPasswordRepository


class RepositoryFactory:
    """
    Factory class for creating repository instances.
    
    This class follows the Factory pattern to provide a single point of creation
    for all repository objects, ensuring they are created with the correct database
    session and dependencies.
    """
    
    def __init__(self, db):
        """
        Initialize the RepositoryFactory with a database session.
        
        Args:
            db: SQLAlchemy database session to be used by all repositories
        """
        self.db = db

    def get_discount_repository(self) -> DiscountRepository:
        """
        Create and return a DiscountRepository instance.
        
        Returns:
            DiscountRepository: Repository for discount-related database operations
        """
        return DiscountRepository(self.db)

    def get_event_rsvp_repository(self) -> EventRSVPRepository:
        """
        Create and return an EventRSVPRepository instance.
        
        Returns:
            EventRSVPRepository: Repository for event RSVP-related database operations
        """
        return EventRSVPRepository(self.db)

    def get_university_repository(self) -> UniversityRepository:
        """
        Create and return a UniversityRepository instance.
        
        Returns:
            UniversityRepository: Repository for university-related database operations
        """
        return UniversityRepository(self.db)

    def get_faculty_repository(self) -> FacultyRepository:
        """
        Create and return a FacultyRepository instance.
        
        Returns:
            FacultyRepository: Repository for faculty-related database operations
        """
        return FacultyRepository(self.db)

    def get_event_repository(self) -> EventRepository:
        """
        Create and return an EventRepository instance.
        
        Returns:
            EventRepository: Repository for event-related database operations
        """
        return EventRepository(self.db)

    def get_user_repository(self) -> UserRepository:
        """
        Create and return a UserRepository instance.
        
        Returns:
            UserRepository: Repository for user-related database operations
        """
        return UserRepository(self.db)
    
    def get_student_repository(self) -> StudentRepository:
        """
        Create and return a StudentRepository instance.
        
        Returns:
            StudentRepository: Repository for student-related database operations
        """
        return StudentRepository(self.db)

    def get_admin_repository(self) -> AdminRepository:
        """
        Create and return an AdminRepository instance.
        
        Returns:
            AdminRepository: Repository for admin-related database operations
        """
        return AdminRepository(self.db)
    
    def get_major_repository(self) -> MajorRepository:
        """
        Create and return a MajorRepository instance.
        
        Returns:
            MajorRepository: Repository for major-related database operations
        """
        return MajorRepository(self.db)
    
    def get_group_register_password_repository(self) -> GroupRegisterPasswordRepository:
        """
        Create and return a GroupRegisterPasswordRepository instance.
        
        Returns:
            GroupRegisterPasswordRepository: Repository for group registration password-related database operations
        """
        return GroupRegisterPasswordRepository(self.db)
    
    def get_group_repository(self) -> BaseRepository:
        """
        Create and return a GroupRepository instance.
        
        Returns:
            BaseRepository: Repository for group-related database operations
        """
        from app.repositories.group_repository import GroupRepository
        return GroupRepository(self.db)
    
    def get_news_repository(self) -> BaseRepository:
        """
        Create and return a NewsRepository instance.
        
        Returns:
            BaseRepository: Repository for news-related database operations
        """
        from app.repositories.news_repository import NewsRepository
        return NewsRepository(self.db)
    
