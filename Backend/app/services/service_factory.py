from app.services.user_service import UserService


class ServiceFactory:
    """
    Factory class to create service instances.
    """

    @staticmethod
    def get_user_service(user_repo):
        """
        Create and return a UserService instance.
        """
        from app.services.user_service import UserService
        return UserService(user_repo)
    
    @staticmethod
    def get_student_service(user_repo):
        """
        Create and return a StudentService instance.
        """
        from app.services.student_service import StudentService
        return StudentService(user_repo)


    @ staticmethod
    def get_admin_service(user_repo):
        """
        Create and return an AdminService instance.
        """
        from app.services.admin_service import AdminService
        return AdminService(user_repo)