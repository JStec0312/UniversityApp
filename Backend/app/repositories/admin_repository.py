"""
Admin repository module for database operations on Admin entities.

This module provides the AdminRepository class which extends the BaseRepository
to provide Admin-specific database operations.
"""

from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from datetime import date

class AdminRepository(BaseRepository[Admin]):
    """
    Repository for Admin entity database operations.
    
    This class provides methods for querying and manipulating Admin records
    in the database.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the AdminRepository with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        super().__init__(db, Admin)

    def get_by_user_id(self, user_id: int) -> Admin | None:
        """
        Get an admin by their associated user ID.
        
        Args:
            user_id: The ID of the user associated with the admin
            
        Returns:
            Admin: The found admin or None if not found
        """
        return self.db.query(self.model).filter(self.model.user_id == user_id).first()

    def get_by_group_id(self, group_id: int) -> list[Admin]:
        """
        Get all admins belonging to a specific group.
        
        Args:
            group_id: The ID of the group to filter by
            
        Returns:
            list[Admin]: List of admins in the specified group
        """
        return self.db.query(self.model).filter(self.model.group_id == group_id).all()

    def get_by_email(self, email: str) -> Admin | None:
        """
        Get an admin by their email address.
        
        This method joins the Admin and User tables to search by the email field
        in the User table.
        
        Args:
            email: The email address to search for
            
        Returns:
            Admin: The found admin or None if not found
        """
        return (
            self.db.query(Admin)
            .join(Admin.user)  
            .filter(User.email == email)
            .first()
        )
    
    def get_event_repository(self):
        """
        Get the event repository for creating events.
        
        This method returns the repository for managing events, which is used
        when an admin creates a new event.
        
        Returns:
            EventRepository: The repository for managing events
        """
        from app.repositories.event_repository import EventRepository
        return EventRepository(self.db)
    
    def get_group_id_by_user_id(self, user_id: int) -> int | None:
        """
        Get the group ID associated with a specific user ID.
        
        Args:
            user_id: The ID of the user to find the group for
            
        Returns:
            int: The group ID or None if not found
        """
        admin = self.get_by_user_id(user_id)
        return admin.group_id if admin else None