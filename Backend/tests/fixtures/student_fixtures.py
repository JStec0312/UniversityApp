"""
Student-related fixtures for testing student functionality.
"""
import pytest
from app.models import User, University, Faculty, Major, Group, Student
from passlib.hash import bcrypt


@pytest.fixture
def student_seed(db_session):
    """Creates a student user with university structure."""
    def _seed():
        university = University(id=1, name="Test University")
        db_session.add(university)
        db_session.flush()
        
        faculty = Faculty(id=1, name="Test Faculty", university_id=1)
        db_session.add(faculty)
        db_session.flush()
        
        major = Major(id=1, name="Test Major", faculty_id=1)
        group = Group(university_id=1, group_name="Test Group")
        db_session.add_all([major, group])
        db_session.flush()
        
        # Create user with hashed password
        hashed_user_password = bcrypt.hash("testpassword")
        user = User(
            email='test@gmail.com',
            hashed_password=hashed_user_password,
            verified=True,
            display_name='Test User',
            university_id=1
        )
        db_session.add(user)
        db_session.flush()

        # Create student record
        student = Student(
            user_id=user.id,
            faculty_id=1,
            major_id=1
        )
        db_session.add(student)
        db_session.flush()

        return {
            'university': university,
            'faculty': faculty,
            'major': major,
            'group': group,
            'user': user,
            'student': student
        }
    return _seed
