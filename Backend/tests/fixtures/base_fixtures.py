"""
Base fixtures for database setup and common entities.
"""
import pytest
from app.models import User, University, Faculty, Major, Group, SuperiorGroup, News
from passlib.hash import bcrypt


@pytest.fixture(scope="function")
def basic_seed(db_session):
    """Creates basic entities: university, faculty, major, groups, and users."""
    def _seed():
        # Create a university
        university = University(name="Test University")
        db_session.add(university)
        db_session.flush()

        # Create a faculty
        faculty = Faculty(name="Test Faculty", university_id=university.id)
        db_session.add(faculty)
        db_session.flush()

        # Create a major
        major = Major(name="Test Major", faculty_id=faculty.id)
        db_session.add(major)
        db_session.flush()

        # Create group
        group = Group(group_name="Test Group", university_id=university.id)
        db_session.add(group)
        db_session.flush()

        # Make previous group superior
        superior_group = SuperiorGroup(
            university_id=university.id,
            group_id=group.id
        )
        db_session.add(superior_group)
        db_session.flush()
        
        # Create non superior group
        non_superior_group = Group(
            group_name="Non Superior Group",
            university_id=university.id
        )
        db_session.add(non_superior_group)
        db_session.flush()

        # Create users
        user_student = User(
            email="user@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=True,
            university_id=university.id,
            display_name="Test User"
        )
        user_admin = User(
            email="admin@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=True,
            university_id=university.id,
            display_name="Test Admin"
        )
        user_non_superior_admin = User(
            email="nonsuperior@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=True,
            university_id=university.id,
            display_name="Test Non Superior Admin"
        )
        user_non_verified = User(
            email="nonverified@gmail.com",
            hashed_password=bcrypt.hash("password"),
            verified=False,
            university_id=university.id,
            display_name="Test Non Verified User"
        )

        db_session.add_all([user_student, user_admin, user_non_superior_admin, user_non_verified])
        db_session.flush()
        
        # Create student and admin records
        from app.models import Student, Admin
        student = Student(
            user_id=user_student.id,
            faculty_id=faculty.id,
            major_id=major.id
        )
        admin = Admin(
            user_id=user_admin.id,
            group_id=group.id
        )
        non_superior_admin = Admin(
            user_id=user_non_superior_admin.id,
            group_id=non_superior_group.id
        )

        db_session.add_all([student, admin, non_superior_admin])
        db_session.flush()

        news1 = News(
            title="News 1",
            content="Content for news 1",
            group_id=group.id,
            university_id=university.id,
            image_url="http://example.com/news1.jpg"
        )
        news2 = News(
            title="News 2",
            content="Content for news 2",
            group_id=non_superior_group.id,
            university_id=university.id,
            image_url="http://example.com/news2.jpg"
        )
        db_session.add_all([news1, news2])
        db_session.flush()      

        
        return {
            'university': university,
            'faculty': faculty,
            'major': major,
            'group': group,
            'superior_group': superior_group,
            'non_superior_group': non_superior_group,
            'users': {
                'student': user_student,
                'admin': user_admin,
                'non_superior_admin': user_non_superior_admin,
                'non_verified': user_non_verified
            },
            'student': student,
            'admin': admin,
            'non_superior_admin': non_superior_admin,
            'news': [news1, news2]
        }
    return _seed


@pytest.fixture
def user_seed(db_session):
    """Creates basic university structure for user tests."""
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
        
        return {
            'university': university,
            'faculty': faculty,
            'major': major,
            'group': group
        }
    return _seed
