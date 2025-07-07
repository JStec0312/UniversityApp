"""
Service Factory module for creating service instances.

This module provides the ServiceFactory class which follows the factory pattern
to create and provide instances of various service classes.
"""



class ServiceFactory:
    """
    Factory class to create service instances.
    
    This class follows the Factory pattern to provide a single point of creation
    for all service objects, ensuring they are created with the correct dependencies.
    It abstracts the creation logic and helps with dependency injection.
    """

    @staticmethod
    def get_user_service(user_repo):
        """
        Create and return a UserService instance.
        
        Args:
            user_repo: User repository instance
            
        Returns:
            UserService: Service for user-related business logic
        """
        from app.services.user_service import UserService
        return UserService(user_repo)
    
    @staticmethod
    def get_student_service(user_repo):
        """
        Create and return a StudentService instance.
        
        Args:
            user_repo: User repository instance
            
        Returns:
            StudentService: Service for student-related business logic
        """
        from app.services.student_service import StudentService
        return StudentService(user_repo)

    @staticmethod
    def get_admin_service(user_repo):
        """
        Create and return an AdminService instance.
        
        Args:
            user_repo: User repository instance (or admin repository)
            
        Returns:
            AdminService: Service for admin-related business logic
        """
        from app.services.admin_service import AdminService
        return AdminService(user_repo)
    
    @staticmethod
    def get_group_register_password_service(group_register_password_repo):
        from app.services.group_register_password_service import GroupRegisterPasswordService
        return GroupRegisterPasswordService(group_register_password_repo)
    
    @staticmethod
    def get_university_service(university_repo):
        from app.services.university_service import UniversityService
        return UniversityService(university_repo)
    
    @staticmethod
    def get_faculty_service(faculty_repo):
        from app.services.faculty_service import FacultyService
        return FacultyService(faculty_repo)
    
    @staticmethod
    def get_major_service(major_repo):
        from app.services.major_service import MajorService
        return MajorService(major_repo)
    