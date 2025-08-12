"""
Service Factory module for creating service instances.

This module provides the ServiceFactory class which follows the factory pattern
to create and provide instances of various service classes.
"""



from app.services.event_service import EventService
from app.services.group_service import GroupService
from app.services.news_service import NewsService
from app.services.student_service import StudentService
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.services.university_service import UniversityService
from app.services.faculty_service import FacultyService
from app.services.major_service import MajorService

class ServiceFactory:
    """
    Factory class to create service instances.
    
    This class follows the Factory pattern to provide a single point of creation
    for all service objects, ensuring they are created with the correct dependencies.
    It abstracts the creation logic and helps with dependency injection.
    """

    @staticmethod
    def get_user_service(user_repo) -> UserService:
        """
        Create and return a UserService instance.
        
        Args:
            user_repo: User repository instance
            
        Returns:
            UserService: Service for user-related business logic
        """
        return UserService(user_repo)
    
    @staticmethod
    def get_student_service(user_repo, faculty_repo = None, major_repo = None) -> StudentService:
        """
        Create and return a StudentService instance.
        
        Args:
            user_repo: User repository instance
            
        Returns:
            StudentService: Service for student-related business logic
        """
        return StudentService(user_repo, faculty_repo, major_repo)

    @staticmethod
    def get_admin_service(user_repo) -> AdminService:
        """
        Create and return an AdminService instance.
        
        Args:
            user_repo: User repository instance (or admin repository)
            
        Returns:
            AdminService: Service for admin-related business logic
        """
        return AdminService(user_repo)
    
    @staticmethod
    def get_university_service(university_repo) -> UniversityService:
        return UniversityService(university_repo)
    
    @staticmethod
    def get_faculty_service(faculty_repo) -> FacultyService:
        return FacultyService(faculty_repo)
    
    @staticmethod
    def get_major_service(major_repo):
        return MajorService(major_repo)
    
    @staticmethod
    def get_group_service(group_repo) -> GroupService:
        return GroupService(group_repo)
    
    @staticmethod
    def get_event_service(event_repo) -> EventService:
        return EventService(event_repo)
    
    @staticmethod
    def get_news_service(news_repo) -> NewsService:
        return NewsService(news_repo)
    

