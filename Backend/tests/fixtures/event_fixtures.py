"""
Event-related fixtures for testing event functionality.
"""
import pytest
from app.models import User, University, Faculty, Major, Group, Student, Event, Admin
from passlib.hash import bcrypt
from datetime import date


@pytest.fixture
def event_api_seed(db_session):
    """Creates two universities with events for testing event API."""
    def _seed():
        # Create two universities
        university1 = University(id=1, name="Test University 1")
        university2 = University(id=2, name="Test University 2")
        db_session.add_all([university1, university2])
        db_session.flush()
        
        # Create faculties
        faculty1 = Faculty(id=1, name="Test Faculty 1", university_id=1)
        faculty2 = Faculty(id=2, name="Test Faculty 2", university_id=2)
        db_session.add_all([faculty1, faculty2])
        db_session.flush()
        
        # Create majors
        major1 = Major(id=1, name="Test Major 1", faculty_id=1)
        major2 = Major(id=2, name="Test Major 2", faculty_id=2)
        db_session.add_all([major1, major2])
        db_session.flush()

        # Create groups
        group1 = Group(university_id=1, group_name="Test Group 1")
        group2 = Group(university_id=2, group_name="Test Group 2")
        db_session.add_all([group1, group2])
        db_session.flush()
        
        # Create events
        event1 = Event(
            title="Upcoming Event 1",
            description="Description for upcoming event 1",
            location="Location for event 1",
            start_date=date(2028, 10, 15),
            end_date=date(2028, 10, 16),
            group_id=group1.id,
            university_id=university1.id
        )
        event2 = Event(
            title="Upcoming Event 2",
            description="Description for upcoming event 2",
            location="Location for event 2",
            start_date=date(2028, 11, 20),
            end_date=date(2028, 11, 21),
            group_id=group2.id,
            university_id=university2.id
        )
        db_session.add_all([event1, event2])
        db_session.flush()
        
        # Create users from both universities
        user1 = User(
            email="test@gmail.com",    
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            display_name="Test User 1",
            university_id=1
        )
        user2 = User(
            email=" test2@gmail.com",
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            display_name="Test User 2",
            university_id=2
        )
        userAdmin = User(
            email="admin@gmail.com",
            hashed_password=bcrypt.hash("adminpassword"),
            verified=True,
            display_name="Admin User",
            university_id=1
        )
        db_session.add_all([user1, user2, userAdmin])
        db_session.flush()
        
        # Create students
        student1 = Student(
            user_id=user1.id,
            faculty_id=faculty1.id,
            major_id=major1.id
        )
        student2 = Student(
            user_id=user2.id,
            faculty_id=faculty2.id,
            major_id=major2.id
        )
        db_session.add_all([student1, student2])
        db_session.flush()

        #Create administrators
        admin = Admin(
            user_id=userAdmin.id,
            group_id=group1.id

        )
        db_session.add(admin)
        db_session.flush()

        
        
        return {
            'universities': [university1, university2],
            'faculties': [faculty1, faculty2],
            'majors': [major1, major2],
            'groups': [group1, group2],
            'events': [event1, event2],
            'users': [user1, user2],
            'students': [student1, student2],
            'admins': [userAdmin]
        }
    return _seed
