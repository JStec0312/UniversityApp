from sqlalchemy.orm import Session
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    Base repository class providing common CRUD operations.
    """

    def __init__(self, db:Session ,model: T):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get a record by its ID.
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, obj: T) -> T:
        """
        Create a new record.
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update_by_id(self, id: int, updates: dict) -> Optional[T]:
        """
        Update an existing record by ID with the provided field updates.
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
        Delete a record by its ID.
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
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """
        Count the total number of records.
        """
        return self.db.query(self.model).count()
    
    def filter(self, **kwargs) -> List[T]:
        """
        Filter records based on given criteria.
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()
    
    def getPaginated(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get paginated records.
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
