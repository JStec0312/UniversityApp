# Repositories Documentation

This document provides detailed information about the repository pattern implementation in the UniversityApp.

## Overview

The repository pattern is used to abstract the data access layer from the business logic. Each repository provides methods for performing CRUD (Create, Read, Update, Delete) operations on a specific model.

## Base Repository

All repositories inherit from the `BaseRepository` class, which provides common operations:

```python
class BaseRepository(Generic[T]):
    """
    Base repository class providing common CRUD operations.
    """

    def __init__(self, db: Session, model: T):
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
    
    def update_by_id(self, id: int) -> T:
        """
        Update an existing record.
        """
        obj = self.get_by_id(id)
        if not obj:
            return None
        self.db.add(obj)
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
```

## Specific Repositories

### User Repository

The `UserRepository` class extends the `BaseRepository` to provide user-specific operations:

```python
class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_university(self, university_id: int) -> List[User]:
        """
        Get all users belonging to a university.
        """
        return self.db.query(User).filter(User.university_id == university_id).all()
```

### Student Repository

The `StudentRepository` class extends the `BaseRepository` to provide student-specific operations:

```python
class StudentRepository(BaseRepository[Student]):
    def __init__(self, db: Session):
        super().__init__(db, Student)
    
    def get_by_user_id(self, user_id: int) -> Optional[Student]:
        """
        Get a student by user ID.
        """
        return self.db.query(Student).filter(Student.user_id == user_id).first()
    
    def get_by_student_id_number(self, student_id_number: str) -> Optional[Student]:
        """
        Get a student by student ID number.
        """
        return self.db.query(Student).filter(Student.student_id_number == student_id_number).first()
    
    def get_by_faculty(self, faculty_id: int) -> List[Student]:
        """
        Get all students in a faculty.
        """
        return self.db.query(Student).filter(Student.faculty_id == faculty_id).all()
    
    def get_by_major(self, major_id: int) -> List[Student]:
        """
        Get all students in a major.
        """
        return self.db.query(Student).filter(Student.major_id == major_id).all()
```

### News Repository

The `NewsRepository` class extends the `BaseRepository` to provide news-specific operations:

```python
class NewsRepository(BaseRepository[News]):
    def __init__(self, db: Session):
        super().__init__(db, News)
    
    def get_by_university(self, university_id: int, skip: int = 0, limit: int = 100) -> List[News]:
        """
        Get news items for a university with pagination.
        """
        return self.db.query(News).filter(
            News.university_id == university_id
        ).offset(skip).limit(limit).all()
    
    def get_latest(self, limit: int = 10) -> List[News]:
        """
        Get the latest news items.
        """
        return self.db.query(News).order_by(News.created_at.desc()).limit(limit).all()
```

### Event Repository

The `EventRepository` class extends the `BaseRepository` to provide event-specific operations:

```python
class EventRepository(BaseRepository[Event]):
    def __init__(self, db: Session):
        super().__init__(db, Event)
    
    def get_by_university(self, university_id: int, skip: int = 0, limit: int = 100) -> List[Event]:
        """
        Get events for a university with pagination.
        """
        return self.db.query(Event).filter(
            Event.university_id == university_id
        ).offset(skip).limit(limit).all()
    
    def get_upcoming(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """
        Get upcoming events with pagination.
        """
        now = datetime.utcnow()
        return self.db.query(Event).filter(
            Event.start_time > now
        ).order_by(Event.start_time).offset(skip).limit(limit).all()
```

### EventRSVP Repository

The `EventRSVPRepository` class extends the `BaseRepository` to provide event RSVP-specific operations:

```python
class EventRSVPRepository(BaseRepository[EventRSVP]):
    def __init__(self, db: Session):
        super().__init__(db, EventRSVP)
    
    def get_by_event(self, event_id: int) -> List[EventRSVP]:
        """
        Get all RSVPs for an event.
        """
        return self.db.query(EventRSVP).filter(EventRSVP.event_id == event_id).all()
    
    def get_by_user(self, user_id: int) -> List[EventRSVP]:
        """
        Get all RSVPs for a user.
        """
        return self.db.query(EventRSVP).filter(EventRSVP.user_id == user_id).all()
    
    def get_by_event_and_user(self, event_id: int, user_id: int) -> Optional[EventRSVP]:
        """
        Get RSVP for a specific event and user.
        """
        return self.db.query(EventRSVP).filter(
            EventRSVP.event_id == event_id,
            EventRSVP.user_id == user_id
        ).first()
```

