"""
Admin-related fixtures for testing admin functionality.
"""
import pytest
from app.models import User, University, Faculty, Major, Group, Admin, SuperiorGroup, Student
from passlib.hash import bcrypt


@pytest.fixture
def seed_admin(db_session):
    """Creates a simple admin user with university structure."""
    def _seed():
        uni = University(name="Test University")
        db_session.add(uni)
        db_session.flush()

        faculty = Faculty(name="Test Faculty", university_id=uni.id)
        db_session.add(faculty)
        db_session.flush()

        major = Major(name="Test Major", faculty_id=faculty.id)
        db_session.add(major)
        db_session.flush()

        group = Group(group_name="Test Group", university_id=uni.id)
        db_session.add(group)
        db_session.flush()

        user = User(
            email="test@gmail.com",
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            university_id=uni.id,
            display_name="Admin User"
        )
        db_session.add(user)
        db_session.flush()

        admin = Admin(user_id=user.id, group_id=group.id)
        db_session.add(admin)
        db_session.flush()

        return {
            'uni': uni,
            'faculty': faculty,
            'major': major,
            'group': group,
            'user': user,
            'admin': admin
        }
    return _seed


@pytest.fixture
def superior_group_api_seed(db_session):
    """Creates superior admin, non-superior admin, and student for testing group permissions."""
    def _seed():
        university = University(id=1, name="Test University")
        db_session.add(university)
        db_session.flush()
        
        # Create faculty and major for students
        faculty = Faculty(id=1, name="Test Faculty", university_id=university.id)
        db_session.add(faculty)
        db_session.flush()
        
        major = Major(id=1, name="Test Major", faculty_id=faculty.id)
        db_session.add(major)
        db_session.flush()
        
        # Create superior group
        group = Group(group_name="Test Group", university_id=university.id)
        db_session.add(group)
        db_session.flush()
        
        superior_group = SuperiorGroup(
            university_id=university.id,
            group_id=group.id
        )
        db_session.add(superior_group)
        db_session.commit()

        # Create non superior group
        non_superior_group = Group(
            group_name="Non Superior Group",
            university_id=university.id
        )
        db_session.add(non_superior_group)
        db_session.commit()

        # Create superior admin user
        user = User(
            email="test@gmail.com",
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            university_id=university.id,
            display_name="Test User"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        admin = Admin(
            user_id=user.id,
            group_id=group.id
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        # Create non-superior admin
        user_non_superior = User(
            email="test2@gmail.com",
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            university_id=university.id,
            display_name="Test Non Superior User"
        )
        db_session.add(user_non_superior)
        db_session.commit()
        db_session.refresh(user_non_superior)
        
        non_superior_admin = Admin(
            user_id=user_non_superior.id,
            group_id=non_superior_group.id
        )
        db_session.add(non_superior_admin)
        db_session.commit()
        db_session.refresh(non_superior_admin)

        # Create student
        student_user = User(
            email="test3@gmail.com",
            hashed_password=bcrypt.hash("testpassword"),
            verified=True,
            university_id=university.id,
            display_name="Test Student User"
        )
        db_session.add(student_user)
        db_session.commit()
        db_session.refresh(student_user)
        
        student = Student(
            user_id=student_user.id,
            faculty_id=faculty.id,
            major_id=major.id
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        
        return {
            'university': university,
            'faculty': faculty,
            'major': major,
            'superior_group': group,
            'non_superior_group': non_superior_group,
            'superior_admin_user': user,
            'superior_admin': admin,
            'non_superior_admin_user': user_non_superior,
            'non_superior_admin': non_superior_admin,
            'student_user': student_user,
            'student': student
        }
    return _seed


@pytest.fixture
def group_register_seed(db_session):
    """Creates setup for group registration password testing."""
    def _seed():
        university = University(id=1, name="Test University")
        faculty = Faculty(id=1, name="Test Faculty", university_id=1)
        major = Major(id=1, name="Test Major", faculty_id=1)
        group = Group(university_id=1, group_name="Test Group")
        
        db_session.add_all([university, faculty, major, group])
        db_session.commit()
        
        # Create superior group
        superior_group = SuperiorGroup(
            university_id=1,
            group_id=1
        )
        db_session.add(superior_group)
        db_session.commit()
        
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
        db_session.commit()
        db_session.refresh(user)
        
        # Create admin record
        admin = Admin(
            user_id=user.id,
            group_id=1
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
        
        return {
            'university': university,
            'faculty': faculty,
            'major': major,
            'group': group,
            'superior_group': superior_group,
            'user': user,
            'admin': admin
        }
    return _seed
