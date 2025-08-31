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
from app.services.group_membership_service import GroupMembershipService
from app.services.me_service import MeService

from app.repositories.group_invitation_repository import GroupInvitationRepository
from app.repositories.group_member_repository import GroupMemberRepository
from app.repositories.user_repository import UserRepository
from app.repositories.admin_repository import AdminRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.event_repository import EventRepository
from app.repositories.student_repository import StudentRepository


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
    
    @staticmethod
    def get_group_membership_service(group_members_repo: GroupMemberRepository = None, group_invite_repo: GroupInvitationRepository = None, user_repository: UserRepository = None, admin_repository: AdminRepository = None, group_repository: GroupRepository = None) -> GroupMembershipService:
        return GroupMembershipService(group_members_repo, group_invite_repo, user_repository, admin_repository, group_repository)


    @staticmethod
    def get_me_service(
        user_repository: UserRepository = None,
        group_repository: GroupRepository = None,
        event_repository: EventRepository = None,
        admin_repository: AdminRepository = None,
        student_repository: StudentRepository = None,
        group_member_repository: GroupMemberRepository = None,
        group_invitation_repository: GroupInvitationRepository = None
    ) -> MeService:
        return MeService(
            user_repository,
            group_repository,
            event_repository,
            admin_repository,
            student_repository,
            group_member_repository,
            group_invitation_repository
        )