### ForumPost Repository

The `ForumPostRepository` class extends the `BaseRepository` to provide forum post-specific operations:

```python
class ForumPostRepository(BaseRepository[ForumPost]):
    def __init__(self, db: Session):
        super().__init__(db, ForumPost)
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ForumPost]:
        """
        Get forum posts by a user with pagination.
        """
        return self.db.query(ForumPost).filter(
            ForumPost.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[ForumPost]:
        """
        Get forum posts by category with pagination.
        """
        return self.db.query(ForumPost).filter(
            ForumPost.category == category
        ).offset(skip).limit(limit).all()
    
    def get_latest(self, skip: int = 0, limit: int = 100) -> List[ForumPost]:
        """
        Get latest forum posts with pagination.
        """
        return self.db.query(ForumPost).order_by(
            ForumPost.created_at.desc()
        ).offset(skip).limit(limit).all()
```

### Discount Repository

The `DiscountRepository` class extends the `BaseRepository` to provide discount-specific operations:

```python
class DiscountRepository(BaseRepository[Discount]):
    def __init__(self, db: Session):
        super().__init__(db, Discount)
    
    def get_by_university(self, university_id: int, skip: int = 0, limit: int = 100) -> List[Discount]:
        """
        Get discounts for a university with pagination.
        """
        return self.db.query(Discount).filter(
            Discount.university_id == university_id
        ).offset(skip).limit(limit).all()
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[Discount]:
        """
        Get active discounts with pagination.
        """
        now = datetime.utcnow()
        return self.db.query(Discount).filter(
            Discount.valid_from <= now,
            Discount.valid_to >= now
        ).offset(skip).limit(limit).all()
```

## Repository Factory

The `RepositoryFactory` class provides a convenient way to create repositories:

```python
class RepositoryFactory:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_repository(self) -> UserRepository:
        return UserRepository(self.db)
    
    def get_student_repository(self) -> StudentRepository:
        return StudentRepository(self.db)
    
    def get_news_repository(self) -> NewsRepository:
        return NewsRepository(self.db)
    
    def get_event_repository(self) -> EventRepository:
        return EventRepository(self.db)
    
    def get_event_rsvp_repository(self) -> EventRSVPRepository:
        return EventRSVPRepository(self.db)
    
    def get_forum_post_repository(self) -> ForumPostRepository:
        return ForumPostRepository(self.db)
    
    def get_discount_repository(self) -> DiscountRepository:
        return DiscountRepository(self.db)
```

## Usage Examples

### Creating a User

```python
def create_user(db: Session, email: str, password: str, display_name: str = None):
    user_repo = UserRepository(db)
    
    # Check if user already exists
    existing_user = user_repo.get_by_email(email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Hash password (implementation not shown)
    hashed_password = hash_password(password)
    
    # Create user
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        display_name=display_name
    )
    
    return user_repo.create(new_user)
```

### Getting User with Student Profile

```python
def get_student_profile(db: Session, user_id: int):
    user_repo = UserRepository(db)
    student_repo = StudentRepository(db)
    
    user = user_repo.get_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    
    student = student_repo.get_by_user_id(user_id)
    if not student:
        raise ValueError("Student profile not found for this user")
    
    return {
        "user": user,
        "student": student
    }
```

### Creating an Event and RSVP

```python
def create_event_and_rsvp(db: Session, event_data: dict, user_id: int):
    event_repo = EventRepository(db)
    event_rsvp_repo = EventRSVPRepository(db)
    
    # Create event
    new_event = Event(
        title=event_data["title"],
        description=event_data["description"],
        start_time=event_data["start_time"],
        end_time=event_data["end_time"],
        location=event_data.get("location"),
        university_id=event_data["university_id"]
    )
    created_event = event_repo.create(new_event)
    
    # Create RSVP for the organizer
    new_rsvp = EventRSVP(
        event_id=created_event.id,
        user_id=user_id,
        status="attending"
    )
    event_rsvp_repo.create(new_rsvp)
    
    return created_event
```
