"""
Base repository module for database operations.

This module provides the BaseRepository generic class which implements
common CRUD operations and query patterns for all entity repositories.
"""

from sqlalchemy.orm import Session
from typing import Generic, Iterable, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    Base repository class providing common CRUD operations.
    
    This generic class implements standard database operations that are common
    across all entity types, following the Repository pattern. It provides a
    consistent interface for database access and isolates the application from
    direct database dependencies.
    
    Type Parameters:
        T: The SQLAlchemy model type this repository works with
    """

    def __init__(self, db: Session, model: T):
        """
        Initialize the repository with a database session and model class.
        
        Args:
            db: SQLAlchemy database session
            model: SQLAlchemy model class this repository will work with
        """
        self.db = db
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get a record by its primary key ID.
        
        Args:
            id: Primary key ID to look up
            
        Returns:
            The found record or None if no record exists with the given ID
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, obj: T) -> T:
        """
        Create a new record in the database.
        
        This method adds the object to the session, commits the transaction,
        and refreshes the object to ensure it reflects the current database state.
        
        Args:
            obj: Model instance to create
            
        Returns:
            The created record with updated fields (e.g., ID, created_at)
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            raise e

    def update_by_id(self, id: int, updates: Dict[str, Any]) -> Optional[T]:
        """
        Update an existing record by ID with the provided field updates.
        
        Args:
            id: Primary key ID of the record to update
            updates: Dictionary of field names and their new values
            
        Returns:
            The updated record or None if no record exists with the given ID
        """
        obj = self.get_by_id(id)
        if not obj:
            return None

        for field, value in updates.items():
            setattr(obj, field, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_by_id(self, id: int) -> Optional[T]:
        """
        Delete a record by its primary key ID.
        
        Args:
            id: Primary key ID of the record to delete
            
        Returns:
            The deleted record or None if no record exists with the given ID
        """
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return obj
        return None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of records based on pagination parameters
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """
        Count the total number of records.
        
        Returns:
            Total count of records for this model
        """
        return self.db.query(self.model).count()
    
    def filter(self, **kwargs) -> List[T]:
        """
        Filter records based on given criteria.
        
        This method dynamically builds a query based on the provided field-value pairs.
        
        Args:
            **kwargs: Field-value pairs to filter by (e.g., name="John", age=30)
            
        Returns:
            List of records matching all filter criteria
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()
    
    def getPaginated(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get paginated records.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of records based on pagination parameters
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    

    def get_paginated_with_conditions(
        self,
        conditions: Iterable[Any] = (),
        offset: int = 0,
        limit: int = 100,
        order_by: Optional[Iterable[Any]] = None,  # 👈 nie str!
    ) -> List[T]:
        query = self.db.query(self.model).filter(*conditions)
        if order_by:
            query = query.order_by(*order_by)      
        return query.offset(offset).limit(limit).all()