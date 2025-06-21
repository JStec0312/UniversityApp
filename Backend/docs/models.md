# Models Documentation

This document provides detailed information about the database models used in the UniversityApp.

## Base Model

All models inherit from the `BaseModel` class, which provides common fields and functionality.

```python
class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
```

## User Model

The User model represents the core user entity for all system users.

```python
class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)
    
    # Relationships
    university = relationship("University", back_populates="users")
    student = relationship("Student", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    forum_posts = relationship("ForumPost", back_populates="user")
    event_rsvps = relationship("EventRSVP", back_populates="user")
```

### Methods

- `__init__(email, hashed_password, display_name=None, verified=False, university_id=None)`: Constructor for creating a new user

## Student Model

The Student model extends the User entity with student-specific attributes.

```python
class Student(BaseModel):
    __tablename__ = "students"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    student_id_number = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="student")
    faculty = relationship("Faculty", back_populates="students")
    major = relationship("Major", back_populates="students")
```

### Methods

- `__init__(user_id, faculty_id=None, major_id=None, graduation_year=None, student_id_number=None)`: Constructor for creating a new student

## Admin Model

The Admin model extends the User entity with admin-specific attributes.

```python
class Admin(BaseModel):
    __tablename__ = "admins"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    role = Column(String(50), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="admin")
```

### Methods

- `__init__(user_id, role)`: Constructor for creating a new admin

## University Model

The University model represents university entities.

```python
class University(BaseModel):
    __tablename__ = "universities"
    
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="university")
    faculties = relationship("Faculty", back_populates="university")
    news_items = relationship("News", back_populates="university")
    events = relationship("Event", back_populates="university")
    discounts = relationship("Discount", back_populates="university")
```

### Methods

- `__init__(name, location=None, website=None)`: Constructor for creating a new university

## Faculty Model

The Faculty model represents faculties within universities.

```python
class Faculty(BaseModel):
    __tablename__ = "faculties"
    
    name = Column(String(255), nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Relationships
    university = relationship("University", back_populates="faculties")
    majors = relationship("Major", back_populates="faculty")
    students = relationship("Student", back_populates="faculty")
```

### Methods

- `__init__(name, university_id)`: Constructor for creating a new faculty

## Major Model

The Major model represents academic majors within faculties.

```python
class Major(BaseModel):
    __tablename__ = "majors"
    
    name = Column(String(255), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="majors")
    students = relationship("Student", back_populates="major")
```

### Methods

- `__init__(name, faculty_id)`: Constructor for creating a new major

## News Model

The News model represents university news items.

```python
class News(BaseModel):
    __tablename__ = "news"
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Relationships
    university = relationship("University", back_populates="news_items")
```

### Methods

- `__init__(title, content, university_id)`: Constructor for creating a new news item

## Event Model

The Event model represents university events.

```python
class Event(BaseModel):
    __tablename__ = "events"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Relationships
    university = relationship("University", back_populates="events")
    rsvps = relationship("EventRSVP", back_populates="event")
```

### Methods

- `__init__(title, description, start_time, end_time, university_id, location=None)`: Constructor for creating a new event

## EventRSVP Model

The EventRSVP model represents user registrations for events.

```python
class EventRSVP(BaseModel):
    __tablename__ = "event_rsvps"
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False)  # attending, maybe, declined
    
    # Relationships
    event = relationship("Event", back_populates="rsvps")
    user = relationship("User", back_populates="event_rsvps")
```

### Methods

- `__init__(event_id, user_id, status)`: Constructor for creating a new event RSVP

## ForumPost Model

The ForumPost model represents forum discussions.

```python
class ForumPost(BaseModel):
    __tablename__ = "forum_posts"
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="forum_posts")
```

### Methods

- `__init__(title, content, user_id, category=None)`: Constructor for creating a new forum post

## Discount Model

The Discount model represents student discounts.

```python
class Discount(BaseModel):
    __tablename__ = "discounts"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Relationships
    university = relationship("University", back_populates="discounts")
```

### Methods

- `__init__(title, description, valid_from, valid_to, university_id)`: Constructor for creating a new discount

## Database Constraints

The models include the following constraints:

- **Primary Keys**: Each model has a unique ID as its primary key
- **Foreign Keys**: Relationships between models are enforced through foreign key constraints
- **Unique Constraints**: Email addresses, student ID numbers, etc., are enforced to be unique
- **Not Null Constraints**: Required fields are marked as not nullable

## Working with Models

### Creating a New Instance

```python
user = User(
    email="john@example.com",
    hashed_password="hashed_password_here",
    display_name="John Doe"
)

# Add to session and commit
db.add(user)
db.commit()
db.refresh(user)
```

### Retrieving Instances

```python
# Get by ID
user = db.query(User).filter(User.id == user_id).first()

# Get by email
user = db.query(User).filter(User.email == email).first()

# Get with relationships
student = db.query(Student).options(
    joinedload(Student.user),
    joinedload(Student.faculty),
    joinedload(Student.major)
).filter(Student.id == student_id).first()
```

### Updating Instances

```python
user = db.query(User).filter(User.id == user_id).first()
user.display_name = "New Name"
db.commit()
```

### Deleting Instances

```python
user = db.query(User).filter(User.id == user_id).first()
db.delete(user)
db.commit()
```
